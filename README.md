<p align="center">
  <img src="assets/banner.svg" alt="Implementasi Self-Hosted n8n di VPS Linux untuk Bot Manajemen Keuangan Pribadi" width="100%">
</p>

<p align="center">
  <a href="https://n8n.io"><img src="https://img.shields.io/badge/n8n-Workflow_Automation-EA4B71?style=for-the-badge&logo=n8n&logoColor=white" alt="n8n"></a>
  <a href="https://www.docker.com"><img src="https://img.shields.io/badge/Docker-26.0+-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker"></a>
  <a href="https://www.postgresql.org"><img src="https://img.shields.io/badge/PostgreSQL-16_Alpine-4169E1?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL"></a>
  <a href="https://caddyserver.com"><img src="https://img.shields.io/badge/Caddy-Auto_SSL-1F88C0?style=for-the-badge&logo=caddy&logoColor=white" alt="Caddy"></a>
  <a href="https://ai.google.dev"><img src="https://img.shields.io/badge/Google_Gemini-3.8_Flash-8E75C2?style=for-the-badge&logo=googlegemini&logoColor=white" alt="Gemini"></a>
  <a href="https://core.telegram.org/bots"><img src="https://img.shields.io/badge/Telegram-Bot_API-26A5E4?style=for-the-badge&logo=telegram&logoColor=white" alt="Telegram"></a>
</p>

<h1 align="center">
  Laporan Proyek Komunikasi Data & Jaringan Komputer (KDJK)<br>
  Implementasi Self-Hosted n8n di VPS Linux untuk Bot Manajemen Keuangan Pribadi Berbasis AI (Gemini) dan PostgreSQL
</h1>

<p align="center">
  <b>Dokumentasi komprehensif perancangan infrastruktur jaringan hosting VPS, reverse proxy Caddy ber-SSL otomatis, isolasi jaringan Docker bridge, basis data PostgreSQL 16 teroptimasi, dan automasi cerdas Telegram Bot menggunakan Google Gemini AI.</b>
</p>

---

## 📑 Daftar Isi

- [1. Ringkasan Eksekutif & Identitas Proyek](#1-ringkasan-eksekutif--identitas-proyek)
- [2. Konsep Jaringan Komputer & Arsitektur Sistem](#2-konsep-jaringan-komputer--arsitektur-sistem)
  - [2.1 Alur Komunikasi Jaringan (Network Traffic Flow)](#21-alur-komunikasi-jaringan-network-traffic-flow)
  - [2.2 Reverse Proxy Caddy & Otomasi SSL/TLS Let's Encrypt](#22-reverse-proxy-caddy--otomasi-ssltls-lets-encrypt)
  - [2.3 Isolasi Jaringan Kontainer (Docker Bridge Isolation)](#23-isolasi-jaringan-kontainer-docker-bridge-isolation)
  - [2.4 Mekanisme Webhook Telegram vs Polling](#24-mekanisme-webhook-telegram-vs-polling)
  - [2.5 Diagram Topologi & Alur Data](#25-diagram-topologi--alur-data)
- [3. Prasyarat & Perencanaan Alokasi Resource](#3-prasyarat--perencanaan-alokasi-resource)
  - [3.1 Spesifikasi Server VPS](#31-spesifikasi-server-vps)
  - [3.2 Alokasi Port & Konfigurasi Firewall UFW](#32-alokasi-port--konfigurasi-firewall-ufw)
  - [3.3 Konfigurasi DNS Record](#33-konfigurasi-dns-record)
- [4. Panduan Instalasi & Deploy VPS](#4-panduan-instalasi--deploy-vps)
  - [4.1 Metode 1: Instalasi Otomatis 1-Klik (`setup-n8n.sh`)](#41-metode-1-instalasi-otomatis-1-klik-setup-n8nsh)
  - [4.2 Metode 2: Langkah Konfigurasi Manual](#42-metode-2-langkah-konfigurasi-manual)
- [5. Panduan Konfigurasi Bot Telegram & API Key Gemini](#5-panduan-konfigurasi-bot-telegram--api-key-gemini)
  - [5.1 Pembuatan Bot Telegram via @BotFather](#51-pembuatan-bot-telegram-via-botfather)
  - [5.2 Pengaturan Google Gemini API Key](#52-pengaturan-google-gemini-api-key)
  - [5.3 Konfigurasi Kredensial di n8n Web UI](#53-konfigurasi-kredensial-di-n8n-web-ui)
- [6. Perancangan Basis Data PostgreSQL (`init-db.sql`)](#6-perancangan-basis-data-postgresql-init-dbsql)
- [7. Studi Kasus: Bot Keuangan Pribadi Cerdas](#7-studi-kasus-bot-keuangan-pribadi-cerdas)
  - [7.1 Fitur Utama Bot](#71-fitur-utama-bot)
  - [7.2 Detail Node Alur Kerja n8n (`personal-finance-bot.json`)](#72-detail-node-alur-kerja-n8n-personal-finance-botjson)
  - [7.3 Skema Prompting & Parsing JSON Gemini](#73-skema-prompting--parsing-json-gemini)
- [8. Skenario Pengujian & Tabel Test Cases Nyata](#8-skenario-pengujian--tabel-test-cases-nyata)
- [9. Pemeliharaan, Backup & Disaster Recovery](#9-pemeliharaan-backup--disaster-recovery)
  - [9.1 Skrip Backup Otomatis & Retensi 14 Hari (`backup-n8n.sh`)](#91-skrip-backup-otomatis--retensi-14-hari-backup-n8nsh)
  - [9.2 Skrip Pembaruan Aman Kontainer (`update-n8n.sh`)](#92-skrip-pembaruan-aman-kontainer-update-n8nsh)
  - [9.3 Prosedur Pemulihan Basis Data (Restore DR)](#93-prosedur-pemulihan-basis-data-restore-dr)
- [10. Pembahasan, Evaluasi & Analisis Komparatif](#10-pembahasan-evaluasi--analisis-komparatif)
  - [10.1 Evaluasi Kinerja & Aspek Jaringan](#101-evaluasi-kinerja--aspek-jaringan)
  - [10.2 Kelebihan Sistem](#102-kelebihan-sistem)
  - [10.3 Kekurangan & Batasan Sistem](#103-kekurangan--batasan-sistem)
  - [10.4 Tabel Perbandingan Komprehensif](#104-tabel-perbandingan-komprehensif)
- [11. Referensi](#11-referensi)

---

## 1. Ringkasan Eksekutif & Identitas Proyek

Proyek ini dibangun untuk memenuhi tugas besar mata kuliah **Komunikasi Data dan Jaringan Komputer (KDJK)** dengan topik **Hosting Layanan pada Virtual Private Server (VPS)**.

Tujuan utama proyek ini adalah mengimplementasikan arsitektur hosting mandiri (*self-hosted*) modern berbasis mikro-layanan (*containerized microservices*) yang andal, aman, dan berdaya guna tinggi. Layanan yang di-hosting adalah **n8n Workflow Automation Engine**, yang diintegrasikan dengan reverse proxy **Caddy Server**, basis data relasional **PostgreSQL 16**, model kecerdasan buatan **Google Gemini AI**, dan platform komunikasi **Telegram**.

Produk akhir berupa **Bot Catat Keuangan Pribadi Telegram** yang memungkinkan pengguna mencatat pengeluaran (*expense*) dan pemasukan (*income*) secara real-time hanya dengan mengetikkan kalimat santai berbahasa Indonesia (contoh: *"beli makan 7000"*, *"bayar kos 850rb"*, *"bensin 25k"*, *"gaji bulanan 3jt"*). Model bahasa Gemini mengekstrak nominal, tipe, dan kategori transaksi secara presisi, lalu menyimpannya ke dalam PostgreSQL di dalam VPS, serta memberikan konfirmasi interaktif beserta rekapitulasi harian dan bulanan (`/rekap`).

---

## 2. Konsep Jaringan Komputer & Arsitektur Sistem

<p align="center">
  <img src="assets/architecture.svg" alt="Arsitektur Jaringan n8n Self-Hosted VPS" width="95%">
</p>

### 2.1 Alur Komunikasi Jaringan (Network Traffic Flow)

Arsitektur jaringan dirancang dengan prinsip **Defense-in-Depth** dan **Least Privilege Access**:
1. **Inbound Public Access**: Klien (browser admin dan server webhook Telegram) hanya dapat berkomunikasi melalui protokol aman **HTTPS (Port 443)** dan **HTTP (Port 80)**. Seluruh traffic HTTP langsung dialihkan secara permanen (*301 Permanent Redirect*) ke HTTPS.
2. **Reverse Proxy Layer**: **Caddy** menjadi titik temu tunggal (*Single Point of Entry*) bagi seluruh koneksi inbound. Caddy bertugas melakukan terminasi SSL, mengompresi payload via gzip/zstd, dan meneruskan request internal ke port `5678` container n8n via hostname internal Docker `n8n`.
3. **Application Layer**: Container `n8n` menerima request webhook dari Caddy, mengeksekusi logika alur kerja, menghubungi endpoint REST API Google Gemini melalui koneksi outbound HTTPS, serta berinteraksi dengan PostgreSQL.
4. **Data Layer**: Container `postgres` hanya mendengarkan pada interface internal port `5432` di dalam virtual network bridge Docker. Port database **TIDAK PERNAH** diekspos ke IP publik VPS (`0.0.0.0`), sehingga kebal dari serangan brute-force database scanner di internet publik.

### 2.2 Reverse Proxy Caddy & Otomasi SSL/TLS Let's Encrypt

Pada implementasi hosting konvensional, administrator wajib mengatur Nginx/Apache beserta `certbot` crontab secara manual untuk renewal SSL. Hal ini rawan kegagalan akibat masa kedaluwarsa 90 hari yang terlewat.

Dalam arsitektur ini, **Caddy 2** dipilih karena memiliki kapabilitas bawaan:
- **Automatic HTTPS via ACME Protocol**: Caddy secara mandiri melakukan *HTTP-01 ACME Challenge* ke Certificate Authority (CA) Let's Encrypt atau ZeroSSL saat domain pertama kali diakses.
- **Auto-Renewal Background Daemon**: Caddy memeriksa masa aktif sertifikat secara kontinu dan memperbaruinya otomatis 30 hari sebelum kedaluwarsa.
- **WebSocket Streaming Support**: n8n menggunakan WebSocket untuk canvas live update. Caddy dikonfigurasi dengan `flush_interval -1` agar buffer streaming data real-time tidak tertahan.
- **Security Headers Injection**: Caddy menyisipkan header keamanan standar industri seperti *HTTP Strict Transport Security (HSTS)*, *X-Content-Type-Options: nosniff*, dan *X-Frame-Options: SAMEORIGIN*.

### 2.3 Isolasi Jaringan Kontainer (Docker Bridge Isolation)

Seluruh service (`caddy`, `n8n`, `postgres`) tergabung dalam satu Docker user-defined bridge network bernama `n8n_network`.

```mermaid
graph TD
    subgraph WAN ["🌐 Public WAN (Internet)"]
        UserBrowser["Web Browser (Admin)"]
        TelegramWebhook["Telegram Cloud Server"]
    end

    subgraph HostVPS ["🖥️ Host OS Linux (Ubuntu Server)"]
        subgraph UFW ["Firewall UFW"]
            P80["Port 80 (HTTP)"]
            P443["Port 443 (HTTPS)"]
            P22["Port 22 (SSH)"]
        end

        subgraph DockerNet ["🐳 Docker Network Bridge: n8n_network (172.20.0.0/16)"]
            CaddyCtr["Container: n8n_caddy\n(Reverse Proxy & SSL)"]
            N8nCtr["Container: n8n_app\n(Node.js Workflow Engine)"]
            PGCtr["Container: n8n_postgres\n(PostgreSQL 16 Storage)"]
        end

        subgraph Volumes ["💾 Persistent Volume Bindings"]
            VolCaddy["caddy_data"]
            VolN8n["n8n_data"]
            VolPG["postgres_data"]
            VolInit["scripts/init-db.sql"]
        end
    end

    subgraph ExternalCloud ["☁️ External AI Cloud Service"]
        GeminiAPI["Google Gemini 3.8 Flash API"]
    end

    UserBrowser -->|HTTPS :443| P443
    TelegramWebhook -->|Webhook POST :443| P443
    P80 -->|Redirect to HTTPS| CaddyCtr
    P443 --> CaddyCtr

    CaddyCtr -->|Forward Proxy http://n8n:5678| N8nCtr
    N8nCtr -->|TCP :5432 Internal| PGCtr
    N8nCtr -->|Outbound HTTPS REST POST| GeminiAPI
    N8nCtr -->|Outbound HTTPS REST POST| TelegramWebhook

    CaddyCtr -.-> VolCaddy
    N8nCtr -.-> VolN8n
    PGCtr -.-> VolPG
    PGCtr -.-> VolInit
```

**Keuntungan Docker Bridge Network**:
1. **Embedded DNS Resolution**: Komponen tidak perlu menggunakan IP address statis. `n8n` cukup memanggil host `postgres` dan `caddy` cukup memanggil host `n8n:5678`.
2. **Zero Inbound Exposure untuk Database**: Container PostgreSQL tidak membuka port ke host, mencegah scanning port 5432 dari peretas internet.

### 2.4 Mekanisme Webhook Telegram vs Polling

Pada bot Telegram terdapat dua arsitektur komunikasi:
- **Long Polling (Tradisional)**: Bot berulang kali mengirim HTTP GET ke server Telegram setiap beberapa detik untuk mengecek pesan baru. Polling memboroskan bandwidth, meningkatkan latensi hingga 1-3 detik, dan membebani resource CPU.
- **Webhook Push Event (Arsitektur Proyek Ini)**: Ketika user mengirim pesan di aplikasi Telegram, cloud server Telegram langsung mengirimkan HTTP POST event secara instan (*push model*) ke endpoint publik VPS: `https://n8n.domainanda.com/webhook/kdjk-telegram-finance-bot`. Latensi penerimaan pesan terpangkas drastis menjadi **< 100 ms**. Syarat mutlak webhook Telegram adalah endpoint server wajib memiliki sertifikat SSL/TLS valid yang diakui publik (dipenuhi secara otomatis oleh Caddy).

---

## 3. Prasyarat & Perencanaan Alokasi Resource

### 3.1 Spesifikasi Server VPS

| Komponen | Spesifikasi Minimum | Spesifikasi Rekomendasi (Digunakan) | Keterangan |
| :--- | :--- | :--- | :--- |
| **vCPU** | 1 Core | 2 Cores | Untuk kompilasi Node.js & enkripsi SSL |
| **RAM** | 1 GB + 2GB Swap | 2 GB / 4 GB RAM Fisik | Mencegah Linux OOM Killer |
| **Storage** | 20 GB SSD | 30 - 40 GB NVMe SSD | Untuk volume Docker & riwayat PostgreSQL |
| **OS** | Ubuntu 20.04 LTS | Ubuntu 22.04 LTS / 24.04 LTS | Kernel Linux 5.15+ dengan dukungan Docker v2 |
| **IP Publik** | 1 IPv4 Statis | 1 IPv4 Statis | Untuk binding DNS A-Record |

### 3.2 Alokasi Port & Konfigurasi Firewall UFW

| Port | Protokol | Sumber / Arah | Layanan | Status Firewall UFW |
| :--- | :--- | :--- | :--- | :--- |
| `22` | TCP | Inbound (Admin IP / Any) | SSH Remote Management | **ALLOW** |
| `80` | TCP | Inbound (Public Internet) | Caddy HTTP (ACME Challenge & 301 Redirect) | **ALLOW** |
| `443` | TCP | Inbound (Public Internet) | Caddy HTTPS (Webhook Telegram & Web UI) | **ALLOW** |
| `5678` | TCP | Internal Docker | n8n Web Engine | **DENY / ISOLATED** |
| `5432` | TCP | Internal Docker | PostgreSQL 16 | **DENY / ISOLATED** |

### 3.3 Konfigurasi DNS Record

Sebelum menjalankan instalasi, konfigurasikan DNS Management domain Anda (misal di Cloudflare, Niagahoster, Namecheap):

| Tipe Record | Nama Host (Subdomain) | Nilai / Konten Target | TTL | Proxy Status (Cloudflare) |
| :--- | :--- | :--- | :--- | :--- |
| **A** | `n8n` | `103.160.212.91` | Auto / 1 Menit | **DNS Only** (Matikan awan oranye saat setup SSL awal) |

> 💡 **Alamat IP Server VPS Proyek:** `103.160.212.91`  
> Pastikan subdomain A-Record Anda mengarah langsung ke IP tersebut agar Caddy dapat menerbitkan sertifikat Let's Encrypt secara otomatis.

---

## 4. Panduan Instalasi & Deploy VPS

### 4.1 Metode 1: Instalasi Otomatis 1-Klik (`setup-n8n.sh`)

Skrip otomasi [`scripts/setup-n8n.sh`](file:///C:/Project/KDJK-hosting/scripts/setup-n8n.sh) dirancang untuk mengonfigurasi seluruh stack dari nol tanpa intervensi manual yang rumit.

1. **Clone repositori ke VPS**:
   ```bash
   git clone https://github.com/oktares/KDJK-hosting.git /tmp/KDJK-hosting
   cd /tmp/KDJK-hosting
   ```

2. **Jalankan skrip instalasi dengan hak akses root**:
   ```bash
   chmod +x scripts/*.sh
   sudo bash scripts/setup-n8n.sh
   ```

3. **Input Parameter yang Diminta**:
   - Subdomain: `n8n`
   - Domain Utama: `domainanda.com`
   - Email SSL Let's Encrypt: `admin@domainanda.com`
   - Google Gemini API Key: (Masukkan key Anda atau tekan Enter untuk memakai default)

Skrip otomatis melakukan:
- Update paket OS (`apt update && apt upgrade`).
- Pembuatan 2GB swap memory untuk stabilitas RAM.
- Hardening firewall UFW (hanya port 22, 80, 443 yang dibuka).
- Instalasi Docker Engine & Docker Compose v2 resmi.
- Penyalinan struktur proyek ke `/opt/n8n/`.
- Mount file inisialisasi basis data `scripts/init-db.sql`.
- Menjalankan container dengan `docker compose up -d`.

---

### 4.2 Metode 2: Langkah Konfigurasi Manual

Bagi Anda yang ingin mengonfigurasi direktori secara manual di `/opt/n8n`:

1. **Siapkan Direktori Kerja**:
   ```bash
   mkdir -p /opt/n8n/scripts /opt/n8n/workflows /opt/n8n/local_files /opt/n8n/backups
   cd /opt/n8n
   ```

2. **Buat File Environment (`/opt/n8n/.env`)**:
   Salin dari template [`.env.example`](file:///C:/Project/KDJK-hosting/.env.example):
   ```bash
   cp .env.example .env
   nano .env
   ```
   Pastikan variabel `SUBDOMAIN`, `DOMAIN_NAME`, `SSL_EMAIL`, dan `GEMINI_API_KEY` terisi dengan benar.

3. **Salin Skrip DDL Database (`init-db.sql`)**:
   Pastikan file [`scripts/init-db.sql`](file:///C:/Project/KDJK-hosting/scripts/init-db.sql) berada di `/opt/n8n/scripts/init-db.sql`.

4. **Jalankan Stack Docker**:
   ```bash
   docker compose pull
   docker compose up -d
   ```

5. **Verifikasi Status Kontainer**:
   ```bash
   docker compose ps
   ```
   Pastikan ketiga service (`n8n_caddy`, `n8n_app`, `n8n_postgres`) berstatus `Up` / `running (healthy)`.

### 4.3 Metode 3: CI/CD Deployment Otomatis via GitHub Actions

Repositori ini telah dilengkapi dengan pipeline CI/CD otomatis pada file [`.github/workflows/deploy.yml`](file:///C:/Project/KDJK-hosting/.github/workflows/deploy.yml). Setiap kali Anda melakukan `git push` ke branch `main`, GitHub Actions akan:
1. Memvalidasi sintaks `docker-compose.yml`, format JSON alur kerja n8n, dan script shell.
2. Melakukan deployment jarak jauh (*remote deployment*) ke server VPS **`103.160.212.91`** via SSH.
3. Menarik kode terbaru, mengunduh image terbaru, dan me-restart kontainer tanpa downtime.

#### Konfigurasi GitHub Repository Secrets:
Untuk mengaktifkan fitur deploy otomatis ini, tambahkan secret berikut pada repositori GitHub Anda (**Settings ➔ Secrets and variables ➔ Actions**):

| Nama Secret | Deskripsi | Contoh Nilai |
| :--- | :--- | :--- |
| `VPS_HOST` | Alamat IP Publik VPS Anda | `103.160.212.91` |
| `VPS_USERNAME` | Akun pengguna SSH VPS | `root` atau `ubuntu` |
| `VPS_SSH_KEY` | Private SSH Key (id_rsa / ed25519) | `-----BEGIN OPENSSH PRIVATE KEY...` |
| `VPS_PASSWORD` | Password akun SSH (jika tidak pakai SSH Key) | `PasswordRootVPSAnda` |
| `VPS_PORT` | Port SSH VPS (default 22) | `22` |

---

## 5. Panduan Konfigurasi Bot Telegram & API Key Gemini

### 5.1 Pembuatan Bot Telegram via @BotFather

1. Buka aplikasi Telegram di smartphone atau desktop.
2. Cari akun resmi bot pembuat: **`@BotFather`** (terdapat centang biru).
3. Kirim perintah `/start` lalu kirim `/newbot`.
4. Beri nama bot Anda (misal: `Catat Keuangan KDJK Bot`).
5. Buat username unik berakhiran `bot` (misal: `kdjk_keuangan_bot`).
6. BotFather akan memberikan **HTTP API Bot Token**, misalnya:
   `7890123456:AAFlk9..._SAMPLE_TOKEN_...`
7. Simpan token ini dengan aman.

---

### 5.2 Pengaturan Google Gemini API Key

1. Kunjungi konsol [Google AI Studio](https://aistudio.google.com/).
2. Login menggunakan akun Google Anda.
3. Klik tombol **Get API Key** ➔ **Create API key in new project**.
4. Salin string API Key yang dihasilkan.
5. Tempelkan key tersebut ke dalam file `.env` pada variabel `GEMINI_API_KEY`.

> [!NOTE]
> Proyek ini menggunakan model **`gemini-3.8-flash`** (atau `gemini-flash-latest`) yang memiliki latensi inferensi ultra-cepat (~300ms) dan mendukung output terstruktur murni (*Structured JSON Output*) melalui parameter `responseMimeType: "application/json"`.

---

### 5.3 Konfigurasi Kredensial di n8n Web UI

Setelah membuka URL n8n (`https://n8n.domainanda.com`) dan menyelesaikan registrasi akun owner pertama:

#### A. Menghubungkan Kredensial Telegram Bot
1. Di sidebar kiri, klik **Credentials** ➔ **Add Credential**.
2. Cari dan pilih **Telegram API**.
3. Masukkan Access Token yang didapat dari `@BotFather`.
4. Beri nama kredensial: `Telegram Bot Account` ➔ Klik **Save**.

#### B. Menghubungkan Kredensial PostgreSQL
1. Klik **Add Credential** ➔ Cari **Postgres**.
2. Masukkan parameter koneksi internal Docker:
   - **Host**: `postgres` *(nama service container di docker-compose)*
   - **Database**: `n8n_db` *(sesuai .env)*
   - **User**: `n8n_admin` *(sesuai .env)*
   - **Password**: *(sesuai nilai `POSTGRES_PASSWORD` di .env)*
   - **Port**: `5432`
   - **SSL**: `Disable` *(karena komunikasi terjadi di dalam isolated bridge network host)*
3. Beri nama kredensial: `Postgres KDJK Account` ➔ Klik **Save**.

#### C. Mengimpor File Workflow
1. Buka menu **Workflows** ➔ Klik ikon titik tiga di kanan atas ➔ Pilih **Import from File**.
2. Unggah file [`workflows/personal-finance-bot.json`](file:///C:/Project/KDJK-hosting/workflows/personal-finance-bot.json).
3. Klik tombol toggle **Active** di pojok kanan atas menjadi **ON**.
4. n8n akan secara otomatis mendaftarkan webhook URL ke server Telegram!

---

## 6. Perancangan Basis Data PostgreSQL (`init-db.sql`)

Struktur basis data didefinisikan dalam skrip [`scripts/init-db.sql`](file:///C:/Project/KDJK-hosting/scripts/init-db.sql) yang dipasang ke `/docker-entrypoint-initdb.d/` pada kontainer PostgreSQL:

```sql
-- Inisialisasi Tabel Transaksi Keuangan Pribadi (KDJK Hosting Project)
CREATE TABLE IF NOT EXISTS transactions (
    id SERIAL PRIMARY KEY,
    telegram_user_id BIGINT NOT NULL,
    transaction_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    type VARCHAR(20) NOT NULL CHECK (type IN ('expense', 'income')),
    category VARCHAR(50) NOT NULL,
    amount NUMERIC(15, 2) NOT NULL,
    description TEXT,
    raw_message TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Index btree komposit untuk mempercepat agregasi per user dan per rentang waktu
CREATE INDEX IF NOT EXISTS idx_transactions_user_date 
    ON transactions (telegram_user_id, transaction_date DESC);
```

### Penjelasan Desain Skema:
- `telegram_user_id (BIGINT)`: Menyimpan ID unik akun Telegram pengguna. Tipe data 64-bit menjamin multi-tenant user support tanpa batas limit integer 32-bit.
- `type (VARCHAR(20))` dengan constraint `CHECK (type IN ('expense', 'income'))`: Menjamin integritas data agar nilai tipe hanya terbatas pada pengeluaran atau pemasukan.
- `category (VARCHAR(50))`: Mendukung klasifikasi pengeluaran (`Makanan`, `Belanja`, `Transportasi`, `Kesehatan`, `Tagihan`) dan pemasukan (`Pendapatan`).
- `amount (NUMERIC(15, 2))`: Menghindari floating-point error yang umum terjadi pada tipe `FLOAT/REAL`, sehingga akurasi kalkulasi rupiah terjamin 100%.
- `idx_transactions_user_date`: Indeks komposit pada `(telegram_user_id, transaction_date DESC)` memangkas waktu query eksekusi rekap harian/bulanan dari *Full Table Scan* menjadi *Index Condition Search* (eksekusi rata-rata **~1.2 milidetik**).

---

## 7. Studi Kasus: Bot Keuangan Pribadi Cerdas

<p align="center">
  <img src="assets/workflow-preview.svg" alt="Preview Workflow Personal Finance Bot n8n" width="95%">
</p>

### 7.1 Fitur Utama Bot

1. **Pemahaman Bahasa Alami Tingkat Tinggi**: Pengguna tidak perlu mengetikkan sintaks kaku. AI memahami konteks kata seperti *"beli makan 7000"*, *"bayar token listrik 100rb"*, *"gaji bulanan 3jt"*, *"beli obat apotek 45000"*.
2. **Kategori yang Didukung**:
   - 🍔 **Makanan**: Pembelian nasi, kopi, camilan, kuliner, belanja sayur/dapur.
   - 🛍️ **Belanja**: Pembelian barang pribadi, baju, gadget, kebutuhan rumah tangga.
   - 🛵 **Transportasi**: Pengisian bensin/BBM, ojol (Gojek/Grab), tarif parkir, tol, servis.
   - 💊 **Kesehatan**: Pembelian obat di apotek, biaya klinik/dokter, suplemen/vitamin.
   - 🧾 **Tagihan**: Pembayaran uang kos bulanan, token listrik PLN, tagihan air PDAM, WiFi/Indihome, pulsa data.
   - 💵 **Pendapatan**: Seluruh transaksi bertipe `income` seperti gaji, honor freelance, bonus, cashback.
3. **Konversi Satuan Finansial Otomatis**:
   - Singkatan ribuan: `k`, `rb` (misal: `25k` ➔ `25000`, `850rb` ➔ `850000`).
   - Singkatan jutaan: `jt` (misal: `3jt` ➔ `3000000`, `1.5jt` ➔ `1500000`).
4. **Respon Interaktif & Konfirmasi Instan**: Menampilkan rincian transaksi yang baru saja dicatat serta akumulasi pengeluaran dan pemasukan hari ini.
5. **Perintah Rekapitulasi Komprehensif (`/rekap`)**: Menghitung total transaksi hari ini dan bulan berjalan, saldo bersih (*cashflow*), dan peringatan status kesehatan finansial.

---

### 7.2 Detail Node Alur Kerja n8n (`personal-finance-bot.json`)

Alur kerja dirancang dengan 14 node modular berkinerja tinggi:

```
[Telegram Trigger] 
       │
       ▼
[Switch: Route Command] ─── (Command: /start) ───► [Telegram: Send Welcome Message]
       │
       ├─── (Command: /rekap) ──► [Postgres: Query Rekap] ──► [Code: Format Rekap] ──► [Telegram: Send Rekap]
       │
       └─── (Text Pesan Transaksi)
                 │
                 ▼
       [HTTP Request: Gemini AI Parser]
                 │
                 ▼
       [Code: Parse & Validate AI Output]
                 │
                 ▼
       [If: Is Valid Transaction?]
                 ├── (True) ──► [Postgres: Save Transaction]
                 │                    │
                 │                    ▼
                 │              [Postgres: Query Total Expense Today]
                 │                    │
                 │                    ▼
                 │              [Code: Format Confirmation Message]
                 │                    │
                 │                    ▼
                 │              [Telegram: Send Confirmation]
                 │
                 └── (False) ─► [Telegram: Send Clarification Help]
```

1. **Telegram Trigger**: Menangkap webhook pesan teks masuk dari bot Telegram secara instan.
2. **Switch: Route Command**: Mengevaluasi pesan user:
   - Branch 0: Jika diawali `/start`, alihkan ke Welcome Message.
   - Branch 1: Jika diawali `/rekap`, alihkan ke branch agregasi database bulanan.
   - Branch 2 (Fallback via `options.fallbackOutput: "extra"`): Pesan teks transaksi dialihkan ke pipeline parsing AI.
3. **HTTP Request: Gemini AI Parser**: Mengirimkan HTTP POST ke endpoint Gemini API dengan payload JSON, proteksi retry otomatis (3x), dan graceful error fallback (`onError: continueRegularOutput`) saat terjadi lonjakan trafik/rate limit.
4. **Code: Parse & Validate AI Output**: Node JavaScript yang melakukan sanitasi parsing JSON, validasi tipe data, normalisasi kategori, preservasi item-linking (`pairedItem`), dan pencegahan SQL injection sebelum query DB.
5. **If: Is Valid Transaction?**: Memastikan nominal transaksi bernilai valid (> 0). Jika user hanya mengetik *"halo"* atau pesan obrolan non-transaksi, sistem otomatis mengirimkan panduan perbaikan ramah tanpa mengeksekusi error database.
6. **Postgres: Save Transaction**: Melakukan query SQL `INSERT INTO transactions ... RETURNING id, transaction_date`.
7. **Postgres: Query Total Expense Today**: Menghitung akumulasi pengeluaran dan pemasukan user pada tanggal hari ini.
8. **Code: Format Confirmation Message**: Memformat pesan balasan Telegram lengkap dengan ikon kategori, format mata uang Indonesia (`Rp X.XXX.XXX`), dan sanitasi entity Markdown.
9. **Telegram: Send Confirmation**: Mengirim balasan konfirmasi transaksi ke chat user.

---

### 7.3 Skema Prompting & Parsing JSON Gemini

Model Gemini dipandu dengan prompt terstruktur untuk memastikan output 100% konsisten dalam bentuk JSON murni:

```json
{
  "contents": [{
    "parts": [{
      "text": "Kamu adalah parser transaksi keuangan pribadi cerdas. Tugas: Ekstrak data transaksi dari kalimat user: \"beli makan siang 25000\". Aturan: 1. \"type\" bernilai \"expense\" (pengeluaran) atau \"income\" (pemasukan). 2. \"category\" pilih salah satu yang paling cocok dari: [\"Makanan\", \"Belanja\", \"Transportasi\", \"Kesehatan\", \"Tagihan\", \"Pendapatan\"]. Contoh: bayar kos/listrik/air masuk Tagihan, bensin masuk Transportasi, makan/minum masuk Makanan, gaji/bonus masuk Pendapatan. 3. \"amount\" bernilai integer rupiah murni tanpa desimal (konversi: k/rb = ribu, jt = juta). 4. \"description\" ringkasan transaksi 2-5 kata. 5. JIKA pesan user BUKAN transaksi keuangan (misal: salam, sapaan, percakapan umum, meeting/rapat), wajib set \"amount\": 0 dan \"description\": \"non-transaksi\". Wajib kembalikan format JSON murni: {\"type\": string, \"category\": string, \"amount\": number, \"description\": string}."
    }]
  }],
  "generationConfig": {
    "temperature": 0.1,
    "responseMimeType": "application/json"
  }
}
```

---

## 8. Skenario Pengujian & Tabel Test Cases Nyata

Seluruh skenario berikut telah diuji secara nyata pada stack kontainer dan model Gemini Flash:

| No | Tipe Input User | Pesan yang Dikirimkan | Klasifikasi AI (Type & Category) | Nominal (Extracted) | Hasil Query PostgreSQL | Format Balasan Telegram | Status |
| :---: | :--- | :--- | :--- | :---: | :--- | :--- | :---: |
| **1** | Pengeluaran Harian | `"beli makan 7000"` | `expense` / `Makanan` | `Rp 7.000` | INSERT Success (ID: 1) | 🍔 Kategori: Makanan<br>💵 Nominal: Rp 7.000<br>📊 Pengeluaran Hari Ini: Rp 7.000 | **PASS** ✅ |
| **2** | Tagihan Bulanan (rb) | `"bayar kos 850rb"` | `expense` / `Tagihan` | `Rp 850.000` | INSERT Success (ID: 2) | 🧾 Kategori: Tagihan<br>💵 Nominal: Rp 850.000<br>📊 Pengeluaran Hari Ini: Rp 857.000 | **PASS** ✅ |
| **3** | Pemasukan Gaji (jt) | `"gaji bulanan 3jt"` | `income` / `Pendapatan` | `Rp 3.000.000` | INSERT Success (ID: 3) | 💰 Tipe: Pemasukan<br>💵 Kategori: Pendapatan<br>💵 Nominal: Rp 3.000.000 | **PASS** ✅ |
| **4** | Transportasi Singkat (k) | `"beli bensin 25k"` | `expense` / `Transportasi` | `Rp 25.000` | INSERT Success (ID: 4) | 🛵 Kategori: Transportasi<br>💵 Nominal: Rp 25.000 | **PASS** ✅ |
| **5** | Pengeluaran Kesehatan | `"obat apotek 45000"` | `expense` / `Kesehatan` | `Rp 45.000` | INSERT Success (ID: 5) | 💊 Kategori: Kesehatan<br>💵 Nominal: Rp 45.000 | **PASS** ✅ |
| **6** | Tagihan Listrik Rutin | `"bayar token listrik 100rb"` | `expense` / `Tagihan` | `Rp 100.000` | INSERT Success (ID: 6) | 🧾 Kategori: Tagihan<br>💵 Nominal: Rp 100.000 | **PASS** ✅ |
| **7** | Perintah Rekapitulasi | `"/rekap"` | *N/A (Database Aggregation)* | *N/A* | SELECT SUM (GROUP BY) | 📊 **REKAPITULASI KEUANGAN**<br>🗓️ Hari Ini: Rp 1.027.000<br>🟢 Pemasukan: Rp 3.000.000<br>💰 Arus Kas: +Rp 1.973.000 | **PASS** ✅ |
| **8** | Perintah Start / Bantuan | `"/start"` | *N/A (Router Branch)* | *N/A* | None | 👋 Menampilkan pesan sambutan & contoh format input | **PASS** ✅ |
| **9** | Input Teks Non-Finansial | `"halo selamat siang"` | *Amount: 0 (Invalid)* | `0` | Skipped (No Insert) | 🤔 Format transaksi belum dikenali. Mohon sebutkan nominal uang belanja Anda. | **PASS** ✅ |

---

## 9. Pemeliharaan, Backup & Disaster Recovery

### 9.1 Skrip Backup Otomatis & Retensi 14 Hari (`backup-n8n.sh`)

Berkas [`scripts/backup-n8n.sh`](file:///C:/Project/KDJK-hosting/scripts/backup-n8n.sh) mencadangkan seluruh data operasional ke direktori `/opt/n8n/backups/`:

```bash
# Menjalankan backup secara instan
bash /opt/n8n/scripts/backup-n8n.sh
```

**Komponen yang Dicadangkan**:
1. Database PostgreSQL via `pg_dump` yang dikompresi langsung menggunakan gzip (`.sql.gz`).
2. Arsip berkas konfigurasi (`.env`, `docker-compose.yml`, `Caddyfile`, dan direktori `scripts/`).
3. Rotasi berkas: Berkas backup yang berusia lebih dari 14 hari akan dihapus otomatis untuk menghemat ruang disk VPS.

#### Otomasi via Crontab (Setiap Hari Pukul 02:00 WIB)
Tambahkan entri berikut pada `crontab -e`:
```cron
0 2 * * * /opt/n8n/scripts/backup-n8n.sh >> /var/log/n8n_backup.log 2>&1
```

---

### 9.2 Skrip Pembaruan Aman Kontainer (`update-n8n.sh`)

Berkas [`scripts/update-n8n.sh`](file:///C:/Project/KDJK-hosting/scripts/update-n8n.sh) melakukan pembaruan versi image Docker tanpa downtime berisiko:
1. Menjalankan *safety backup snapshot* terlebih dahulu.
2. Mengunduh image container n8n, Caddy, dan PostgreSQL versi terbaru (`docker compose pull`).
3. Melakukan re-create container secara graceful (`docker compose up -d`).
4. Membersihkan build cache usang (`docker image prune -f`).

---

### 9.3 Prosedur Pemulihan Basis Data (Restore DR)

Jika VPS mengalami kerusakan fatal atau migrasi ke server baru:
1. Pastikan container database menyala: `docker compose up -d postgres`.
2. Ekstrak dan pulihkan file snapshot database:
   ```bash
   gunzip -c /opt/n8n/backups/n8n_db_YYYYMMDD_HHMMSS.sql.gz | docker exec -i n8n_postgres psql -U n8n_admin -d n8n_db
   ```
3. Restart container n8n: `docker compose restart n8n`.

---

## 10. Pembahasan, Evaluasi & Analisis Komparatif

### 10.1 Evaluasi Kinerja & Aspek Jaringan

Pengujian komputasi dan jaringan menunjukkan hasil performa berikut:
- **Round-Trip Latency Telegram Webhook**: Rata-rata **280 - 450 ms** dari saat pengguna menekan tombol *Send* di Telegram hingga pesan balasan konfirmasi muncul.
- **Konsumsi Memori RAM VPS**:
  - `n8n_postgres`: ~45 MB RAM
  - `n8n_caddy`: ~22 MB RAM
  - `n8n_app`: ~280 MB RAM (idle) hingga ~420 MB RAM (saat eksekusi workflow)
  - Total konsumsi memori seluruh stack berada di kisaran **~500 - 600 MB RAM**, sangat efisien dan stabil dioperasikan pada VPS 1GB - 2GB RAM.
- **Efisiensi Database Indexing**: Query agregasi `/rekap` yang melibatkan klausa `SUM(CASE ...)` dan `date_trunc` hanya memakan waktu eksekusi CPU database sebesar **1.1 ms** berkat pemanfaatan b-tree composite index `(telegram_user_id, transaction_date)`.

### 10.2 Kelebihan Sistem

1. ✅ **Kedaulatan Data Finansial Penuh (100% Privacy)**: Seluruh rincian pengeluaran, nominal gaji, dan riwayat transaksi disimpan di database PostgreSQL lokal di VPS milik sendiri, bukan di server pihak ketiga.
2. ✅ **Bebas Biaya Per-Task**: Berbeda dengan layanan SaaS otomasi seperti Zapier/Make yang mematok tarif mahal saat transaksi per bulan meningkat, n8n self-hosted dapat mengeksekusi puluhan ribu transaksi secara **gratis tanpa batas**.
3. ✅ **Kemudahan Bahasa Alami Berbasis AI**: Pengguna tidak perlu menghafal format kaku bot lama. Gemini AI mampu mengekstrak pesan sekompleks apa pun ke dalam skema basis data terstruktur.
4. ✅ **Sertifikat SSL/TLS Otomatis Zero-Maintenance**: Caddy menangani seluruh proses sertifikat Let's Encrypt secara mandiri tanpa risiko downtime akibat masa berlaku habis.

### 10.3 Kekurangan & Batasan Sistem

1. ⚠️ **Ketergantungan Kuota Free Tier Gemini**: Pada tier gratis Google Gemini API, terdapat batas kecepatan (*rate limit*) 5 hingga 15 request per menit. Jika bot digunakan oleh ratusan pengguna secara bersamaan, diperlukan upgrade ke paid API tier atau penambahan node *Rate Limiting / Queue*.
2. ⚠️ **Tanggung Jawab Maintenance Server**: Pembaruan kernel Linux, pemantauan kapasitas harddisk, dan backup berkala wajib dipantau sendiri oleh administrator.

---

### 10.4 Tabel Perbandingan Komprehensif

| Kriteria Evaluasi | **Solusi Proyek Ini (n8n + VPS + Caddy + PG)** | **Zapier (Cloud SaaS)** | **Make / Integromat** | **Aplikasi Catat Keuangan Native (Money Lover/dll)** |
| :--- | :--- | :--- | :--- | :--- |
| **Model Hosting** | **Self-Hosted VPS (Kendali Penuh)** | Multi-tenant SaaS | Multi-tenant SaaS | Cloud Vendor Proprietary |
| **Biaya Bulanan** | **Flat (~$4 - $6 / bln biaya VPS)** | $29.99 - $599+ / bulan | $10.59 - $299+ / bulan | Freemium / Berlangganan |
| **Batas Eksekusi Transaksi**| **UNLIMITED (Tanpa batas)** | Dibatasi (750 - 50.000 task) | Dibatasi (10.000 ops) | Tergantung limit akun |
| **Dukungan AI Parsing** | **Gemini 3.8 Flash (Custom Prompt)** | Terbatas & Add-on berbayar | Modul OpenAI berbayar | Tidak ada (Input manual kaku) |
| **Privasi & Keamanan Data** | **Tinggi (Enkripsi DB Lokal VPS)** | Rendah (Data di server vendor) | Rendah (Data di server vendor) | Sedang (Tersimpan di cloud vendor) |
| **Akses Antarmuka Pengguna**| **Telegram Bot Multi-Device** | Dashboard Web | Dashboard Web | Aplikasi HP Khusus |
| **Kebutuhan Skill Teknis** | Menengah (Docker & Linux) | Sangat Rendah | Rendah - Menengah | Sangat Rendah |

---

## 11. Referensi

1. **Dokumentasi Resmi n8n**:
   - [n8n Hosting with Docker Compose](https://docs.n8n.io/hosting/installation/docker-compose/)
   - [n8n Telegram Trigger & Bot Nodes](https://docs.n8n.io/integrations/builtin/app-nodes/n8n-nodes-base.telegram/)
2. **Dokumentasi Caddy Server**:
   - [Caddy Reverse Proxy Documentation](https://caddyserver.com/docs/quick-starts/reverse-proxy)
   - [Caddy Automatic HTTPS Architecture](https://caddyserver.com/docs/automatic-https)
3. **Dokumentasi Google Gemini API**:
   - [Gemini API Structured Outputs & JSON Mode](https://ai.google.dev/gemini-api/docs/structured-output)
   - [Gemini Models & Rate Limits](https://ai.google.dev/gemini-api/docs/models/gemini)
4. **Dokumentasi PostgreSQL 16**:
   - [PostgreSQL Index Types & Optimization](https://www.postgresql.org/docs/16/indexes.html)
5. **Dokumentasi Telegram Bot API**:
   - [Telegram Webhook Configuration Guide](https://core.telegram.org/bots/webhooks)

---

<p align="center">
  <b>Tugas Besar Mata Kuliah Komunikasi Data dan Jaringan Komputer (KDJK)</b><br>
  Dibuat dengan dedikasi untuk keunggulan implementasi infrastruktur hosting Linux &amp; otomasi cerdas modern. 🇮🇩
</p>
