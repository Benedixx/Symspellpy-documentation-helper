# Symspellpy Documentation Helper

![Symspellpy Documentation Helper](https://github.com/Benedixx/Symspellpy-documentation-helper/assets/97221880/11753826-f2d6-45e9-81ec-572a35bcb1c6)

## Introduction

Symspellpy Documentation Helper is a valuable LLM companion for developers working with Symspellpy, a Python library for spelling correction based on Symmetric Delete spelling correction algorithm. This tool streamlines the process of accessing and comprehending Symspellpy's documentation.

## Features

- Quick access to documentation: Easily navigate through Symspellpy documentation.
- Simplified querying: Ask questions related to Symspellpy's usage, features, and functionalities.
- Enhanced understanding: Get concise explanations and examples for better comprehension.
- Visual aid: Utilize images and diagrams to enhance learning and understanding.

## Installation

To use Symspellpy Documentation Helper, you need to clone the repository:
```
git clone https://github.com/Benedixx/Symspellpy-documentation-helper.git
```
##  Usage

1. Download Symspellpy documentation :
```
python download_docs.py
```   
2. Create index on your pinecone databases in https://www.pinecone.io/ console
3. make .env file and insert your Azure OpenAI endpoint and API key, and Pinecone host and API key
4. Ingest data and store it on database by running this command :
```
python ingestion.py
```
5. Open terminal and run :
```
streamlit run main.py
```
