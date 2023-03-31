import os
import PyPDF2
from bs4 import BeautifulSoup
from flask import Flask, request, render_template
import openai
from io import StringIO
from functools import partial

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
        return render_template('index.html', user_query=answer)
    return render_template('index.html', user_query=None)

def extract_text_from_file(file):
    file_ext = os.path.splitext(file.filename)[-1].lower()
    text = ""
    
    if file_ext == '.txt':
        text = file.read().decode('utf-8')
    elif file_ext == '.pdf':
        pdf_reader = PyPDF2.PdfReader(file)
        pdf_text = StringIO()
        for page_num in range(len(pdf_reader.pages)):
            pdf_text.write(pdf_reader.pages[page_num].extract_text())
        text = pdf_text.getvalue()
    elif file_ext == '.html':
        html_content = file.read().decode('utf-8')
        soup = BeautifulSoup(html_content, 'html.parser')
        text = soup.get_text()
    
    return text

def split_text_into_chunks(text, chunk_size):
    tokens = text.split()
    return [" ".join(tokens[i:i + chunk_size]) for i in range(0, len(tokens), chunk_size)]

def get_answer_from_gpt(document, query):
    # Calculate the maximum tokens allowed for the input document (reserve tokens for query and answer)
    max_input_tokens = 4096 - len(query) - 50  # Reserve 50 tokens for the answer
    chunk_size = max_input_tokens // 4  # Roughly estimate the number of words per chunk

    # Split the document into smaller chunks that fit within the token limit
    document_chunks = split_text_into_chunks(document, chunk_size)

    # Process each chunk separately and collect the answers
    answers = []
    for chunk in document_chunks:
        prompt = f"Document: {chunk}\nQuestion: {query}\nAnswer:"
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=50,
            n=1,
            stop=None,
            temperature=0.5,
        )
        answer = response.choices[0].text.strip()
        answers.append(answer)

    # Combine the answers into a single response
    combined_answer = " ".join(answers)
    return combined_answer



if __name__ == '__main__':
    app.run(debug=True)




