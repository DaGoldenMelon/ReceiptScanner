from flask import Flask, request, jsonify
from scanner import extract_receipt_data, extract_text_data  # Import your Gemini logic
from spreadsheet import findNextPosition, appendToNextPosition # Import Sheets logic
import os

app = Flask(__name__)

@app.route('/scan', methods=['POST'])
def scan_receipt():
    if request.is_json:
        data = request.get_json()
        receipt_lines = extract_text_data(data.get('text_list', []))

    elif 'file' in request.files:
        file = request.files['file']
        file_path = os.path.join("/tmp", file.filename)
        file.save(file_path)

        receipt_lines = extract_receipt_data(file_path)
        os.remove(file_path)
    
    else:
        return jsonify({"error": "No file uploaded"}), 400

    try:
        for line in receipt_lines:
            next_pos = findNextPosition()
            appendToNextPosition(line, next_pos)

        return jsonify({"status": "success", "message": "Receipt processed!"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500