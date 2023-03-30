import os
import PyPDF2
from bs4 import BeautifulSoup
from flask import Flask, request, render_template
import openai

app = Flask(__name__)

# Retrieve the API key
openai.api_key = os.environ.get('OPENAI_API_KEY')

# # Set the model and other parameters
model = "gpt-4"  # Replace with the appropriate model version
max_tokens = 100

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
    prompt = f"{document}\n\nQuestion: {query}\nAnswer:"

    response = openai.Completion.create(
        engine=model,
        prompt=prompt,
        max_tokens=max_tokens,
    )
    generated_text = response.choices[0].text.strip()
    return generated_text

if __name__ == '__main__':
    app.run(debug=True)

