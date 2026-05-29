import torch
from transformers import BertTokenizer, BertForSequenceClassification
from torch.utils.data import Dataset
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


# Define a class for the custom dataset
class NewsDataset(Dataset):
    def __init__(self, texts, labels, tokenizer, max_length=128):
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        text = self.texts[idx]
        label = self.labels[idx]
        encoding = self.tokenizer.encode_plus(
            text,
            add_special_tokens=True,
            max_length=self.max_length,
            padding='max_length',
            truncation=True,
            return_attention_mask=True,
            return_tensors='pt',
        )
        return {
            'input_ids': encoding['input_ids'].flatten(),
            'attention_mask': encoding['attention_mask'].flatten(),
            'label': torch.tensor(label, dtype=torch.long)
        }


# Function to load the dataset
def load_dataset(file_path):
    df = pd.read_csv(file_path, encoding='utf-8', on_bad_lines='skip')
    texts = df['content'].tolist()  # Assuming 'content' column contains the news text
    labels = df['label'].tolist()  # Assuming 'label' column contains the fake/real labels (0 or 1)
    return texts, labels


# Model inference function
def predict(news_content):
    # Load pre-trained model and tokenizer
    model = BertForSequenceClassification.from_pretrained(r'train_model\roberta_trained_model')
    tokenizer = BertTokenizer.from_pretrained(r'train_model\roberta_trained_model')

    # Tokenize the input news content
    inputs = tokenizer(news_content, return_tensors="pt", padding=True, truncation=True, max_length=128)
    model.eval()

    # Make predictions
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        probs = torch.nn.functional.softmax(logits, dim=-1)
        return probs.squeeze().tolist()  # Return probabilities

