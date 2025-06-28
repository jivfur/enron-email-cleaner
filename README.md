# Enron Email Cleaner and Thread Builder

A Python-based tool to parse, clean, and structure the [Enron Email Dataset](https://www.cs.cmu.edu/~enron/) for downstream machine learning tasks. This tool extracts metadata, cleans message bodies, and optionally reconstructs email threads into a structured format for contextual modeling such as sentiment classification.

---

## 🔍 Features

- 📑 **Metadata Extraction**: Extracts `From`, `To`, `Subject`, `Date`, and other headers.
- 🧹 **Body Cleaning**: Removes email signatures, legal disclaimers, quoted replies, and common noise.
- 🧵 **Thread Reconstruction** *(optional)*: Groups emails into thread-like structures using subject normalization and timestamp proximity.
- 🛠️ **Output Formats**: Supports saving the cleaned data in structured formats like JSON or CSV for further processing.

---

## 📁 Folder Structure (Input)

The tool expects the standard Enron dataset format:

```
enron_mail_20110402/
├── allen-p/
│ ├── inbox/
│ ├── sent/
│ └── ...
├── arora-h/
│ └── ...
```
Each mailbox folder contains subfolders with `.txt` files — one per email.

---

## 🚀 Usage Overview

1. **Download and unzip** the Enron dataset.
2. **Run the cleaner script** to extract metadata and clean the body content.
3. (Optional) **Enable thread reconstruction** to group emails by subject and timestamp.
4. **Export results** to your preferred format.

> 📌 *This repository focuses on preprocessing only. It does not include any machine learning or modeling components.*

---
### 📦 Installation

It's recommended to use a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
---

## 📦 Requirements

- Python 3.8+
- Dependencies: listed in `requirements.txt` (e.g., `email`, `mailparser`, `email-reply-parser`)

---

## 📚 Use Cases

- Preparing email threads for NLP research
- Building sentiment analysis datasets with context
- Training lightweight models for email classification
- Teaching and experimentation with real-world communication data
---
### 🔄 Batch Processing Enron Emails

This project includes a utility script to process a folder of raw Enron-style email files (plain `.txt` format with headers and body) and convert them into a structured, cleaned format suitable for downstream tasks like sentiment analysis or thread reconstruction.

#### 🛠 How It Works

- Parses headers (`From`, `To`, `Subject`, `Date`)
- Cleans the body (removes signatures and quoted replies)
- Normalizes subject for threading
- Generates a consistent `ThreadKey` using subject + date
- Tracks the source filename

#### 📂 Folder Structure (Example)

```bash
data/enron-emails/
├── email1.txt
├── email2.txt
...
```

#### 🚀 How to Run

Run the script directly:

```bash
python process_enron_folder.py
```

Or import into another script or notebook:

```python
from process_enron_folder import process_enron_folder

emails = process_enron_folder("data/enron-emails")

# Optionally save output
import json
with open("cleaned_emails.json", "w", encoding="utf-8") as f:
    json.dump(emails, f, indent=2)
```
 - Emails with encoding issues are skipped with a warning.
 - This version ignores attachments and non-standard MIME formats.
 - Outputs a list of dictionaries, each representing a cleaned email with metadata.

---

## 🗂 Access the Cleaned Dataset

You can download the fully processed and cleaned Enron Email Dataset directly from Kaggle, without needing to run the cleaner yourself:

🔗 **[📥 Download on Kaggle](https://www.kaggle.com/datasets/jivfur/enron-emails)**

This version includes:
- Cleaned plain-text email bodies
- Extracted metadata (`From`, `To`, `Subject`, `Date`)
- Normalized subject lines
- Thread keys for grouping related emails
- Original filenames for traceability

**Format**: JSON (~1 GB)  
**Encoding**: UTF-8  
**License**: Research use only — see disclaimer below
---

## ⚖️ License

This project is released under the MIT License. See `LICENSE` for details.

---

## 🙏 Acknowledgments

- Original Enron Email Dataset provided by Carnegie Mellon University.
- Inspired by research in contextual sentiment analysis and conversational modeling.

---

## ✨ Future Plans

- Add support for HTML-to-text conversion
- Improve thread grouping heuristics
- Optional anonymization of email content for ethical research use

---

