from transformers import pipeline

# Load fine-tuned model
nlp = pipeline('text-classification', model='intent-model')

# Test examples
tests = [
    "I was charged twice for my order #12345"
]

for t in tests:
    print(t, "->", nlp(t))