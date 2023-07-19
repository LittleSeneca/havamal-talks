import PyPDF2
import openai
import os
import time
import json

# Set up your OpenAI API credentials
openai.api_key = os.getenv('OAI_TOKEN')

# Save the summaries to a file
def save_summaries(summaries):
    with open('summaries.json', 'w') as f:
        json.dump(summaries, f)

# Load the summaries from a file
def load_summaries():
    with open('summaries.json', 'r') as f:
        summaries = json.load(f)
    return summaries

# Function to generate summary using OpenAI's ChatCompletion API
def generate_summary(chunks):
    # Check if summaries.json file exists
    if os.path.exists('summaries.json'):
        summaries = load_summaries()
        start = len(summaries)
    else:
        summaries = []
        start = 0

    for i in range(start, len(chunks)):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant. Your job is to review the content provided and summarize what it's talking about in just a few sentences."},
                {"role": "user", "content": chunks[i]}
            ]
        )
        message = response['choices'][0]['message']
        summaries.append(message['content'])
        save_summaries(summaries)
        print(f"Summarized chunk {i+1} of {len(chunks)}")
        time.sleep(2)
    return summaries

# Load the PDF document
def read_pdf(file_path):
    with open(file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        num_pages = len(pdf_reader.pages)
        chunks = []
        
        # Iterate over the pages and create chunks of text
        for page_num in range(num_pages):
            page = pdf_reader.pages[page_num]
            text = page.extract_text()
            chunks.append(text)
        
        # Generate summaries for each chunk
        summaries = generate_summary(chunks)
        
        return summaries

# Function to generate a bulleted list of primary functionalities
def generate_bullet_list(summaries):
    for i, summary in enumerate(summaries):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant. Extract the primary functionalities from the summary and list them as bullet points."},
                {"role": "user", "content": summary}
            ]
        )
        message = response['choices'][0]['message']
        print(f"Processed summary {i+1} of {len(summaries)}")
        # Add a delay here
        time.sleep(2)
        yield message['content']

# Provide the file path to your PDF document
file_path = 'document.pdf'

# Read the PDF document and generate summaries
summaries = read_pdf(file_path)

# Create an array to store the summaries
summary_results = []

# Add the summaries to the array
for i in range(0, len(summaries), 5):
    summary_group = " ".join(summaries[i:i+5])
    summary_results.append(summary_group)

# Generate the bulleted list
bullet_list = list(generate_bullet_list(summary_results))

# Print the bulleted list
for bullet in bullet_list:
    print(bullet)
