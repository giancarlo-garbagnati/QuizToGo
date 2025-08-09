# Data Directory

This folder stores all quiz data for the project.

---

## Structure

```
data/
  raw/         # Unprocessed data straight from scraping (HTML dumps, raw API JSON)
  processed/   # Canonical JSONL files that follow the data contract
  exports/     # Optional exports (CSV, JSON arrays) for analysis or sharing
```

---

## Guidelines

### `raw/`
- **Purpose:** Debugging, development, archival of original scrape responses.
- **Format:** Whatever the source provides — may include HTML, JSON, screenshots.
- **Version control:** **Do not commit** large/raw scrape files. These are transient.

### `processed/`
- **Purpose:** Clean, normalized quiz data following the [data contract](../docs/schema.md).
- **Canonical file:**  
  `questions.jsonl` — single JSONL file, one question record per line.
- **Version control:** Commit only **valid** files that pass the schema validator.
- **Naming:**  
  - Use `questions.jsonl` for the current canonical dataset.  
  - If you keep historical snapshots, name as `questions_YYYYMMDD.jsonl`.

### `exports/`
- **Purpose:** Derived files for external use — e.g., CSV exports for analysis.
- **Version control:** Optional; commit only small representative samples if needed.
- **Formats:** CSV, JSON arrays, etc.

---

## Validation

Always validate processed files before committing:

```bash
python scripts/validate_jsonl.py data/processed/questions.jsonl
```

---

## Import/Export Tools
- **CSV → JSONL**: `scripts/csv_to_jsonl.py`  
- **JSONL → CSV**: _TBD_ (planned script for analysis exports)

---

## Notes
- Keep `raw/` and any sensitive/large files **out of git** (see `.gitignore`).
- `processed/` is the **single source of truth** for the Android app.
- The `skip` flag in `quality` ensures certain questions are excluded from the app.
