# build_faiss.py
from sentence_transformers import SentenceTransformer
import faiss, numpy as np
passages = [
  "You can reset your password from Settings -> Account -> Reset Password.",
  "Refunds are processed within 7 business days.",
  "Contact sales at sales@example.com for enterprise plans."
]
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
embs = model.encode(passages, convert_to_numpy=True).astype("float32")
index = faiss.IndexFlatL2(embs.shape[1])
index.add(embs)
faiss.write_index(index, "faiss_index.idx")
import pickle
pickle.dump(passages, open("passages.pkl","wb"))
print("index built")
