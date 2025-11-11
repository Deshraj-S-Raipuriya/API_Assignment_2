# intent_test.py
from transformers import pipeline

# If you have a local fine-tuned model: model="intent-model"
# Otherwise use a pretrained sentiment model just to test pipeline:
model = "intent-model"  # or "distilbert-base-uncased-finetuned-sst-2-english"
nlp = pipeline("text-classification", model=model, return_all_scores=False)

tests = [
    "I want a refund for my last purchase",
    "My app crashes when I open it",
    "How do I upgrade to premium?",
    "Where can I track my order?"
]

for t in tests:
    out = nlp(t)
    print(t, "->", out)
