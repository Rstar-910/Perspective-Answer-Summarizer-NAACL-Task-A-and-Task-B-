# Perspective-Answer-Summarizer-NAACL-Task-A-and-Task-B-

# Perspective Answer Summarizer (NAACL Task A & B)

A web-based AI-powered tool for perspective-aware answer summarization, built for the **NAACL 2025 PerAnsSumm shared task**. It extracts and summarizes perspective-specific spans from health-related answers.

## 🚀 Features

- **Perspective-Specific Span Extraction** (Task A)
- **Perspective-Specific Answer Summarization** (Task B)
- **Deep Learning & NLP models** for precise extraction & summarization
- **Interactive Web UI** for seamless user experience

## 🛠️ Technologies Used

| Category             | Technologies & Tools |
|----------------------|--------------------------------------------------------|
| **Frontend**        | React.js, Tailwind CSS, Theme UI                      |
| **Backend**         | Flask, FastAPI                                        |
| **AI/ML Models**    | mDeBERTa-v3-base (SQuAD2), Flan-T5-Small              |
| **Data Processing** | Python, Hugging Face Datasets, Pandas, NumPy         |


## 📜 Installation & Setup

### 1️⃣ Clone the Repository
```bash
 git clone https://github.com/yourusername/perspective-answer-summarizer.git
 cd perspective-answer-summarizer
```

### 2️⃣ Install Dependencies
#### Backend (Flask API)
```bash
 cd backend
 pip install -r requirements.txt
 python server.py
```
#### Frontend (React.js)
```bash
 cd frontend
 npm install
 npm start
```

## 📡 API Endpoints
| Method | Endpoint | Description |
|--------|---------|-------------|
| `POST` | `/api/process-question` | Takes a health-related question & answer, extracts perspective-specific spans, and generates summaries. |

## 🖥️ Usage
1. Enter a **health-related question**.
2. Provide a **detailed answer**.
3. Click **Generate Insights** to extract perspective-specific spans.
4. View AI-generated perspective summaries.

## 🤝 Contributing
Feel free to contribute by submitting issues or pull requests!

---
💡 **Developed for NAACL 2025 PerAnsSumm** | **Built with AI & NLP!** 🚀
