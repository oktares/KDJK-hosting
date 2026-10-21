#!/usr/bin/env bash
# ==============================================================================
# Script Otomatisasi Instalasi n8n Self-Hosted dengan Docker, PostgreSQL & Caddy
# Target OS: Ubuntu 22.04 / 24.04 LTS atau Debian 12
# ==============================================================================

set -euo pipefail

# Warna terminal
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}=====================================================${NC}"
echo -e "${GREEN}   Installer Otomatis n8n Self-Hosted di VPS Linux   ${NC}"
echo -e "${BLUE}=====================================================${NC}"

# 1. Pastikan script dijalankan sebagai root / sudo
if [ "$EUID" -ne 0 ]; then
  echo -e "${RED}[ERROR] Script ini wajib dijalankan dengan hak akses root / sudo!${NC}"
  exit 1
fi

# 2. Input parameter konfigurasi dari user
read -rp "Masukkan Subdomain (contoh: n8n): " INPUT_SUBDOMAIN
read -rp "Masukkan Domain Utama (contoh: perusahaan.com): " INPUT_DOMAIN
read -rp "Masukkan Email untuk Sertifikat SSL Let's Encrypt: " INPUT_EMAIL
read -rp "Masukkan Google Gemini API Key [Tekan Enter untuk memakai default]: " INPUT_GEMINI_KEY

INPUT_SUBDOMAIN=${INPUT_SUBDOMAIN:-n8n}
INPUT_DOMAIN="${INPUT_DOMAIN#.}"
INPUT_GEMINI_KEY=${INPUT_GEMINI_KEY:-YOUR_GEMINI_API_KEY}
if [[ -z "$INPUT_DOMAIN" || -z "$INPUT_EMAIL" ]]; then
    echo -e "${RED}[ERROR] Domain dan Email tidak boleh kosong!${NC}"
    exit 1
fi

# 3. Update sistem operasi
echo -e "\n${YELLOW}[1/6] Memperbarui paket sistem operasi...${NC}"
apt-get update -y && apt-get upgrade -y
apt-get install -y curl wget git ufw htop ca-certificates gnupg lsb-release

# 4. Konfigurasi Firewall UFW
echo -e "\n${YELLOW}[2/6] Mengonfigurasi firewall UFW...${NC}"
ufw default deny incoming
ufw default allow outgoing
ufw allow 22/tcp comment 'SSH'
ufw allow 80/tcp comment 'HTTP'
ufw allow 443/tcp comment 'HTTPS'
ufw --force enable

# 5. Konfigurasi Swap Memory (2GB) jika belum ada
if [ ! -f /swapfile ]; then
    echo -e "\n${YELLOW}[3/6] Membuat 2GB Swap Memory untuk stabilitas server...${NC}"
    fallocate -l 2G /swapfile
    chmod 600 /swapfile
    mkswap /swapfile
    swapon /swapfile
    echo '/swapfile none swap sw 0 0' >> /etc/fstab
    sysctl vm.swappiness=10
    echo 'vm.swappiness=10' >> /etc/sysctl.conf
else
    echo -e "\n${GREEN}[INFO] Swap file sudah terdeteksi. Melewati pembuatan swap.${NC}"
fi

# 6. Install Docker Engine & Docker Compose
if ! command -v docker &> /dev/null; then
    echo -e "\n${YELLOW}[4/6] Menginstal Docker Engine & Docker Compose...${NC}"
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    rm -f get-docker.sh
    systemctl enable --now docker
else
    echo -e "\n${GREEN}[INFO] Docker sudah terinstal.${NC}"
fi

# 7. Generate Password & Encryption Key
INSTALL_DIR="/opt/n8n"
echo -e "\n${YELLOW}[5/6] Menyiapkan direktori aplikasi di ${INSTALL_DIR}...${NC}"
mkdir -p "${INSTALL_DIR}"
mkdir -p "${INSTALL_DIR}/local_files"
mkdir -p "${INSTALL_DIR}/backups"

RANDOM_PG_PASS=$(openssl rand -base64 16 | tr -dc 'a-zA-Z0-9' | head -c 16)
RANDOM_ENC_KEY=$(openssl rand -hex 24)

# Pertahankan kredensial lama jika .env sudah ada agar tidak terjadi mismatch encryption key
if [ -f "${INSTALL_DIR}/.env" ]; then
    EXISTING_ENC=$(grep -E '^N8N_ENCRYPTION_KEY=' "${INSTALL_DIR}/.env" | cut -d '=' -f2- | tr -d ' ' || true)
    EXISTING_PG=$(grep -E '^POSTGRES_PASSWORD=' "${INSTALL_DIR}/.env" | cut -d '=' -f2- | tr -d ' ' || true)
    [ -n "$EXISTING_ENC" ] && RANDOM_ENC_KEY="$EXISTING_ENC"
    [ -n "$EXISTING_PG" ] && RANDOM_PG_PASS="$EXISTING_PG"
fi

# Buat file .env
cat <<EOF > "${INSTALL_DIR}/.env"
SUBDOMAIN=${INPUT_SUBDOMAIN}
DOMAIN_NAME=${INPUT_DOMAIN}
SSL_EMAIL=${INPUT_EMAIL}
GENERIC_TIMEZONE=Asia/Jakarta

POSTGRES_USER=n8n_admin
POSTGRES_PASSWORD=${RANDOM_PG_PASS}
POSTGRES_DB=n8n_db

N8N_ENCRYPTION_KEY=${RANDOM_ENC_KEY}
N8N_PAYLOAD_SIZE_MAX=128
EXECUTIONS_DATA_PRUNE=true
EXECUTIONS_DATA_MAX_AGE=168
EXECUTIONS_DATA_PRUNE_MAX_COUNT=50000
N8N_LOG_LEVEL=info
N8N_DIAGNOSTICS_ENABLED=false

GEMINI_API_KEY=${INPUT_GEMINI_KEY}
EOF

# Salin docker-compose.yml, Caddyfile, scripts (termasuk init-db.sql), dan workflows
CURRENT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
mkdir -p "${INSTALL_DIR}/scripts"
mkdir -p "${INSTALL_DIR}/workflows"

if [ "${CURRENT_DIR}" != "${INSTALL_DIR}" ]; then
    [ -f "${CURRENT_DIR}/docker-compose.yml" ] && cp "${CURRENT_DIR}/docker-compose.yml" "${INSTALL_DIR}/"
    [ -f "${CURRENT_DIR}/Caddyfile" ] && cp "${CURRENT_DIR}/Caddyfile" "${INSTALL_DIR}/"
    [ -f "${CURRENT_DIR}/scripts/init-db.sql" ] && cp "${CURRENT_DIR}/scripts/init-db.sql" "${INSTALL_DIR}/scripts/"
    [ -f "${CURRENT_DIR}/scripts/backup-n8n.sh" ] && cp "${CURRENT_DIR}/scripts/backup-n8n.sh" "${INSTALL_DIR}/scripts/"
    [ -f "${CURRENT_DIR}/scripts/update-n8n.sh" ] && cp "${CURRENT_DIR}/scripts/update-n8n.sh" "${INSTALL_DIR}/scripts/"
    if [ -d "${CURRENT_DIR}/workflows" ]; then
        cp -r "${CURRENT_DIR}/workflows/"* "${INSTALL_DIR}/workflows/" || true
    fi
fi

chmod +x "${INSTALL_DIR}"/scripts/*.sh 2>/dev/null || true
if [ -f "${INSTALL_DIR}/workflows/personal-finance-bot.json" ]; then
    sed -i "s|YOUR_GEMINI_API_KEY|${INPUT_GEMINI_KEY}|g" "${INSTALL_DIR}/workflows/personal-finance-bot.json"
fi

# 8. Jalankan Container
echo -e "\n${YELLOW}[6/6] Menjalankan n8n, PostgreSQL, dan Caddy...${NC}"
cd "${INSTALL_DIR}"
docker compose pull
docker compose up -d

echo -e "\n${BLUE}=====================================================${NC}"
echo -e "${GREEN}   INSTALASI BERHASIL!                             ${NC}"
echo -e "${BLUE}=====================================================${NC}"
echo -e "Akses n8n Anda di URL: ${YELLOW}https://${INPUT_SUBDOMAIN}.${INPUT_DOMAIN}${NC}"
echo -e "Enkripsi Key n8n     : ${YELLOW}${RANDOM_ENC_KEY}${NC} (Wajib dicatat!)"
echo -e "Database Password    : ${YELLOW}${RANDOM_PG_PASS}${NC}"
echo -e "Folder Instalasi     : ${INSTALL_DIR}"
echo -e "Status Container     : Gunakan 'cd ${INSTALL_DIR} && docker compose ps'"
echo -e "${BLUE}=====================================================${NC}"
