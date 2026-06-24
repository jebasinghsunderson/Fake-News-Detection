# Fake-News-Detection

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python)
![ML](https://img.shields.io/badge/Machine-Learning-orange?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

A machine learning project for detecting fake news articles, with support for classification workflows and optional retrieval-based enhancements.

---

## Features

- Detects whether a news article is **real** or **fake**
- Built using Python and machine learning workflows
- Structured project modules for preprocessing and inference
- Docker support for easier deployment

---

## Tech Stack

- Python
- Machine Learning
- Streamlit / Flask style app flow
- ChromaDB / vector search components
- Docker

---

## Project Structure

```bash
Fake-News-Detection/
├── app.py
├── requirements.txt
├── Dockerfile
├── modules/
├── docs/
│   └── chroma/
├── .gitignore
└── README.md
```

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/jebasinghsunderson/Fake-News-Detection.git
cd Fake-News-Detection
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the environment

**Windows**
```bash
venv\Scripts\activate
```

**Linux / Mac**
```bash
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Run the Project

```bash
python app.py
```

Then open the local URL shown in the terminal.

---

## Docker

### Build the image

```bash
docker build -t fake-news-detector .
```

### Run the container

```bash
docker run -p 8501:8501 fake-news-detector
```

---

## Usage

1. Start the application
2. Enter or paste a news article
3. Run the prediction
4. View whether the article is classified as real or fake

---

## Future Improvements

- Add model accuracy and evaluation metrics
- Add screenshots of the UI
- Add API endpoint documentation
- Add CI/CD with GitHub Actions
- Add sample dataset for testing

---

## License

This project is licensed under the MIT License.

---

## Author

**Jebasingh Sunderson I**  
Mudichur, Tamil Nadu, India  
GitHub: [jebasinghsunderson](https://github.com/jebasinghsunderson)
