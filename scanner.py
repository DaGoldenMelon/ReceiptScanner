import os
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
    image = Image.open(image_path)
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

    response = client.models.generate_content(model = "models/gemini-3-flash-preview", contents=[prompt, image])

    import ast
    lines = response.text.strip().split('\n')
    print(lines)
    result = [ast.literal_eval(line) for line in lines]
    return result
    
