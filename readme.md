python -m venv venv

curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py

python get-pip.py

pip install -r  requirements.txt  


# Get Api keys
# Open Api key

https://platform.openai.com/docs/overview

#hugging face portal
https://huggingface.co/


# prepare env
pip install transformers datasets accelerate

# example trainer script (train_intent.py) - use Hugging Face 
python train_intent.py --model distilbert-base-uncased --data my_intent_dataset.csv
