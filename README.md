# Project README: Yelp Sentiment Analysis and Graph Interpretation

Welcome to the Yelp Sentiment Analysis and Graph Interpretation project! This README provides an overview of the project, its components, setup instructions, and usage guidelines.

## Table of Contents

1. **Introduction**
2. **Project Overview**
3. **Prerequisites**
4. **Installation**
5. **Usage**
6. **Contributing**
7. **License**

## 1. Introduction

This project aims to analyze sentiments of Yelp reviews for two specified Yelp URLs using BERT sentiment analysis and visualize the sentiment trends over possible years. The sentiment data is then used to generate detailed interpretations using OpenAI's GPT-3.5 model.

## 2. Project Overview

The project consists of a React frontend using Material-UI (MUI), a Python Flask backend, sentiment analysis with BERT, sentiment visualization using pandas and matplotlib, and interpretation using OpenAI's GPT-3.5 model.

## 3. Prerequisites

-   Node.js and npm (for the React frontend)
-   Python 3.x (for the Flask backend)
-   OpenAI API key (for generating interpretations)

## 4. Installation

### Frontend

1. Navigate to the `frontend` directory.
2. Run `npm install` to install frontend dependencies.

### Backend

1. Navigate to the `backend` directory.
2. Create a virtual environment: `python3 -m venv venv`
3. Activate the virtual environment:
    - On Windows: `venv\Scripts\activate`
    - On macOS/Linux: `source venv/bin/activate`
4. Run `pip install -r requirements.txt` to install backend dependencies.

## 5. Usage

1. **Frontend:**

    - Start the frontend: `npm start`

2. **Backend:**

    - Set up your OpenAI GPT-3.5 API key in a safe and secure manner
        - You will be getting it via os.environ.get("OPEN_AI_KEY")
    - Start the backend: `python flask_server.py`

3. **Using the Application:**
    - Access the frontend through your browser.
    - Input two Yelp URLs and click "Submit."
    - The frontend will call the backend to perform sentiment analysis, generate sentiment graphs, and interpret the trends.

## 6. Contributing

Contributions are welcome! If you have improvements or new features to add, please follow the standard GitHub Fork & Pull Request process.

## 7. License

This project is licensed under the [MIT License](LICENSE).
