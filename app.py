import os
import PyPDF2
from bs4 import BeautifulSoup
from flask import Flask, request, render_template
import openai

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def chat_gpt():
    if request.method == 'POST':
        document_file = request.files['document']
        query = request.form['query']
        document_text = extract_text_from_file(document_file)
        answer = get_answer_from_gpt(document_text, query)
        return render_template('index.html', answer=answer)
    return render_template('index.html', answer=None)

def extract_text_from_file(document_file):
    file_extension = os.path.splitext(document_file.filename)[1].lower()
    text = ""

    if file_extension == '.txt':
        text = document_file.read().decode('utf-8')
    elif file_extension == '.pdf':
        with PyPDF2.PdfFileReader(document_file) as pdf_reader:
            for page_num in range(pdf_reader.numPages):
                text += pdf_reader.getPage(page_num).extractText()
    elif file_extension == '.html':
        soup = BeautifulSoup(document_file.read(), 'html.parser')
        text = soup.get_text()

    return text

def get_answer_from_gpt(document, query):
    # Replace this with the actual API call to GPT-4
    # and return the answer based on the document and query.
    return "This is a sample answer."

if __name__ == '__main__':
    app.run(debug=True)

