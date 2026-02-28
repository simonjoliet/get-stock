# get-stock

Extract image metadata from Shutterstock and Adobe Stock HTML exports. Outputs CSV-style lines with platform, filename, ID, and title. Auto-detects platform and decodes HTML/URL-encoded titles. Supports wildcard file patterns for batch processing.

---

## Purpose

When exporting catalog or portfolio pages from stock platforms, the data is embedded inside HTML rather than provided as a clean CSV.  

This script:

- Detects the platform automatically from the `<title>` tag  
- Extracts relevant image metadata using regular expressions  
- Outputs structured, comma-separated results to stdout  
- Supports wildcard file patterns (`*.html`)  

---

## Requirements

- Python 3.7+  
- No external dependencies (standard library only)  

Uses: `re`, `glob`, `html`, `urllib.parse`, `os`, `sys`  

---

## How It Works

### Platform Detection

The script reads the `<title>` tag from the HTML file to determine the platform:

```python
pattern = r'<title>(.*?)</title>'
platform = re.findall(pattern, content)[0][-12:].strip()
