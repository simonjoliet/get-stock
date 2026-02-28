# HTML Stock Export Parser

Extract image metadata from Shutterstock and Adobe Stock HTML exports. Outputs CSV-style lines with platform, filename, ID, and title. Auto-detects platform or can be forced with a flag. Supports wildcard file patterns for batch processing.

---

## Purpose

When exporting catalog or portfolio pages from stock platforms, the data is embedded in HTML rather than provided as a clean CSV.  

This script:

- Detects the platform automatically from the `<title>` tag or via a flag  
- Extracts relevant image metadata using regular expressions  
- Outputs structured, comma-separated results to stdout  
- Supports wildcard file patterns (`*.html`)  

---

## Requirements

- Python 3.7+  
- Standard library only (`re`, `glob`, `html`, `urllib.parse`, `os`, `sys`)  

---

## How It Works

### Platform Detection

The script reads the `<title>` tag from the HTML file to determine the platform.  
You can also force a platform using the `--platform` flag:

```bash
py script.py "*.html" --platform adobe
py script.py "*.html" --platform shutterstock
