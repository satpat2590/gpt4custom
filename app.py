from flask import Flask, request, render_template
import openai

app = Flask(__name__)


# # Replace 'your_api_key' with your actual API key
openai.api_key = "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"

# # Set the model and other parameters
model = "gpt-4"  # Replace with the appropriate model version
max_tokens = 100

@app.route('/', methods=['GET', 'POST'])
def chat_gpt():
    if request.method == 'POST':
        document = request.form['document']
        query = request.form['query']
        answer = get_answer_from_gpt(document, query)
        return render_template('index.html', answer=answer)
    return render_template('index.html', answer=None)

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
