import os
from extract import extract_text_from_pdf
from embed import chunk_text, upload_to_pinecone

# Set folder path for all your PDFs
folder_path = "data/policies"

# List all PDF files
pdf_files = [f for f in os.listdir(folder_path) if f.endswith(".pdf")]

for pdf_file in pdf_files:
    file_path = os.path.join(folder_path, pdf_file)
    doc_id = os.path.splitext(pdf_file)[0]  # Use filename as ID (without .pdf)

    print(f"\n📄 Processing: {pdf_file}")

    # Extract text
    text = extract_text_from_pdf(file_path)
    print("✅ Text extracted.")

    # Chunk text
    chunks = chunk_text(text)
    print(f"✅ {len(chunks)} chunks created.")

    # Upload to Pinecone
    upload_to_pinecone(doc_id, chunks)
    print("✅ Uploaded to Pinecone.")
