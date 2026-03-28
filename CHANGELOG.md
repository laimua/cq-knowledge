# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-03-25

### Added

#### Core Features
- **Knowledge Unit (KU) Data Model**: Structured storage for problems, solutions, and metadata
- **SQLite Storage with FTS5**: Full-text search capability for knowledge retrieval
- **CLI Tool**: Complete command-line interface for knowledge management
  - `cq init` - Initialize knowledge base
  - `cq add` - Add knowledge unit
  - `cq list` - List knowledge units
  - `cq search` - Search knowledge with FTS5
  - `cq show` - Show knowledge details
  - `cq delete` - Delete knowledge unit
  - `cq export` - Export knowledge base to JSON
  - `cq import-cmd` - Import knowledge base from JSON
  - `cq feedback` - Add feedback for knowledge unit

#### MCP Integration
- **Claude Code MCP Plugin**: Seamless integration with Claude Code
  - `search_knowledge` tool
  - `add_knowledge` tool
  - `show_knowledge` tool
  - `list_knowledge` tool
  - `add_feedback` tool

#### Advanced Features
- **Confidence Scoring System**: Rate knowledge reliability (0-1)
- **Feedback System**: Mark knowledge as helpful/unhelpful
- **Tag-based Filtering**: Organize knowledge with tags
- **Usage Tracking**: Track how often knowledge is used

#### Testing
- **30 Comprehensive Tests**: 100% pass rate
  - CLI tests (8)
  - Database tests (10)
  - MCP tests (12)

### Technical Details

#### Dependencies
- FastAPI >= 0.104.0
- Typer >= 0.9.0
- Rich >= 13.7.0
- aiosqlite >= 0.19.0
- MCP >= 0.9.0

#### Database Schema
- `knowledge_units` table with FTS5 virtual table
- `feedback_history` table for user feedback
- Automatic migration system
- Trigger-based FTS synchronization

#### Architecture
- Clean architecture with repositories pattern
- Async/await throughout
- Type hints with Pydantic models
- Modular design for extensibility

### Fixed
- Database migration duplicate execution issue
- FTS5 search syntax with `bm25()` function
- Typer/Click compatibility (Click 8.1.7)
- Storage cursor await warnings

### Security
- Local SQLite database (no external dependencies)
- No data leaves your machine
- Optional cloud sync (future feature)

---

## Future Plans

### [0.2.0] - Planned
- Web management interface
- Enhanced search with semantic similarity
- Knowledge deduplication
- Import from external sources (Stack Overflow, etc.)

### [0.3.0] - Planned
- Cloud sync functionality
- Team collaboration features
- API endpoints for external integrations
- Knowledge versioning

### [1.0.0] - Planned
- Production-ready release
- Full documentation
- Community guidelines
- Contribution workflow

---

## Release Notes

### v0.1.0 - Initial MVP Release

This is the first public release of Cq! 🎉

**What's Included:**
- Full CLI functionality for knowledge management
- MCP integration with Claude Code
- Local SQLite storage with full-text search
- Confidence scoring and feedback system
- Comprehensive test suite (30/30 passing)

**Known Limitations:**
- No web interface (planned for v0.2.0)
- No cloud sync (planned for v0.3.0)
- English and Chinese documentation only

**Getting Started:**
```bash
pip install cq-knowledge
cq-knowledge init
cq-knowledge add --title "Your first knowledge" --problem "Problem" --solution "Solution"
```

**Feedback Welcome!**
Please report issues and suggestions on [GitHub Issues](https://github.com/yourusername/cq/issues).

---

[0.1.0]: https://github.com/yourusername/cq/releases/tag/v0.1.0
