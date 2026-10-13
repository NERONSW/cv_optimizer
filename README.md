# Local CV & Cover Letter Tailor

A lightweight, local Streamlit application designed to automatically tailor your comprehensive Master Resume and Cover Letter against any target job description using OpenRouter LLM APIs.

## 🚀 Key Features

- **Local Context Management:** Reads your master files (`master_resume.md`, `master_prompt.md`, `common_cv_template.md`) directly from disk—no manual re-uploading required.
- **OpenRouter Multi-Model Support:** Seamlessly switch between cost-effective, high-reasoning models like `openai/gpt-4o-mini`, `deepseek/deepseek-chat`, and `anthropic/claude-3.5-sonnet`.
- **API Key Gatekeeping:** Built-in live validation ensures your OpenRouter key is authenticated before unlocking the application interface.
- **Strict 2-Page Budgeting:** Utilizes a structural exemplar (`common_cv_template.md`) and dynamic rules to enforce exact word counts, line limits, and bullet constraints.
- **Truthfulness Controls:** Strict negative constraints prevent AI hallucinations, keyword stuffing, or invented skills/experience.
- **Copy-Ready Output:** Generates clean Markdown output with instant copy blocks and one-click file downloads.

## 📁 Project Structure

```text
cv-tailor/
├── .streamlit/
│   └── secrets.toml          # Optional OpenRouter API key configuration
├── app.py                    # Main Streamlit web application
├── master_prompt.md          # Optimization rules, constraints, and instructions
├── master_resume.md          # Comprehensive unfiltered master resume source data
├── common_cv_template.md     # 2-page target layout and structural exemplar
└── master_cover_letter.md    # Master cover letter source
```

````

## 🛠️ Quick Start

1. Install dependencies:

```bash
pip install streamlit openai

```

2. Place your markdown context files into the project root.
3. Run the application:

```bash
streamlit run app.py

```
````
