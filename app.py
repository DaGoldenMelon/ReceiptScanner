from flask import Flask, request, jsonify
from scanner import extract_receipt_data
from spreadsheet import appendToNextPosition

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_file():
    # Logic to receive the image from your phone
    return jsonify({"status": "success"})