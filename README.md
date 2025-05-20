# tfplan-parser

CLI tool that parses a Terraform plan (plain-text) and summarizes changes by action—**create**, **update**, **destroy**, and **replace**—with counts per resource type.

---

## 🚨 Note

Terraform’s built-in `plan` summary merges a **replace** into one create + one destroy.  
This tool tracks **replace** as its own action so you get an explicit replace count.

---

## 📦 Requirements

- **Python** 3.8+
- Runtime dependencies:
  - `typer[all]`
  - `rich`

---

## ⚙️ Installation

Set up Python virtual environment:

```bash
# from project root - create a .venv folder
python3 -m venv .venv
# activate it (macOS / Linux)
source .venv/bin/activate
```

Install

```bash
# upgrade pip (optional but recommended)
python -m pip install --upgrade pip
# install your project in editable mode (inside your project dir / virtual-env)
pip install -e .
```

## 🗂️ Generating a Plan File

```bash
terraform plan > tfplan.txt
```

Save tfplan.txt as a CI artifact (e.g. GitHub Actions) or drop it next to your scripts.

## 🚀 Usage

```bash
# table summary to console
tfplan-parser -i tfplan.txt

# JSON output
tfplan-parser -i tfplan.txt --json > summary.json

# HTML report
tfplan-parser -i tfplan.txt --output report.html
```

## Options

| Flag                | Description                                        |
| ------------------- | -------------------------------------------------- |
| `-i, --input PATH`  | Terraform plan file (plain-text)                   |
| `-j, --json`        | Emit JSON instead of a Rich-styled table           |
| `-o, --output PATH` | Write HTML (no `-j`) or JSON (with `-j`) to a file |

## 🖥️ Example Output

```bash
┏━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━┓
┃ Action ┃ Resource type                    ┃ Count ┃
┡━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━┩
│ create │ google_storage_bucket            │     2 │
│ update │ google_compute_instance          │     1 │
│ destroy│ google_sql_database              │     1 │
│ replace│ google_bigquery_table            │     1 │
└────────┴──────────────────────────────────┴───────┘
```

## 📝 Example JSON ouptut

```json
{
  "create": {
    "google_storage_bucket": [
      "org--aorg_google_storage_bucket-user-auser_1A496840",
      "org--borg_google_storage_bucket-user-buser_1B69C449"
    ]
  },
  "update": {
    "google_compute_instance": [
      "org--aorg_compute_instance-user-auser_ABC123DEF"
    ]
  },
  "destroy": {
    "google_sql_database": ["org--aorg_sql_database-main"]
  },
  "replace": {
    "google_bigquery_table": ["org--aorg_bigquery_table-main_table"]
  }
}
```

## 🧪 Testing

```bash
# install test deps (optional-extras)
pip install -e .[test]

# run pytest
pytest
```
