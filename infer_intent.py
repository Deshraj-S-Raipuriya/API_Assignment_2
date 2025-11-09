from transformers import pipeline

# assume we uploaded a fine-tuned model to HF hub or local path 'intent-model'
nlp = pipeline('text-classification', model='intent-model')

def predict_intent(text: str):
    out = nlp(text)
    # out example: [{'label': 'LABEL_1', 'score': 0.98}]
    return out[0]

if __name__ == '__main__':
    print(predict_intent('I want a refund for my last purchase'))
