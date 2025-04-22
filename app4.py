# # Dockerized Streamlit App for OCR + Translation + Combined Word Export
# import os
# import fitz  # PyMuPDF
# from pdf2image import convert_from_path
# from PIL import Image
# import pytesseract
# import streamlit as st
# import tempfile
# from openai import OpenAI
# from combine_to_word import combine_txt_to_docx

# # Set tesseract binary for Linux (default for Docker)
# pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"

# # Configure your OpenAI API key
# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# # Supported languages
# LANGUAGES = {
#     "English": "English",
#     "Hindi": "Hindi",
#     "Punjabi": "Punjabi",
#     "Telugu": "Telugu",
#     "Tamil": "Tamil",
# }

# def split_pdf(input_pdf, pages_per_part=3):
#     pdf_document = fitz.open(input_pdf)
#     total_pages = len(pdf_document)
#     base_name = os.path.splitext(os.path.basename(input_pdf))[0]
#     output_paths = []

#     for i in range(0, total_pages, pages_per_part):
#         part = fitz.open()
#         for j in range(i, min(i + pages_per_part, total_pages)):
#             part.insert_pdf(pdf_document, from_page=j, to_page=j)
#         output_file = f"{base_name}_part{i//pages_per_part + 1}.pdf"
#         part.save(output_file)
#         output_paths.append(output_file)

#     return output_paths

# def extract_text_from_pdf(pdf_path):
#     poppler_path = "/usr/bin"  # Poppler is system-installed in Docker
#     pages = convert_from_path(pdf_path, poppler_path=poppler_path)
#     full_text = ""
#     for i, image in enumerate(pages):
#         try:
#             image = image.convert("RGB")
#             text = pytesseract.image_to_string(image, lang='hin')
#             full_text += f"--- Page {i+1} ---\n{text}\n"
#         except Exception as e:
#             full_text += f"[Error processing page {i+1}]: {str(e)}\n"
#     return full_text

# def chunk_text(text, max_words=1500):
#     words = text.split()
#     for i in range(0, len(words), max_words):
#         yield ' '.join(words[i:i+max_words])

# def translate_text(text, target_language):
#     prompt_prefix = f"Translate the following text to {target_language}:\n\n"
#     translated_chunks = []
#     for chunk in chunk_text(text):
#         try:
#             response = client.chat.completions.create(
#                 model="gpt-3.5-turbo-16k",
#                 messages=[{"role": "user", "content": prompt_prefix + chunk}],
#             )
#             translated_chunks.append(response.choices[0].message.content.strip())
#         except Exception as e:
#             translated_chunks.append(f"[Error during translation: {e}]")
#     return "\n\n".join(translated_chunks)

# def main():
#     st.title("Scanned PDF Translator (Hindi to Multiple Languages)")
#     uploaded_file = st.file_uploader("Upload scanned Hindi PDF", type="pdf")
#     target_lang = st.selectbox("Select target language", list(LANGUAGES.keys()))

#     if uploaded_file and target_lang:
#         os.makedirs("output", exist_ok=True)
#         with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
#             tmp_file.write(uploaded_file.read())
#             tmp_path = tmp_file.name

#         st.info("Splitting PDF into parts...")
#         split_files = split_pdf(tmp_path)
#         st.success("PDF file split successfully")

#         st.info("Extracting and translating each part...")
#         for idx, part_file in enumerate(split_files):
#             text = extract_text_from_pdf(part_file)
#             translated = translate_text(text, LANGUAGES[target_lang])
#             txt_filename = f"output/Part{idx+1}.txt"
#             with open(txt_filename, "w", encoding="utf-8") as f:
#                 f.write(translated)
#             st.success(f"Saved: {txt_filename}")
#             st.download_button(f"Download Part {idx+1} Translation", translated, file_name=f"Part{idx+1}.txt")

#         # Combine all parts into a Word document
#         docx_path = combine_txt_to_docx(txt_folder='output')
#         with open(docx_path, "rb") as f:
#             st.download_button("Download Combined Word File", f, file_name="final_translation.docx")

# if __name__ == "__main__":
#     main()

## Above code splits into 3 by 3 pages, extracts text, translates it, and combines into a Word document.

# Dockerized Streamlit App for OCR + Translation + Combined Word Export
import os
import fitz  # PyMuPDF
from pdf2image import convert_from_path
from PIL import Image
import pytesseract
import streamlit as st
import tempfile
from openai import OpenAI
from combine_to_word import combine_txt_to_docx

# Set tesseract binary for Linux (default for Docker)
pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"

# Configure your OpenAI API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Supported languages
LANGUAGES = {
    "English": "English",
    "Hindi": "Hindi",
    "Punjabi": "Punjabi",
    "Telugu": "Telugu",
    "Tamil": "Tamil",
}

def split_pdf(input_pdf, pages_per_part):
    pdf_document = fitz.open(input_pdf)
    total_pages = len(pdf_document)
    base_name = os.path.splitext(os.path.basename(input_pdf))[0]
    output_paths = []

    for i in range(0, total_pages, pages_per_part):
        part = fitz.open()
        for j in range(i, min(i + pages_per_part, total_pages)):
            part.insert_pdf(pdf_document, from_page=j, to_page=j)
        output_file = f"{base_name}_part{i//pages_per_part + 1}.pdf"
        part.save(output_file)
        output_paths.append(output_file)

    return output_paths

def extract_text_from_pdf(pdf_path):
    poppler_path = "/usr/bin"  # Poppler is system-installed in Docker
    pages = convert_from_path(pdf_path, poppler_path=poppler_path)
    full_text = ""
    for i, image in enumerate(pages):
        try:
            image = image.convert("RGB")
            text = pytesseract.image_to_string(image, lang='hin')
            full_text += f"--- Page {i+1} ---\n{text}\n"
        except Exception as e:
            full_text += f"[Error processing page {i+1}]: {str(e)}\n"
    return full_text

def chunk_text(text, max_words=1500):
    words = text.split()
    for i in range(0, len(words), max_words):
        yield ' '.join(words[i:i+max_words])

def translate_text(text, target_language):
    prompt_prefix = f"Translate the following text to {target_language}:\n\n"
    translated_chunks = []
    for chunk in chunk_text(text):
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo-16k",
                messages=[{"role": "user", "content": prompt_prefix + chunk}],
            )
            translated_chunks.append(response.choices[0].message.content.strip())
        except Exception as e:
            translated_chunks.append(f"[Error during translation: {e}]")
    return "\n\n".join(translated_chunks)

def main():
    st.title("Scanned PDF Translator (Hindi to Multiple Languages)")
    uploaded_file = st.file_uploader("Upload scanned Hindi PDF", type="pdf")
    target_lang = st.selectbox("Select target language", list(LANGUAGES.keys()))
    pages_per_part = st.number_input("Enter number of pages per split part", min_value=1, value=3, step=1)

    if uploaded_file and target_lang:
        os.makedirs("output", exist_ok=True)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.read())
            tmp_path = tmp_file.name

        st.info("Splitting PDF into parts...")
        split_files = split_pdf(tmp_path, pages_per_part)
        st.success("PDF file split successfully")

        st.info("Extracting and translating each part...")
        for idx, part_file in enumerate(split_files):
            text = extract_text_from_pdf(part_file)
            translated = translate_text(text, LANGUAGES[target_lang])
            txt_filename = f"output/Part{idx+1}.txt"
            with open(txt_filename, "w", encoding="utf-8") as f:
                f.write(translated)
            st.success(f"Saved: {txt_filename}")
            st.download_button(f"Download Part {idx+1} Translation", translated, file_name=f"Part{idx+1}.txt")

        # Combine all parts into a Word document
        docx_path = combine_txt_to_docx(txt_folder='output')
        with open(docx_path, "rb") as f:
            st.download_button("Download Combined Word File", f, file_name="final_translation.docx")

if __name__ == "__main__":
    main()
# # This code is a Streamlit app that allows users to upload a scanned Hindi PDF, split it into parts, extract text using OCR, translate it into a selected language, and download the translated text as a Word document.
# # The app uses PyMuPDF for PDF manipulation, pdf2image for converting PDF pages to images, pytesseract for OCR, and OpenAI's API for translation.
# # The app is designed to run in a Docker container, with the necessary dependencies installed.    