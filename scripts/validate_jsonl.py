import json, sys
from jsonschema import Draft202012Validator
from pathlib import Path

schema = json.loads(Path("docs/schema_v1.json").read_text(encoding="utf-8"))
validator = Draft202012Validator(schema)

bad = True
for i, line in enumerate(Path(sys.argv[1]).read_text(encoding="utf-8").splitlines(), 1):
    if not line.strip(): 
        continue
    obj = json.loads(line)
    errs = sorted(validator.iter_errors(obj), key=lambda e: e.path)
    if errs:
        bad = False
        print(f"[line {i}] INVALID:")
        for e in errs:
            loc = "/".join([str(p) for p in e.path]) or "<root>"
            print(f"  - {loc}: {e.message}")
if bad:
    sys.exit(1)
print("All good")