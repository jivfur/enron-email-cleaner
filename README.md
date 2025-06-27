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

