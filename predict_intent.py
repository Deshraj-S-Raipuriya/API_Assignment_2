from transformers import pipeline

# Load fine-tuned model
nlp = pipeline('text-classification', model='intent-model')

# Test examples
tests = [
    "I want a refund for my order",
    "How can I reset my password?",
    "My app keeps crashing"
]

for t in tests:
    print(t, "->", nlp(t))
