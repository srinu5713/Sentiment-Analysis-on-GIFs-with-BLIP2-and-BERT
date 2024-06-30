# -*- coding: utf-8 -*-
"""Sentiment_Analyisis_using_Bert.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1-Bs2t3c9Z4S18T6YXHJkAjIJB-unhEqi
"""

# Step 1: Import necessary libraries
import pandas as pd
import numpy as np
import torch
from torch.utils.data import TensorDataset, DataLoader, RandomSampler, SequentialSampler
from transformers import BertTokenizer, BertForSequenceClassification, AdamW, get_linear_schedule_with_warmup
from sklearn.model_selection import train_test_split
from tqdm import tqdm
from sklearn.preprocessing import LabelEncoder

# Step 2: Load the dataset
df = pd.read_csv('/content/drive/MyDrive/twitter_data.csv', encoding='ISO-8859-1', names=['target', 'ids', 'date', 'flag', 'user', 'text'])
df = df.sample(n=100000, random_state=42)

# Step 3: Preprocess the data
# Remove unnecessary columns
df = df[['target', 'text']]
# Map target values to 0, 1, 2 (assuming your target values are 0, 2, 4)
df['target'] = df['target'].map({0: 0, 2: 1, 4: 2})

# Step 4: Split the dataset into training and testing sets
train_texts, test_texts, train_labels, test_labels = train_test_split(df['text'], df['target'], test_size=0.2, random_state=42)

# Step 5: Tokenize and encode the text data
max_len = 64  # Maximum sequence length
max_words = 10000  # Maximum number of words in the tokenizer's vocabulary

# Tokenize the text data
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased', do_lower_case=True)

# Tokenize and encode the text data using BERT tokenizer
train_encodings = tokenizer(list(train_texts), truncation=True, padding=True, max_length=max_len, return_tensors='pt')
test_encodings = tokenizer(list(test_texts), truncation=True, padding=True, max_length=max_len, return_tensors='pt')

from sklearn.preprocessing import LabelEncoder

label_encoder = LabelEncoder()
train_labels_encoded = label_encoder.fit_transform(train_labels)
test_labels_encoded = label_encoder.transform(test_labels)

# Step 6: Create PyTorch datasets for BERT
train_dataset_bert = TensorDataset(train_encodings['input_ids'], train_encodings['attention_mask'], torch.tensor(train_labels_encoded))
test_dataset_bert = TensorDataset(test_encodings['input_ids'], test_encodings['attention_mask'], torch.tensor(test_labels_encoded))

batch_size_bert = 32
train_loader_bert = DataLoader(train_dataset_bert, batch_size=batch_size_bert, sampler=RandomSampler(train_dataset_bert))
test_loader_bert = DataLoader(test_dataset_bert, batch_size=batch_size_bert, sampler=SequentialSampler(test_dataset_bert))

# Step 8: Load the pre-trained BERT model for sequence classification
model_bert = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=3)

# Step 9: Set up optimizer and scheduler
optimizer_bert = AdamW(model_bert.parameters(), lr=2e-5, eps=1e-8)
epochs_bert = 3
total_steps_bert = len(train_loader_bert) * epochs_bert
scheduler_bert = get_linear_schedule_with_warmup(optimizer_bert, num_warmup_steps=0, num_training_steps=total_steps_bert)

# Step 10: Fine-tune BERT model
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model_bert.to(device)

for epoch in range(epochs_bert):
    model_bert.train()
    total_train_loss = 0

    for batch in tqdm(train_loader_bert, desc=f'Epoch {epoch + 1}', leave=False):
        input_ids = batch[0].to(device)
        attention_mask = batch[1].to(device)
        labels = batch[2].to(device)

        model_bert.zero_grad()
        outputs = model_bert(input_ids, attention_mask=attention_mask, labels=labels)
        loss = outputs.loss
        total_train_loss += loss.item()

        loss.backward()
        torch.nn.utils.clip_grad_norm_(model_bert.parameters(), 1.0)
        optimizer_bert.step()
        scheduler_bert.step()

    avg_train_loss = total_train_loss / len(train_loader_bert)
    print(f'Training loss: {avg_train_loss}')

# Step 8: Evaluate the model on the test set
from sklearn.metrics import accuracy_score, classification_report
from transformers import BertTokenizer
model_bert.eval()
predictions = []
true_labels = []

for batch in tqdm(test_loader_bert, desc='Evaluating'):
    input_ids = batch[0].to(device)
    attention_mask = batch[1].to(device)
    labels = batch[2]

    with torch.no_grad():
        outputs = model_bert(input_ids, attention_mask=attention_mask)

    logits = outputs.logits
    logits = logits.detach().cpu().numpy()
    predictions.extend(np.argmax(logits, axis=1))
    true_labels.extend(labels.numpy())

# Step 9: Calculate accuracy and other metrics
accuracy = accuracy_score(true_labels, predictions)
report = classification_report(true_labels, predictions, target_names=['Negative', 'Positive'])

print(f'Accuracy: {accuracy}')
print(report)

# Function for predicting sentiment of a given text
def predict_sentiment(text):
    encoded_text = tokenizer_bert.encode_plus(
        text,
        max_length=max_len,
        truncation=True,
        padding='max_length',
        return_tensors='pt'
    )
    input_ids = encoded_text['input_ids'].to(device)
    attention_mask = encoded_text['attention_mask'].to(device)

    with torch.no_grad():
        output = model_bert(input_ids, attention_mask=attention_mask)

    logits = output.logits
    predicted_class = torch.argmax(logits, dim=1).cpu().item()

    return label_encoder.classes_[predicted_class]

# Test the predict_sentiment function with user input
user_input = "I love this movie!"
predicted_sentiment = predict_sentiment(user_input)
print(f'User input: "{user_input}"')
print(f'Predicted sentiment: {predicted_sentiment}')

# Test the predict_sentiment function with user input
user_input = "I hate this movie!"
predicted_sentiment = predict_sentiment(user_input)
print(f'User input: "{user_input}"')
print(f'Predicted sentiment: {predicted_sentiment}')

# Test the predict_sentiment function with user input
# user_input = "I love the way that the movie sucks!"
user_input = "a group of people with red hair in the rain with water on them and a man with a red hair in the water with a woman in the water with a mana woman kneeling down in the rain near a graveyard with a tombstone in the background and a tombstone with a red head on it in the foreground with a red hat on ita man is standing in the mud with his hands on his head and his face covered in mud and dirt. he is wearing a black shirt and black pants.the scene from the movie the last man on earth with the man in the mud and the other man in the water with the other man in the water with the other man in the watera woman with red hair is being attacked by a group of people in the rain with water dripping down their faces and hair on their heads and faces. the woman is being attacked by a group of peoplea woman with red hair in the rain with a dog in the background and a man with a red shirt and a dog in the background in the rain with a dog "
predicted_sentiment = predict_sentiment(user_input)
print(f'User input: "{user_input}"')
print(f'Predicted sentiment: {predicted_sentiment}')

user_input = "a group of people with red hair in the rain with water on them and a man with a red hair in the water with a woman in the water with a man"
predicted_sentiment = predict_sentiment(user_input)
print(f'User input: "{user_input}"')
print(f'Predicted sentiment: {predicted_sentiment}')

user_input = "the scene from the movie the last man on earth with the man in the mud and the other man in the water with the other man in the water with the other man in the water"
predicted_sentiment = predict_sentiment(user_input)
print(f'User input: "{user_input}"')
print(f'Predicted sentiment: {predicted_sentiment}')

user_input = "the scene from the movie the last man on earth with the man in the mud and the other man in the water with the other man in the water with the other man in the water"
predicted_sentiment = predict_sentiment(user_input)
print(f'User input: "{user_input}"')
print(f'Predicted sentiment: {predicted_sentiment}')

user_input = "a woman with red hair in the rain with a dog in the background and a man with a red shirt and a dog in the background in the rain with a dog"
predicted_sentiment = predict_sentiment(user_input)
print(f'User input: "{user_input}"')
print(f'Predicted sentiment: {predicted_sentiment}')

user_input = "a man is standing in the mud with his hands on his head and his face covered in mud and dirt. he is wearing a black shirt and black pants."
predicted_sentiment = predict_sentiment(user_input)
print(f'User input: "{user_input}"')
print(f'Predicted sentiment: {predicted_sentiment}')

user_input = "a woman with red hair is being attacked by a group of people in the rain with water dripping down their faces and hair on their heads and faces. the woman is being attacked by a group of people"
predicted_sentiment = predict_sentiment(user_input)
print(f'User input: "{user_input}"')
print(f'Predicted sentiment: {predicted_sentiment}')

model_save_name = 'sentiment_BERT.pt'
path = F"/content/drive/MyDrive/{model_save_name}"
torch.save(model_bert.state_dict(), path)