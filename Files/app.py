from fastapi import FastAPI
from pydantic import BaseModel
from embed import search_similar_chunks
from dotenv import load_dotenv
import google.generativeai as genai
import os
import json
import re

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

# FastAPI app
app = FastAPI()

# Input format
class QueryRequest(BaseModel):
    query: str

@app.post("/api/v1/hackrx/run")
def run_query(data: QueryRequest):
    query = data.query

    # Step 1: Search Pinecone for relevant chunks
    chunks = search_similar_chunks(query)

    if not chunks:
        return {
            "decision": "Rejected",
            "amount": "₹0",
            "justification": "No relevant policy clauses found for this query."
        }

    # Step 2: Ask Gemini for a decision in structured JSON format
    prompt = f"""
You are a helpful insurance assistant.

The user has asked:
"{query}"

Here are relevant policy clauses from documents:
{chr(10).join(chunks)}

Based on this, return ONLY a valid JSON response in this format:

{{
  "decision": "Approved" or "Rejected",
  "amount": "₹<amount>",
  "justification": "Yes, knee surgery is covered under the policy." (or similar short sentence)
}}

✅ The justification should be:
- Short and human-friendly
- Similar to: "Yes, knee surgery is covered under the policy."
- Do NOT explain too much
- Do NOT include any extra explanation or text outside the JSON

Only return valid JSON.
"""

    try:
        response = model.generate_content(prompt)

        # Extract JSON from Gemini response
        json_match = re.search(r"\{[\s\S]*\}", response.text.strip())
        if json_match:
            return json.loads(json_match.group())
        else:
            return {
                "decision": "Rejected",
                "amount": "₹0",
                "justification": "LLM response was not in expected JSON format."
            }

    except Exception as e:
        return {
            "decision": "Rejected",
            "amount": "₹0",
            "justification": f"An error occurred while processing your request: {str(e)}"
        }
