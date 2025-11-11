# rag_test.py 
from sentence_transformers import SentenceTransformer
import faiss, numpy as np, pickle
from openai import OpenAI
import os

# ✅ Initialize OpenAI client
client = OpenAI(api_key='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')

# ✅ Load embedding model and FAISS index
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
index = faiss.read_index("faiss_index.idx")
passages = pickle.load(open("passages.pkl", "rb"))

def retrieve(q, k=2):
    v = model.encode([q]).astype("float32")
    D, I = index.search(v, k)
    return [passages[i] for i in I[0]]

q = "How long till I get a refund?"
top = retrieve(q, k=2)

prompt = f"""You are a customer support assistant.

User question: {q}

Relevant knowledge base passages:
{chr(10).join(f"- {p}" for p in top)}

Based on the above, give a short, polite, and accurate answer.
"""

# ✅ New API call
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt},
    ],
    max_tokens=200
)

print("🔹 Final Answer:\n", response.choices[0].message.content)
