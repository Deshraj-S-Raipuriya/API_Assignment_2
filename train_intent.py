from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForSequenceClassification, TrainingArguments, Trainer
import numpy as np
from sklearn.metrics import accuracy_score, f1_score

# 1️⃣ Load dataset
dataset = load_dataset('csv', data_files='my_intent_dataset.csv')

# 2️⃣ Map text labels to numeric ids
unique_labels = sorted(list(set(dataset['train']['label'])))
label2id = {label: i for i, label in enumerate(unique_labels)}
id2label = {i: label for label, i in label2id.items()}

# 3️⃣ Initialize tokenizer
tokenizer = AutoTokenizer.from_pretrained('distilbert-base-uncased')

# 4️⃣ Preprocess and tokenize the data
def preprocess_function(examples):
    tokens = tokenizer(
        examples['text'],
        padding='max_length',
        truncation=True,
        max_length=128
    )
    # Convert each label to integer
    tokens['labels'] = [label2id[l] for l in examples['label']]
    return tokens

# Apply preprocessing safely
encoded_dataset = dataset.map(preprocess_function, batched=True, remove_columns=dataset['train'].column_names)

# 5️⃣ Load pretrained model
model = AutoModelForSequenceClassification.from_pretrained(
    'distilbert-base-uncased',
    num_labels=len(unique_labels),
    id2label=id2label,
    label2id=label2id
)

# 6️⃣ Training configuration
args = TrainingArguments(
    output_dir='output_intent',
    per_device_train_batch_size=4,
    num_train_epochs=3,
    save_strategy='epoch',
    logging_dir='./logs',
    logging_strategy='epoch'
)

# 7️⃣ Define evaluation metrics
def compute_metrics(p):
    preds = np.argmax(p.predictions, axis=1)
    acc = accuracy_score(p.label_ids, preds)
    f1 = f1_score(p.label_ids, preds, average='weighted')
    return {'accuracy': acc, 'f1': f1}

# 8️⃣ Initialize trainer
trainer = Trainer(
    model=model,
    args=args,
    train_dataset=encoded_dataset['train'],
    eval_dataset=encoded_dataset['train'],  # demo only
    tokenizer=tokenizer,
    compute_metrics=compute_metrics,
)

# 9️⃣ Start training
trainer.train()

# 🔟 Save the fine-tuned model
model.save_pretrained('intent-model')
tokenizer.save_pretrained('intent-model')

print("✅ Fine-tuning complete! Model saved in 'intent-model' folder.")