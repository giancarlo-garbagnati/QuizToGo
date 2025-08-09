# Quiz App Project

A quiz application with a Python scraping backend and a Kotlin/Android frontend.  
The backend scrapes questions from various sources, normalizes them into a single canonical format, and the app consumes that format to present quizzes to users.

---

## Data Contract

All quiz data follows the **canonical JSONL schema** defined in [`docs/schema.md`](docs/schema.md).

### Format
- **File type:** JSON Lines (JSONL), UTF-8 encoded
- **Canonical path:** `data/processed/questions.jsonl`
- **One object per line** — each object is a complete question record.

### Schema Highlights
- **Required fields:**  
  `schema_version`, `id`, `source`, `question`, `options`, `correct_options`, `hash`
- **Question types:** `"single"` or `"multiple"`
- **Options:** 2–10 items, labeled `"A"`, `"B"`, etc.
- **Correct options:** letters from the options list
- **Quality flags:** `needs_review`, `incomplete`, `skip` — see workflow in `docs/schema.md`

### Skip Precedence
If `quality.skip == true`, the question **must not** be shown in the app, regardless of other flags.

---

## Validating Data

Run the JSON Schema validator before committing scraped or imported data:

```bash
python scripts/validate_jsonl.py data/processed/questions.jsonl
```

Schema file: [`docs/schema_v1.json`](docs/schema_v1.json)  
Validator: [`scripts/validate_jsonl.py`](scripts/validate_jsonl.py)

---

## CSV Import/Export

- CSV template: [`docs/csv_template.csv`](docs/csv_template.csv)
- Use `scripts/csv_to_jsonl.py` to convert CSV to JSONL following the schema.
- CSV columns:
  ```
  source_name,source_url,test_no,q_no,q_type,question_text,options,correct_options,explanation,topic,tags,language
  ```

---

## Directory Layout

```
data/
  raw/         # Unprocessed dumps, HTML, raw JSON
  processed/   # Canonical JSONL + optional exports
docs/
  schema.md    # Human-readable schema & workflow
  schema_v1.json # Machine-readable schema
scraping/
  ...          # Playwright scraping scripts
android-app/
  ...          # Kotlin Android project
```

---

## License / Legal

Only scrape sources you have permission to use. Respect terms of service and copyright laws when collecting and distributing quiz content.
