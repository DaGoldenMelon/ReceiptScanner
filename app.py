from flask import Flask, request, jsonify
import os
from scanner import extract_receipt_data
from spreadsheet import appendToNextPosition
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route('/')
def home():
    return "Receipt Scanner API is running!"

@app.route('/scan', methods=['POST'])
def scan():
    # We will expand this to handle image uploads from Android later!
    return jsonify({"message": "Endpoint ready for Android images"}), 200

if __name__ == '__main__':
    app.run(debug=True)