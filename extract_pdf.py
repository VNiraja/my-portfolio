from pdfminer.high_level import extract_text

try:
    text = extract_text("resume (1).pdf")
    with open("resume_text.txt", "w", encoding="utf-8") as f:
        f.write(text)
    print("Text extraction complete.")
except Exception as e:
    print(f"Error extracting text: {e}")
