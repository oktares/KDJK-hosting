#!/usr/bin/env python3
"""
scripts/sync-workflow.py
Otomasi Sinkronisasi & Auto-Publish n8n Workflow dari file JSON ke Database PostgreSQL.

Fungsi:
1. Membaca file workflows/personal-finance-bot.json.
2. Mengambil kredensial riil (Telegram & Postgres) dari tabel credentials_entity di PostgreSQL.
3. Menginjeksi kredensial riil dan API key dari .env ke node workflow.
4. Membandingkan workflow baru dengan yang sedang aktif di database (tabel workflow_entity).
5. JIKA TIDAK ADA PERUBAHAN & sudah aktif:
   -> Lewati (tidak ada restart/publish, exit 0).
6. JIKA ADA PERUBAHAN atau belum aktif:
   -> Update workflow_entity, set active = true, update versionId & workflow_history.
   -> Restart kontainer n8n agar webhook Telegram otomatis teregistrasi ulang ke versi mutakhir.
"""

import os
import sys
import json
import uuid
import time
import subprocess
from pathlib import Path

# Path konfigurasi
PROJECT_DIR = Path(__file__).resolve().parent.parent
WORKFLOW_FILE = PROJECT_DIR / "workflows" / "personal-finance-bot.json"
ENV_FILE = PROJECT_DIR / ".env"

def load_env():
    """Membaca file .env jika ada."""
    env_vars = {}
    if ENV_FILE.exists():
        with open(ENV_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    env_vars[k.strip()] = v.strip().strip("'\"")
    return env_vars

def run_psql(sql_query, db_user, db_name, container_name="n8n_postgres"):
    """Menjalankan query SQL di container postgres dan mengembalikan output stdout."""
    cmd = [
        "docker", "exec", "-i", container_name,
        "psql", "-U", db_user, "-d", db_name,
        "-t", "-A", "-c", sql_query
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
    return res.stdout.strip()

def run_psql_stdin(sql_query, db_user, db_name, container_name="n8n_postgres"):
    """Menjalankan query SQL besar via stdin."""
    cmd = [
        "docker", "exec", "-i", container_name,
        "psql", "-U", db_user, "-d", db_name
    ]
    res = subprocess.run(cmd, input=sql_query, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
    return res.stdout.strip()

def main():
    print("==================================================================")
    print("🤖 n8n Workflow Auto-Sync & Auto-Publisher")
    print("==================================================================")

    if not WORKFLOW_FILE.exists():
        print(f"[ERROR] File workflow tidak ditemukan di {WORKFLOW_FILE}")
        sys.exit(1)

    env_vars = load_env()
    db_user = env_vars.get("POSTGRES_USER", "n8n_admin")
    db_name = env_vars.get("POSTGRES_DB", "n8n_db")
    container_name = "n8n_postgres"

    # 1. Pastikan container postgres berjalan
    try:
        check_pg = subprocess.run(
            ["docker", "inspect", "-f", "{{.State.Running}}", container_name],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        if check_pg.stdout.strip() != "true":
            print(f"[ERROR] Kontainer {container_name} tidak aktif!")
            sys.exit(1)
    except Exception as e:
        print(f"[ERROR] Gagal memeriksa status kontainer: {e}")
        sys.exit(1)

    # 2. Ambil kredensial riil dari database (credentials_entity)
    print("[INFO] Mengambil kredensial riil dari database n8n...")
    try:
        sql_creds = "SELECT json_agg(t) FROM (SELECT id, name, type FROM credentials_entity) t;"
        creds_json = run_psql(sql_creds, db_user, db_name, container_name)
        creds_list = json.loads(creds_json) if creds_json else []
    except Exception as e:
        print(f"[WARNING] Gagal mengambil credentials_entity ({e}), mencoba fallback kredensial...")
        creds_list = []

    tg_cred = None
    pg_cred = None
    for c in creds_list:
        if c.get("type") == "telegramApi" and not tg_cred:
            tg_cred = {"id": c["id"], "name": c["name"]}
        elif c.get("type") == "postgres" and not pg_cred:
            pg_cred = {"id": c["id"], "name": c["name"]}

    # Fallback kredensial jika credentials_entity kosong
    if not tg_cred:
        tg_cred = {"id": "ZJgioklOFZpvg5j7", "name": "Telegram account"}
    if not pg_cred:
        pg_cred = {"id": "bdSHEy7ZlxpgBCkC", "name": "Postgres account"}

    print(f"[INFO] Kredensial terdeteksi -> Telegram: {tg_cred['name']} ({tg_cred['id']}), Postgres: {pg_cred['name']} ({pg_cred['id']})")

    # 3. Baca file workflow baru
    with open(WORKFLOW_FILE, "r", encoding="utf-8") as f:
        file_wf = json.load(f)

    new_nodes = file_wf.get("nodes", [])
    new_connections = file_wf.get("connections", {})
    new_name = file_wf.get("name", "Bot Manajemen Keuangan Pribadi (KDJK Telegram & Gemini AI)")
    new_settings = file_wf.get("settings", {})

    # Injeksi kredensial riil ke node baru
    groq_api_key = env_vars.get("GROQ_API_KEY", "")
    for node in new_nodes:
        creds = node.get("credentials", {})
        if "telegramApi" in creds:
            creds["telegramApi"] = tg_cred
        if "postgres" in creds:
            creds["postgres"] = pg_cred

        # Pastikan Authorization Groq / Gemini di header jika ada API key di .env
        if groq_api_key and "HTTP Request" in node.get("name", ""):
            params = node.get("parameters", {})
            header_params = params.get("headerParameters", {}).get("parameters", [])
            for hp in header_params:
                if hp.get("name") == "Authorization" and "YOUR_GROQ_API_KEY" in hp.get("value", ""):
                    hp["value"] = f'=Bearer {{{{ $env.GROQ_API_KEY || "{groq_api_key}" }}}}'

    # 4. Ambil data workflow yang saat ini aktif di database (workflow_entity)
    print("[INFO] Mengambil data alur kerja aktif di database...")
    sql_current_wf = """
    SELECT row_to_json(t) FROM (
        SELECT id, name, active, nodes, connections, "versionId" 
        FROM workflow_entity 
        ORDER BY "updatedAt" DESC 
        LIMIT 1
    ) t;
    """
    current_wf_json = run_psql(sql_current_wf, db_user, db_name, container_name)
    current_wf = json.loads(current_wf_json) if current_wf_json else None

    workflow_id = current_wf.get("id", "veHMz9UkgGMlUh4n") if current_wf else "veHMz9UkgGMlUh4n"

    # 5. Deteksi Perubahan (Change Detection)
    has_changes = False
    reason = []

    if not current_wf:
        has_changes = True
        reason.append("Workflow belum ada di database")
    else:
        is_active = current_wf.get("active", False)
        if not is_active:
            has_changes = True
            reason.append("Status workflow saat ini belum aktif (unpublished)")

        # Bandingkan nodes & connections
        curr_nodes_str = json.dumps(current_wf.get("nodes", []), sort_keys=True)
        new_nodes_str = json.dumps(new_nodes, sort_keys=True)
        if curr_nodes_str != new_nodes_str:
            has_changes = True
            reason.append("Perubahan pada struktur node workflow terdeteksi")

        curr_conn_str = json.dumps(current_wf.get("connections", {}), sort_keys=True)
        new_conn_str = json.dumps(new_connections, sort_keys=True)
        if curr_conn_str != new_conn_str:
            has_changes = True
            reason.append("Perubahan pada alur koneksi (connections) terdeteksi")

        if current_wf.get("name") != new_name:
            has_changes = True
            reason.append("Perubahan pada nama workflow")

    # 6. Eksekusi Berdasarkan Hasil Deteksi
    if not has_changes:
        print("[INFO] ==========================================================")
        print("[INFO] ✅ TIDAK ADA PERUBAHAN pada workflow bot.")
        print("[INFO] ℹ️ Status alur kerja di n8n sudah AKTIF (PUBLISHED).")
        print("[INFO] ⏭️ Melewati proses sinkronisasi & publish (No restart needed).")
        print("[INFO] ==========================================================")
        sys.exit(0)

    print(f"[INFO] 🔄 Perubahan terdeteksi: {', '.join(reason)}.")
    print(f"[INFO] 📝 Memperbarui workflow di database (ID: {workflow_id}) dan mempublikasikan (active = true)...")

    new_version_id = str(uuid.uuid4())
    
    # Simpan nodes ke file sementara di VPS lalu masukkan via SQL aman
    tmp_nodes_path = "/tmp/n8n_sync_nodes.json"
    tmp_conn_path = "/tmp/n8n_sync_conn.json"

    with open(tmp_nodes_path, "w", encoding="utf-8") as f:
        json.dump(new_nodes, f)
    with open(tmp_conn_path, "w", encoding="utf-8") as f:
        json.dump(new_connections, f)

    subprocess.run(["docker", "cp", tmp_nodes_path, f"{container_name}:/tmp/n8n_sync_nodes.json"], check=True)
    subprocess.run(["docker", "cp", tmp_conn_path, f"{container_name}:/tmp/n8n_sync_conn.json"], check=True)

    escaped_name = new_name.replace("'", "''")

    sql_update = f"""
    UPDATE workflow_entity
    SET name = '{escaped_name}',
        nodes = pg_read_file('/tmp/n8n_sync_nodes.json')::json,
        connections = pg_read_file('/tmp/n8n_sync_conn.json')::json,
        active = true,
        "versionId" = '{new_version_id}',
        "updatedAt" = CURRENT_TIMESTAMP
    WHERE id = '{workflow_id}';

    -- Catat histori versi jika tabel workflow_history tersedia
    DO $$
    BEGIN
        IF EXISTS (SELECT FROM pg_tables WHERE schemaname = 'public' AND tablename = 'workflow_history') THEN
            INSERT INTO workflow_history ("versionId", "workflowId", nodes, connections, "authors", "createdAt", "updatedAt")
            VALUES (
                '{new_version_id}',
                '{workflow_id}',
                pg_read_file('/tmp/n8n_sync_nodes.json')::json,
                pg_read_file('/tmp/n8n_sync_conn.json')::json,
                'system_ci_cd',
                CURRENT_TIMESTAMP,
                CURRENT_TIMESTAMP
            )
            ON CONFLICT ("versionId") DO NOTHING;
        END IF;
    END $$;
    """

    run_psql_stdin(sql_update, db_user, db_name, container_name)
    print(f"[SUCCESS] Basis data diperbarui! VersionId baru: {new_version_id}")

    # 7. Restart container n8n agar webhook otomatis terdaftar ulang
    print("[INFO] 🔄 Merestart kontainer n8n agar webhook Telegram dimuat ulang...")
    subprocess.run(["docker", "compose", "restart", "n8n"], cwd=PROJECT_DIR, check=True)

    # Tunggu sebentar untuk kesiapan n8n
    print("[INFO] Menunggu inisialisasi n8n...")
    time.sleep(3)

    print("==================================================================")
    print("🚀 [SUCCESS] WORKFLOW BERHASIL DISINKRONKAN & OTOMATIS DIPUBLIKASIKAN!")
    print("🤖 Bot Telegram kini aktif dengan alur kerja terbaru.")
    print("==================================================================")

if __name__ == "__main__":
    main()
