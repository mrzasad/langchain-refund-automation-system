# 🤖 Refund Automation System

An AI-powered Streamlit application that automates refund decisions for customer complaints using LangChain and OpenAI's GPT models.

## Features

✨ **Key Features:**
- **Data Loading**: Upload Excel files with customer complaint tickets
- **AI-Powered Extraction**: Use LLMs with Pydantic models to extract delivery and claim dates
- **Intelligent Decision Making**: Automated approval/rejection based on refund policy
- **Email Generation**: Generate personalized response emails using prompt templates
- **Structured Output**: Store all results in pandas DataFrames
- **Streamlit Dashboard**: Interactive UI with progress tracking and visualizations

## Requirements

- Python 3.8+
- OpenAI API Key
- Libraries: streamlit, pandas, langchain, pydantic, openpyxl

## Installation

```bash
pip install -r requirements.txt
