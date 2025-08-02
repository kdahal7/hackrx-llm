import os
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone, ServerlessSpec

# Load environment variables
load_dotenv()

# Load Pinecone credentials
api_key = os.getenv("PINECONE_API_KEY")
env = os.getenv("PINECONE_ENV")
index_name = os.getenv("PINECONE_INDEX")

# Connect to Pinecone
pc = Pinecone(api_key=api_key)
index = pc.Index(index_name)

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Split text into chunks
def chunk_text(text, chunk_size=500):
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

# Upload chunks to Pinecone
def upload_to_pinecone(doc_id, chunks):
    vectors = []
    for i, chunk in enumerate(chunks):
        vector = model.encode(chunk).tolist()
        vectors.append({
            "id": f"{doc_id}-{i}",
            "values": vector,
            "metadata": {"text": chunk}
        })
    index.upsert(vectors=vectors)

# Search similar chunks
def search_similar_chunks(query, top_k=3):
    vector = model.encode(query).tolist()
    result = index.query(vector=vector, top_k=top_k, include_metadata=True)
    return [match["metadata"]["text"] for match in result["matches"]]
