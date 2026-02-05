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
- `--max-per-tag-per-level` : Limits how many times each tag prints at a given level (e.g., show 2 <A> and 2 <B>)


### 4. To convert XML into CSV

```bash
python3 main.py <filename>.xml
```

### 5. To Format the XML file

```bash
xmllint --format <filename>.xml > <output_filename>.xml
```