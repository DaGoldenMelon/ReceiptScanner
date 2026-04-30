from flask import Flask, request, jsonify
import os
from scanner import extract_receipt_data, extract_text_data
from spreadsheet import appendToNextPosition
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route('/')
def home():
    return "Receipt Scanner API is running!"

@app.route('/scan', methods=['POST'])
def scan():
    # Frontend wil send photos labeled 'file'
    if "file" in request.files:
        file = request.files['file']
        if file.filename == "":
            return jsonify({"error": "No Data"}), 400

        file_path = os.path.join('/tmp', file.filename)
        file.save(file_path)

        processed_data = extract_receipt_data(file_path)
    
    data = request.get_json(silent=True)
    # Frontend will send manually entered data labeled 'items'
    if data and 'items' in data:
        item_list = data['items']

        processed_data = extract_text_data(item_list)
        
        return jsonify({"status": "success", "source": "manual_list", "data": processed_data}), 200

    return jsonify({"error": "Neither data types were received"}), 400

if __name__ == '__main__':
    app.run(debug=True)