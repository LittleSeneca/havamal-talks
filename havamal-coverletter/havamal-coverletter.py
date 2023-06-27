import openai
import os
import PyPDF2

openai.api_key = os.getenv('OAI_TOKEN')

source_resume = "resume.pdf"
source_application = "application.txt"

with open(source_application, "r") as file:
    application_content = file.read()

def load_content_from_pdf(file_path):
    content = ''
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        num_pages = len(reader.pages)
        for page_number in range(num_pages):
            page = reader.pages[page_number]
            content += page.extract_text()
    return content

document_content = load_content_from_pdf(source_resume)

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a applicant for a job"},
        {"role": "user", "content": f"Here is my resume: {document_content} \n And here is the job description: {application_content} \n Using this information, please craft me a 4 paragraph cover letter. Please make sure to reference how the skills in the resume match the application."}
    ]
)
encoded_response = response["choices"][0]["message"]["content"]
# Print the vulnerability descriptions
print(encoded_response, end='\n')