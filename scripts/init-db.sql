-- ==============================================================================
-- KDJK Project: Bot Manajemen Keuangan Pribadi
-- Database Initialization Script for PostgreSQL 16
-- ==============================================================================

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

-- Index untuk mempercepat query rekap harian dan bulanan per user Telegram
CREATE INDEX IF NOT EXISTS idx_transactions_user_date 
    ON transactions (telegram_user_id, transaction_date DESC);
