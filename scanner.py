import os
import mimetypes
from google import genai
from google.genai import types
from PIL import Image
from dotenv import load_dotenv

#1. Load the API key
load_dotenv()
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
    )

def extract_receipt_data(image_path):
    mime_type, _ = mimetypes.guess_type(image_path)
    
    with open(image_path, "rb") as f:
        file_data = f.read()

    media_content = types.Part.from_bytes(
        data = file_data,
        mime_type = mime_type
    )

    categories = ["Warmmiete","Sancks + Wants", "Krankenkasse","Rundfunkbeitrag","Handytarif","Abos","Lebensmittel","Eating out","Haushalt","Drogerie","Semesterbeitrag","Studienmaterialien","Bürokratie","Hobbies / Gaming","Sozial & Events","Kleidung","Geschenke","Reisen","Tech & Hardware","Schulden","Notfälle / Others"]

    #Prompt
    prompt = f"""
    Analyze this receipt. Look at every item. 
    Group items by these categories: {", ".join(categories)}.
    
    For each category found, return exactly one line in this format:
    ["DD.MM.YY", "Total for this category", "Items included", "Category Name"]
    
    Example output for a mixed receipt:
    ["03.04.26", "12,50", "Ingredients", "Lebensmittel"]
    ["03.04.26", "2,50", "Silverware", "Haushalt"]

    Please do not mention the following in Items Included:
    - Leergut
    - Pfand
    """

    response = client.models.generate_content(model = "models/gemini-3-flash-preview", contents=[prompt, media_content])

    import ast
    lines = response.text.strip().split('\n')
    print(lines)
    result = [ast.literal_eval(line) for line in lines]
    return result

def extract_text_data(text_list):

    categories = ["Warmmiete","Sancks + Wants", "Krankenkasse","Rundfunkbeitrag","Handytarif","Abos","Lebensmittel","Eating out","Haushalt","Drogerie","Semesterbeitrag","Studienmaterialien","Bürokratie","Hobbies / Gaming","Sozial & Events","Kleidung","Geschenke","Reisen","Tech & Hardware","Schulden","Notfälle / Others"]

    formatted_text = ""
    for item in text_list:
        formatted_text += f"Product: {item['name']}, Price: {item['price']}\n"

    #Prompt
    prompt = f"""
    I have manually written the items from a receipt.
    Categorize them into: {", ".join(categories)}.
    Return exactly one line per category found in this format:
    ["DD.MM.YY", "Total for category", "Items included", "Category Name"]

    Items: 
    {formatted_text}
    """

    response = client.models.generate_content(model = "models/gemini-3-flash-preview", contents=[prompt])
    return response.text


