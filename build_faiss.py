from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2')
passages = [
    'How to reset password?',
    'Refund policy for orders under 30 days',
    'How to contact technical support'
]
embs = model.encode(passages)
embs = np.array(embs).astype('float32')
index = faiss.IndexFlatL2(embs.shape[1])
index.add(embs)
# save index
faiss.write_index(index, 'faiss_index.idx')










