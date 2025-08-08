# Quiz Data Schema (v1.0)

## Purpose
Canonical, app-ready format for quiz questions aggregated from scraping and user imports.  
This contract ensures the scraper, converters, and Android app stay compatible.

---

## File Format
- **JSON Lines (JSONL)**: one JSON object per line
- UTF-8 encoded
- Canonical file: `data/processed/questions.jsonl`

---

## Record Overview
Each line is a **QuestionDoc**.

```json
{
  "schema_version": "1.0",
  "id": "ExamplePrep:3:12",
  "source": { "name": "ExamplePrep", "url": "https://ex.com/t/3", "test_no": 3 },
  "question": { "q_no": 12, "text": "Which is true?", "html": null, "type": "single" },
  "options": [
    {"key": "A", "text": "Needs GROUP BY"},
    {"key": "B", "text": "Returns one result per row"},
    {"key": "C", "text": "Replaces WHERE"}
  ],
  "correct_options": ["B"],
  "explanation": "Window functions preserve row granularity.",
  "topic": "SQL",
  "tags": ["window-functions","analytics"],
  "difficulty": "medium",
  "date": "2024-10-01",
  "media": [],
  "metadata": { "scraped_at": "2025-08-08T22:14:00Z", "source_item_id": "t3_q12" },
  "quality": { "needs_review": false, "incomplete": false, "skip": false },
  "hash": "sha1:3c1f…",
  "language": "en"
}
```

---

## Fields

### Top level
- **`schema_version`** *(string, req)* — Current schema version, start at `"1.0"`.
- **`id`** *(string, req)* — Stable human-readable ID, default:  
  `"{source.name}:{source.test_no}:{question.q_no}"`.
- **`source`** *(object, req)*:
  - `name` *(string, req)*
  - `url` *(string, opt \| null)*
  - `test_no` *(integer, opt \| null)*
- **`question`** *(object, req)*:
  - `q_no` *(integer, req)*
  - `text` *(string, req)*
  - `html` *(string, opt \| null)*
  - `type` *(string, req)* — `"single"` or `"multiple"`
- **`options`** *(array<Option>, req)* — 2..10 items:
  - `Option.key` *(string, req)* — `"A"`, `"B"`, …
  - `Option.text` *(string, req)*
- **`correct_options`** *(array<string>, req)* — letters from `options.key`
- **`explanation`** *(string, opt \| null)*
- **`topic`** *(string, opt \| null)*
- **`tags`** *(array<string>, opt \| null)*
- **`difficulty`** *(string, opt \| null)* — freeform or `"easy" | "medium" | "hard"`
- **`date`** *(string, opt \| null)* — ISO-8601 date (`YYYY-MM-DD`)
- **`media`** *(array<string>, opt)*
- **`metadata`** *(object, opt)*:
  - `scraped_at` *(string, opt \| null)*
  - `source_item_id` *(string, opt \| null)*
- **`quality`** *(object, opt)*:
  - `needs_review` *(boolean, req if present)*
  - `incomplete` *(boolean, req if present)*
  - `skip` *(boolean, req if present)*
- **`hash`** *(string, req)* — SHA1 of normalized question + options
- **`language`** *(string, opt)* — default `"en"`

---

## Constraints
- `question.type ∈ {"single","multiple"}`
- `len(options) ≥ 2` and ≤ 10
- `options.key` unique, uppercase A..Z in order
- `correct_options ⊆ {options.key}`
- If `question.type == "single"` → `len(correct_options) == 1`
- `question.text` non-empty
- `id` unique within a file
- `hash` ideally unique across files
- **Skip precedence:** If `quality.skip == true`, the question must be excluded from quiz presentation in the app, regardless of other `quality` flags.


---

## Curation Workflow for `quality` Flags

These flags indicate the review and inclusion status of a question:

1. **Initial scrape/import**
   - `needs_review = false`
   - `incomplete = false`
   - `skip = false`
   - All new questions are assumed usable unless clearly broken.

2. **Flagging for review**
   - Set `needs_review = true` if the question:
     - Has suspicious or unclear content
     - Is missing a key part (e.g., option text, partial question)
     - Requires human verification (e.g., correct answer in doubt)
   - `incomplete` may also be set here if missing data is detected.

3. **Post-review outcomes**
   - **Approved:**  
     - `needs_review = false`
     - `incomplete = false` (if fixed)
     - `skip = false`
   - **Incomplete but usable:**  
     - `needs_review = false`
     - `incomplete = true` (e.g., missing optional explanation)
     - `skip = false`
   - **Rejected (unusable):**  
     - `needs_review = false`
     - `incomplete` = true or false (as applicable)
     - `skip = true` → Exclude from app quizzes permanently

4. **App behavior**
   - Questions with `skip = true` must **never** appear in quiz sessions.
   - Other flags (`needs_review`, `incomplete`) are metadata for maintainers and do not affect inclusion unless `skip` is set.

---

### Quality Flag Decision Table

| needs_review | incomplete | skip  | Meaning / Action                                           |
|--------------|------------|-------|------------------------------------------------------------|
| false        | false      | false | ✅ Ready for use — complete and approved                   |
| false        | true       | false | ⚠️ Usable but missing optional info                        |
| true         | false      | false | 🔍 Awaiting review — content seems fine but needs checking |
| true         | true       | false | 🔍 Awaiting review — content incomplete                    |
| false        | any        | true  | ❌ Rejected — exclude from app quizzes                      |
| true         | any        | true  | ❌ Rejected but still marked for review (double-check reason) |

---

## ID Policy
Default:  
```
"{source.name}:{source.test_no}:{question.q_no}"
```
If `test_no` is unknown, use:
```
"{source.name}:{metadata.source_item_id}"
```

---

## Hash Policy
```
hash = "sha1:" + sha1(
  lower(trim(question.text)) + "||" +
  "||".join(lower(trim(o.text)) for o in options in order)
)
```
Use for deduplication across runs and sources.

---

## Examples (JSONL)
```
{"schema_version":"1.0","id":"ExamplePrep:3:1","source":{"name":"ExamplePrep","url":"https://ex.com/t/3","test_no":3},"question":{"q_no":1,"text":"Pick the true statement.","html":null,"type":"single"},"options":[{"key":"A","text":"Needs GROUP BY"},{"key":"B","text":"Returns one per row"}],"correct_options":["B"],"explanation":null,"topic":"SQL","tags":["window-functions"],"difficulty":null,"date":null,"media":[],"metadata":{"scraped_at":"2025-08-08T22:14:00Z","source_item_id":"t3_q1"},"quality":{"needs_review":false,"incomplete":false,"skip":false},"hash":"sha1:...","language":"en"}
{"schema_version":"1.0","id":"ExamplePrep:3:2","source":{"name":"ExamplePrep","url":"https://ex.com/t/3","test_no":3},"question":{"q_no":2,"text":"Select all correct options.","html":null,"type":"multiple"},"options":[{"key":"A","text":"Uses OVER()"},{"key":"B","text":"Removes WHERE"},{"key":"C","text":"Can partition rows"}],"correct_options":["A","C"],"explanation":"…","topic":"SQL","tags":["window-functions"],"difficulty":"medium","date":"2024-10-01","media":[],"metadata":{"scraped_at":"2025-08-08T22:14:10Z","source_item_id":"t3_q2"},"quality":{"needs_review":false,"incomplete":false,"skip":false},"hash":"sha1:...","language":"en"}
{"schema_version":"1.0","id":"ExamplePrep:5:3","source":{"name":"ExamplePrep","url":"https://ex.com/t/5","test_no":5},"question":{"q_no":3,"text":"Identify the molecule shown.","html":null,"type":"single"},"options":[{"key":"A","text":"Glucose"},{"key":"B","text":"Fructose"}],"correct_options":["A"],"explanation":null,"topic":"Chemistry","tags":["organic","structure"],"difficulty":"medium","date":null,"media":[],"metadata":{"scraped_at":"2025-08-08T23:01:00Z","source_item_id":"t5_q3"},"quality":{"needs_review":false,"incomplete":true,"skip":true},"hash":"sha1:...","language":"en"}
```


---

## CSV Import/Export (Optional)
Template columns for user-friendly CSV:
```
source_name,source_url,test_no,q_no,q_type,question_text,options,correct_options,explanation,topic,tags,language
```
- `options`: semicolon-separated (`A) foo; B) bar; C) baz` or `foo; bar; baz`)
- `correct_options`: semicolon-separated letters (`B` or `A;C`)

---

## Versioning
- Current: `schema_version = "1.0"`
- Backwards-compatible additions → bump minor (e.g., `"1.1"`)
- Breaking changes → bump major (e.g., `"2.0"`)
- Keep migration notes here.

---

## Migration Notes
- *1.0 → 1.1*: _(placeholder)_
- *1.1 → 2.0*: _(placeholder)_

---

## Testing & Validation
- Run a JSON Schema validator (optional) during scraping/import.
- Spot check:
  - `correct_options` letters exist in `options`
  - No empty `question.text`
  - ≥ 2 `options`
