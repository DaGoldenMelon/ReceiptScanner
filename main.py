from scanner import extract_receipt_data
from spreadsheet import findNextPosition, appendToNextPosition

def run_app():
    image_path = "Netto_Kassenbon_20260413-173132.pdf"
    lines = extract_receipt_data(image_path)

    for line in lines:
        nextPos = findNextPosition()
        appendToNextPosition(line, nextPos)


if __name__ == "__main__":
    run_app()