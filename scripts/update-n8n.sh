#!/usr/bin/env bash
# ==============================================================================
# Script Otomatisasi Update n8n & Database ke Versi Terbaru (Safe Update)
# ==============================================================================

set -euo pipefail

INSTALL_DIR="/opt/n8n"

echo "[$(date)] Memulai proses update n8n..."
cd "${INSTALL_DIR}"

# 1. Jalankan backup terlebih dahulu sebelum update
if [ -f "${INSTALL_DIR}/scripts/backup-n8n.sh" ]; then
    echo "[INFO] Melakukan snapshot backup darurat..."
    bash "${INSTALL_DIR}/scripts/backup-n8n.sh"
fi

# 2. Tarik image Docker versi terbaru
echo "[INFO] Menarik image n8n & Caddy terbaru..."
docker compose pull

# 3. Restart container dengan image baru
echo "[INFO] Merestart container dengan versi terbaru..."
docker compose up -d

# 4. Bersihkan image usang (dangling images)
echo "[INFO] Menghapus cache image lama yang tidak terpakai..."
docker image prune -f

# 5. Smart Workflow Sync & Auto-Publish (Hanya reload/publish jika ada perubahan)
if [ -f "${INSTALL_DIR}/scripts/sync-workflow.py" ]; then
    echo "[INFO] Memeriksa sinkronisasi alur kerja bot..."
    python3 "${INSTALL_DIR}/scripts/sync-workflow.py"
fi

echo "[SUCCESS] Update n8n selesai! Periksa log dengan: docker compose logs -f n8n"
