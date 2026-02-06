# XML To CSV

## 🚀 Getting Started (Local Dev)

### 1. Create and Activate a Python Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. To get the XML Structure

```bash
python3 main.py <filename>.xml --print-structure --max-depth 3 --max-per-tag-per-level 2
```

#### Arguments:
- `--max-depth` : Controls how deep the structure prints (0 = root)
- `--max-per-tag-per-level` : Limits how many times each tag prints at a given level


### 4. To convert XML into CSV

```bash
python3 main.py <filename>.xml
```

### 5. To Format the XML file

```bash
xmllint --format <filename>.xml > <output_filename>.xml
```

### 6. Logging 📊

Control verbosity with `--log-level` to see what's happening at each step. All logs are printed to the terminal with **color-coded levels** for easy scanning.

#### Log Levels

| Level | Color | Use Case |
|-------|-------|----------|
| **DEBUG** | 🔵 Cyan | Pedantic per-row details; use when troubleshooting |
| **INFO** | 🟢 Green | Default; tracks key steps (start, export progress, row counts) |
| **WARNING** | 🟡 Yellow | Warns about potential issues |
| **ERROR** | 🔴 Red | Only errors that don't stop execution |
| **CRITICAL** | 🟥 Red BG | Critical failures |

#### Examples

**Default (INFO):**
```bash
python3 main.py 1_12.26.25.xml
```

**Debug mode (see every row processed):**
```bash
python3 main.py --log-level DEBUG 1_12.26.25.xml
```

**Quiet mode (warnings only):**
```bash
python3 main.py --log-level WARNING 1_12.26.25.xml
```