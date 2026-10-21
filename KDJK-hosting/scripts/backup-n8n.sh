#!/usr/bin/env bash
# ==============================================================================
# Script Otomatisasi Backup Database PostgreSQL & Kunci Enkripsi n8n
# Retensi: Menyimpan data backup selama 14 hari terakhir
# ==============================================================================

set -euo pipefail

INSTALL_DIR="/opt/n8n"
BACKUP_DIR="${INSTALL_DIR}/backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
RETENTION_DAYS=14

# Buat direktori backup jika belum ada
mkdir -p "${BACKUP_DIR}"

echo "[$(date)] Memulai proses pencadangan (backup) n8n..."

# Load konfigurasi dari .env
if [ -f "${INSTALL_DIR}/.env" ]; then
    export $(grep -v '^#' "${INSTALL_DIR}/.env" | xargs)
else
    echo "[ERROR] File .env tidak ditemukan di ${INSTALL_DIR}!"
    exit 1
fi

# 1. Dump database PostgreSQL
BACKUP_SQL_FILE="${BACKUP_DIR}/n8n_db_${TIMESTAMP}.sql.gz"
echo "[INFO] Menjalankan pg_dump dari container PostgreSQL..."
docker exec n8n_postgres pg_dump -U "${POSTGRES_USER}" -d "${POSTGRES_DB}" | gzip > "${BACKUP_SQL_FILE}"

# 2. Backup file .env dan encryption key
BACKUP_ENV_FILE="${BACKUP_DIR}/n8n_env_${TIMESTAMP}.tar.gz"
echo "[INFO] Menyelamatkan file konfigurasi dan encryption key..."
tar -czf "${BACKUP_ENV_FILE}" -C "${INSTALL_DIR}" .env Caddyfile docker-compose.yml

# 3. Validasi hasil backup
if [ -s "${BACKUP_SQL_FILE}" ] && [ -s "${BACKUP_ENV_FILE}" ]; then
    echo "[SUCCESS] Backup berhasil disimpan:"
    echo "  - Database: ${BACKUP_SQL_FILE} ($(du -sh "${BACKUP_SQL_FILE}" | cut -f1))"
    echo "  - Config  : ${BACKUP_ENV_FILE} ($(du -sh "${BACKUP_ENV_FILE}" | cut -f1))"
else
    echo "[ERROR] File backup berukuran 0 byte! Periksa log database."
    exit 1
fi

# 4. Hapus file backup yang berusia lebih dari RETENTION_DAYS
echo "[INFO] Membersihkan backup lama yang berumur lebih dari ${RETENTION_DAYS} hari..."
find "${BACKUP_DIR}" -name "n8n_db_*.sql.gz" -mtime +"${RETENTION_DAYS}" -delete
find "${BACKUP_DIR}" -name "n8n_env_*.tar.gz" -mtime +"${RETENTION_DAYS}" -delete

echo "[$(date)] Proses backup selesai sempurna."
