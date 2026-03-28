-- migrations/001_initial.sql
-- Initial database schema for Cq
-- Version: 1.0
-- Date: 2026-03-25

-- Schema version tracking
CREATE TABLE IF NOT EXISTS schema_version (
    version INTEGER PRIMARY KEY,
    applied_at TEXT NOT NULL DEFAULT (datetime('now'))
);

-- Knowledge units table
CREATE TABLE IF NOT EXISTS knowledge_units (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    problem TEXT NOT NULL,
    solution TEXT NOT NULL,
    context TEXT DEFAULT '{}',
    confidence REAL DEFAULT 0.5 CHECK (confidence >= 0 AND confidence <= 1),
    usage_count INTEGER DEFAULT 0 CHECK (usage_count >= 0),
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now')),
    source TEXT DEFAULT 'manual',
    verified INTEGER DEFAULT 0 CHECK (verified IN (0, 1))
);

-- Indexes for knowledge_units
CREATE INDEX IF NOT EXISTS idx_ku_created_at ON knowledge_units(created_at);
CREATE INDEX IF NOT EXISTS idx_ku_confidence ON knowledge_units(confidence);
CREATE INDEX IF NOT EXISTS idx_ku_source ON knowledge_units(source);
CREATE INDEX IF NOT EXISTS idx_ku_verified ON knowledge_units(verified);
CREATE INDEX IF NOT EXISTS idx_ku_updated_at ON knowledge_units(updated_at);

-- FTS5 virtual table for full-text search
CREATE VIRTUAL TABLE IF NOT EXISTS ku_fts USING fts5(
    title,
    problem,
    solution,
    content='knowledge_units',
    content_rowid='rowid',
    tokenize='porter unicode61'
);

-- Trigger: Insert knowledge unit -> sync to FTS
CREATE TRIGGER IF NOT EXISTS ku_ai AFTER INSERT ON knowledge_units BEGIN
    INSERT INTO ku_fts(rowid, title, problem, solution)
    VALUES (NEW.rowid, NEW.title, NEW.problem, NEW.solution);
END;

-- Trigger: Delete knowledge unit -> sync to FTS
CREATE TRIGGER IF NOT EXISTS ku_ad AFTER DELETE ON knowledge_units BEGIN
    INSERT INTO ku_fts(ku_fts, rowid, title, problem, solution)
    VALUES ('delete', OLD.rowid, OLD.title, OLD.problem, OLD.solution);
END;

-- Trigger: Update knowledge unit -> sync to FTS
CREATE TRIGGER IF NOT EXISTS ku_au AFTER UPDATE ON knowledge_units BEGIN
    INSERT INTO ku_fts(ku_fts, rowid, title, problem, solution)
    VALUES ('delete', OLD.rowid, OLD.title, OLD.problem, OLD.solution);
    INSERT INTO ku_fts(rowid, title, problem, solution)
    VALUES (NEW.rowid, NEW.title, NEW.problem, NEW.solution);
END;

-- Feedback history table
CREATE TABLE IF NOT EXISTS feedback_history (
    id TEXT PRIMARY KEY,
    ku_id TEXT NOT NULL,
    helpful INTEGER NOT NULL CHECK (helpful IN (0, 1)),
    feedback_at TEXT NOT NULL DEFAULT (datetime('now')),
    source TEXT,
    FOREIGN KEY (ku_id) REFERENCES knowledge_units(id) ON DELETE CASCADE
);

-- Indexes for feedback_history
CREATE INDEX IF NOT EXISTS idx_feedback_ku_id ON feedback_history(ku_id);
CREATE INDEX IF NOT EXISTS idx_feedback_at ON feedback_history(feedback_at);
CREATE INDEX IF NOT EXISTS idx_feedback_helpful ON feedback_history(helpful);

-- Note: Migration version tracking is handled by storage.py _apply_migration()
