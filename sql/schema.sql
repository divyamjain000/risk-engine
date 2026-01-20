-- Portfolio-related tables for risk_engine
-- Run with: psql postgresql://risk_user:risk_password@localhost:5432/risk_engine -f sql/schema.sql

CREATE TABLE IF NOT EXISTS positions (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(128) NOT NULL,
    quantity DOUBLE PRECISION NOT NULL,
    avg_price DOUBLE PRECISION NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_positions_symbol ON positions (symbol);

-- Daily holdings snapshots per symbol
CREATE TABLE IF NOT EXISTS holdings_daily (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(128) NOT NULL,
    as_of_date DATE NOT NULL,
    quantity DOUBLE PRECISION NOT NULL,
    avg_price DOUBLE PRECISION,
    CONSTRAINT uq_holdings_daily_symbol_date UNIQUE (symbol, as_of_date)
);

CREATE INDEX IF NOT EXISTS idx_holdings_daily_symbol ON holdings_daily (symbol);
CREATE INDEX IF NOT EXISTS idx_holdings_daily_date ON holdings_daily (as_of_date);
