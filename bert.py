# Torch ML libraries
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

"""
    Argument:
        Single Text(String) 

    Returns:
        Returns emotion(String)
"""

# Local path to the fine-tuned BERT model
MODEL_PATH = 'bert-sentilytics'

# Load the tokenizer and model from the local directory
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)

# Sentiment analysis function
def bert_sentiment(review_text):
    # Tokenize the input text
    inputs = tokenizer(review_text, return_tensors="pt", truncation=True, padding=True)
    
    # Perform inference
    with torch.no_grad():
        outputs = model(**inputs)
    
    # Get the predicted class
    probabilities = torch.nn.functional.softmax(outputs.logits, dim=-1)
    predicted_class = torch.argmax(probabilities, dim=1).item()
    
    # Map the predicted class to sentiment categories
    # Model output: 0 = 1-star, 1 = 2-stars, ..., 4 = 5-stars
    if predicted_class in [0, 1]:  # 1-star and 2-star reviews are Negative
        return "NEGATIVE"
    elif predicted_class == 2:    # 3-star reviews are Neutral
        return "NEUTRAL"
    elif predicted_class in [3, 4]:  # 4-star and 5-star reviews are Positive
        return "POSITIVE"

text = "I love this fucking asshole!"
print("Sentiment:", bert_sentiment(text))