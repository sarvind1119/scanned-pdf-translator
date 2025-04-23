# 🧾 Scanned PDF Translator

A Streamlit web application that:
- 📥 Accepts scanned Hindi PDF files
- 🔍 Uses OCR to extract text
- 🌐 Translates it into English, Hindi, Punjabi, Tamil, or Telugu
- 🧩 Splits PDFs by user-defined number of pages
- 📝 Outputs part-wise `.txt` files and one combined `.docx` file

---

## 🚀 Features

✅ Upload scanned Hindi PDFs  
✅ Choose number of pages per split  
✅ Extracts text using Tesseract OCR  
✅ Translate with OpenAI GPT (Multilingual)  
✅ Download part-wise `.txt` files  
✅ Download single `.docx` file with all translations  

---

## 🖥️ Live Demo

> 🚧 Coming soon (host via Railway or local Docker)

---

## 🧰 Tech Stack

- [Python 3.10](https://www.python.org/)
- [Streamlit](https://streamlit.io/)
- [OpenAI GPT API](https://platform.openai.com/)
- [PyMuPDF (fitz)](https://pymupdf.readthedocs.io/)
- [pdf2image + Tesseract OCR](https://github.com/madmaze/pytesseract)
- [python-docx](https://python-docx.readthedocs.io/en/latest/)

---

## 🐳 Run with Docker

```bash
# Build image
docker build -t pdf-translator-app .

# Run container (replace sk-... with your OpenAI API key)
docker run -p 8501:8501 -e OPENAI_API_KEY=sk-... pdf-translator-app
```

Then visit: [http://localhost:8501](http://localhost:8501)

---

## 🛠️ Local Development

```bash
# Clone repo
git clone https://github.com/yourusername/pdf-translator-app.git
cd pdf-translator-app

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run app
streamlit run app4.py
```

---

## 🔑 Environment Variable

| Variable        | Description             |
|-----------------|-------------------------|
| `OPENAI_API_KEY`| Your OpenAI API Key     |

---

## 📂 Folder Structure

```
scanned-pdf-translator/
├── app4.py               # Streamlit app
├── combine_to_word.py    # Combine .txt to .docx
├── requirements.txt      # Python packages
├── Dockerfile            # Docker instructions
└── README.md             # Project overview
```

---

## 🖼️ Screenshots

> ![image](https://github.com/user-attachments/assets/f5d492d1-7a7a-4de2-8b6a-f48f676ab1a2)


---

## 📜 License

MIT License © 2025 Arvind Singh Rawat
