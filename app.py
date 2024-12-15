import os
import mimetypes
import requests
from flask import Flask, request, jsonify
from markitdown import MarkItDown
from openai import OpenAI

app = Flask(__name__)

# Set up the path for supported files if necessary
SUPPORTED_FILE_EXTENSIONS = ['.pdf', '.docx', '.pptx', '.xlsx', '.html', '.txt', '.jpg', '.jpeg', '.png']

@app.route('/convert', methods=['POST'])
def convert():
    # Check if the file is provided via upload
    file = request.files.get('file')
    
    # Check if a URL is provided
    url = request.json.get('url')

    if file:
        # Handle file upload
        file_extension = os.path.splitext(file.filename)[1].lower()
        if file_extension not in SUPPORTED_FILE_EXTENSIONS:
            return jsonify({"error": "Unsupported file format"}), 400
        
        # Process file directly using MarkItDown
        client = OpenAI()  # Initialize the OpenAI client (e.g., GPT-4)
        md = MarkItDown(mlm_client=client, mlm_model="gpt-4")
        result = md.convert(file)

        return jsonify({"text_content": result.text_content})

    elif url:
        # Handle URL input
        try:
            response = requests.get(url)
            response.raise_for_status()

            # Detect MIME type
            mime_type, encoding = mimetypes.guess_type(url)
            if mime_type is None:
                return jsonify({"error": "Unable to detect MIME type for the URL content"}), 400

            # Process URL content using MarkItDown
            client = OpenAI()  # Initialize the OpenAI client (e.g., GPT-4)
            md = MarkItDown(mlm_client=client, mlm_model="gpt-4")
            result = md.convert_stream(response.content, mime_type=mime_type, url=url)

            return jsonify({"text_content": result.text_content})

        except requests.exceptions.RequestException as e:
            return jsonify({"error": f"Error fetching the URL: {str(e)}"}), 400

    else:
        return jsonify({"error": "No file or URL provided"}), 400


if __name__ == '__main__':
    app.run(debug=True)
