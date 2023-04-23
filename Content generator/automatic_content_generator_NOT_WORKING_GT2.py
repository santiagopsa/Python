import requests
from datetime import datetime, timedelta
from transformers import GPT2Tokenizer, GPT2LMHeadModel
from newsapi.newsapi_client import NewsApiClient
from random import randint
import torch

# Replace with your Medium access token
access_token = "23eb2d9a58670117daa4e707faa7168a61f7dbdf2c58a6af36809c8d44797f54f"

# Init
newsapi = NewsApiClient(api_key='507d16caf77344e3adc4c6936d505e58')

# The date for which you want to find the trending topics
date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

# /v2/top-headlines
all_headlines = newsapi.get_top_headlines(
                                      category='technology',
                                      language='en',
                                      page=1)

print(all_headlines)
print(type(all_headlines))
# Get the articles from the response
articles = all_headlines['articles']
number_results = int(all_headlines['totalResults'])
article_number = randint(0,10)
print(article_number)
# Get the trending topics
trending_topics = [article["title"].split(" ") for article in articles]

print(trending_topics)
print(" ".join(trending_topics[article_number]))


# Build the prompt using the trending topics and statistics, facts and information about the benefits and drawbacks
prompt = "Write a post about " + " and ".join(trending_topics[article_number]) + " including statistics, facts, and information about the benefits and drawbacks of the topic and their controversial aspects, explaining the different perspectives and opinions"

# Instantiate the model and tokenizer
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2")

prompt_tensor = torch.tensor([tokenizer.encode(prompt)])

# Create attention mask
attention_mask = torch.ones(prompt_tensor.shape[0], prompt_tensor.shape[1], dtype=torch.long)

# Generate text
generated_text = model.generate(prompt_tensor, attention_mask=attention_mask, pad_token_id = tokenizer.eos_token_id, max_length=500, top_p=0.9, top_k=40)


print(generated_text)
# Assign the content to title and body of the post
title = generated_text.split("\n")[0]
body = "\n".join(generated_text.split("\n")[1:])

# The data to send in the request
data = {
    "title": title,
    "contentFormat": "markdown",
    "content": body,
    "publishStatus": "public"
}

# The headers for the request
headers = {
    "Authorization": "Bearer " + access_token,
    "Content-Type": "application/json"
}

# The URL to send the request to
url = "https://api.medium.com/v1/users/me/posts"

# Send the request and get the response
response = requests.post(url, json=data, headers=headers)

# Print the response
print(response.json())
