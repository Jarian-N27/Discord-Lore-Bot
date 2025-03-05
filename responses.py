# Import necessary libraries
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import requests
import spacy
import os
import yaml
import re
from openai import OpenAI

# Load SpaCy model
nlp = spacy.load("en_core_web_sm")

# Load OpenAI API key

load_dotenv()
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

# Load URLs from the YAML file
def load_urls(yaml_path='fandom_urls.yaml'):
    with open(yaml_path, 'r') as file:
        return yaml.safe_load(file)
    
# Scrape sites for lore using a web scraping function
def scrape_lore(fandom_url):
    response = requests.get(fandom_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Scrape all paragraphs
    paragraphs = soup.find_all('p')
    lore_text = '\n'.join([para.text for para in paragraphs])
    
    return lore_text

# Clean the text
def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\n+', '\n', text)
    return text

# Format the text
def format_text(text):
    paragraphs = text.split('\n\n')
    formatted_text = '\n\n'.join(paragraphs)
    return formatted_text

# Summarize text using OpenAI
def openai_summarize(text):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Please summarize the following text:\n\n{text}"}
        ],
        max_tokens=150,
        temperature=0.8,
    )
    summary = response.choices[0].message.content
    return summary

# Cache lore data
def cache_lore_data(fandom_urls, cache_path='lore_cache.yaml'):
    if os.path.exists(cache_path):
        with open(cache_path, 'r') as cache_file:
            lore_data = yaml.safe_load(cache_file)
    else:
        lore_data = {}

    for fandom, url in fandom_urls.items():
        if fandom not in lore_data:
            lore_data[fandom] = scrape_lore(url)

    with open(cache_path, 'w') as cache_file:
        yaml.safe_dump(lore_data, cache_file)
    return lore_data

# Load and cache lore data
fandom_urls = load_urls('fandom_urls.yaml')
lore_data = cache_lore_data(fandom_urls)

def process_question(question, lore_data):
    question = question.lower()
    
    for keyword in lore_data:
        if keyword in question:
            raw_text = lore_data[keyword]
            cleaned_text = clean_text(raw_text)
            formatted_text = format_text(cleaned_text)
            
            # Summarize the cleaned and formatted text using OpenAI
            summarized_text = openai_summarize(formatted_text)
            
            return summarized_text
    
    return "I'm sorry, I don't have information on that topic. Please try asking about something else!"
