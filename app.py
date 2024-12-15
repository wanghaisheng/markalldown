from flask import Flask, request, jsonify
from markitdown import MarkItDown
from openai import OpenAI

app = Flask(__name__)

@app.route('/convert', methods=['POST'])
def convert():
    file = request.files.get('file')
    if not file:
        return jsonify({"error": "No file provided"}), 400

    # Initialize MarkItDown with an optional MLM client (OpenAI)
    client = OpenAI()
    md = MarkItDown(mlm_client=client, mlm_model="gpt-4")

    # Convert the uploaded file
    result = md.convert(file)
    return jsonify({"text_content": result.text_content})

if __name__ == '__main__':
    app.run(debug=True)
