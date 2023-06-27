import requests
import json
import openai
import os
import time
from datetime import datetime, timedelta
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(body):
    # Create message container
    msg = MIMEMultipart()
    msg['From'] = os.getenv('SENDER_EMAIL')
    msg['To'] = os.getenv('RECIPIENT_EMAIL')
    msg['Subject'] = os.getenv('EMAIL_SUBJECT')

    # Attach the body of the message
    msg.attach(MIMEText(body, 'plain'))

    # Try to send the email
    try:
        server = smtplib.SMTP(os.getenv('SMTP_SERVER'), int(os.getenv('SMTP_PORT')))
        server.starttls()
        server.login(os.getenv('SMTP_USERNAME'), os.getenv('SMTP_PASSWORD'))
        text = msg.as_string()
        server.sendmail(msg['From'], msg['To'], text)
        server.quit()
        print('Email sent!')
    except Exception as e:
        print('Failed to send email:', e)

openai.api_key = os.getenv('OAI_TOKEN')
cvssv3Severity = os.getenv('CVSS_SEVERITY')
timeconstraint = os.getenv('TIME_CONSTRAINT')

current_date = datetime.now()
previous_day = current_date - timedelta(days=int(timeconstraint))

previous_day_iso8601 = previous_day.date().isoformat()
current_day_iso8601 = current_date.date().isoformat()

url = f"https://services.nvd.nist.gov/rest/json/cves/2.0?cvssV3Severity={cvssv3Severity}&pubStartDate={previous_day_iso8601}T00:00:00.000&pubEndDate={current_day_iso8601}T00:00:00.000"

payload = {}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)

# Format the response text as pretty JSON
json_response = json.loads(response.text)

filtered_results = [
    vulnerability["cve"] for vulnerability in json_response["vulnerabilities"]
]

# Configure OpenAI API

# Make the API request to NVD for vulnerabilities
# (Your existing code here to fetch the vulnerabilities)

# Prepare a list to store the vulnerability descriptions
descriptions = []

# Iterate over each vulnerability
for vulnerability in filtered_results:
    time.sleep(5)
    # Extract relevant information from the vulnerability
    cve_id = vulnerability["id"]
    source_identifier = vulnerability["sourceIdentifier"]
    published = vulnerability["published"]
    last_modified = vulnerability["lastModified"]
    vuln_status = vulnerability["vulnStatus"]
    description = vulnerability["descriptions"][0]["value"]
    cvss_metric = vulnerability["metrics"]["cvssMetricV31"][0]["cvssData"]
    exploitability_score = vulnerability["metrics"]["cvssMetricV31"][0]["exploitabilityScore"]
    impact_score = vulnerability["metrics"]["cvssMetricV31"][0]["impactScore"]

    # assuming 'published' variable is a string like '2023-05-21T23:15:08.960'
    published_date = datetime.fromisoformat(published.replace("Z", ""))

    # Now, let's format it in a more human readable format
    formatted_date = published_date.strftime('%B %d, %Y, %H:%M:%S')
    
    # Generate a paragraph description using OpenAI GPT-3.5 API
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a Cyber Security Expert"},
            {"role": "user", "content": f"Provide a detailed  explanation of the description provided here, focusing on the specific componants listed in the advisory: {description} \n and incorporate the CVSS Metrics provided here: {json.dumps(cvss_metric, indent=4)} \n Also, if their is a keyword describing the type of exploit made possible by the vulnerability (Like a use after free or buffer overflow), please provide a brief explanation of what the keyword does in the context of the original description"}
        ]
    )
    def get_friendly_metric_name(metric):
        mappings = {
            "version": "CVSS Version",
            "vectorString": "Vector String",
            "attackVector": "Attack Vector",
            "attackComplexity": "Attack Complexity",
            "privilegesRequired": "Privileges Required",
            "userInteraction": "User Interaction",
            "scope": "Scope",
            "confidentialityImpact": "Confidentiality Impact",
            "integrityImpact": "Integrity Impact",
            "availabilityImpact": "Availability Impact",
            "baseScore": "Base Score",
            "baseSeverity": "Base Severity"
        }
        return mappings.get(metric, metric)

    friendly_cvss_metric = {get_friendly_metric_name(k): v for k, v in cvss_metric.items()}

    output_string = "\nCVSS Metrics:"
    for key, value in friendly_cvss_metric.items():
        output_string += f"\n    {key}: {value}"
    # Extract the generated description from the API response
    generated_description = f"CVE-ID: {cve_id}"
    generated_description += f"\nPublish Date: {formatted_date}"
    generated_description += f"\n"
    generated_description += f"\nFormal Description: \n {description}"
    generated_description += f"\n"
    generated_description += f"\nMy Interpretation: \n {response.choices[0].message.content}"
    generated_description += f"\n"
    generated_description += f"\n{output_string}"
    generated_description += f"\n"
    # Explain key terms mentioned in the description
    # (Your code here to explain key terms, using appropriate APIs or techniques)
    
    descriptions.append(generated_description)

# Print the vulnerability descriptions
final_string = ""
for i, description in enumerate(descriptions):
    time.sleep(5)
    response_filtered = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are one of the following comedians: Dave Chappelle, Gabriel Iglesias, Chris Rock, or Aziz Ansari"},
            {"role": "user", "content": f"Using everything provided in the full context below, please expand the 'My Interpretation' section to make it more funny and informative: \n {description} \n\n Do not include the line 'My Interpretation: in your response'. Also, please do not use your own name in the response."}
        ]
    )
    message_content = response_filtered["choices"][0]["message"]["content"]

    # Get the required details from the original description
    cve_id = description.split('\n')[0].split(': ')[1]
    publish_date = description.split('\n')[1].split(': ')[1]
    formal_description = description.split('Formal Description: \n ')[1].split('\n')[0]
    cvss_metrics = description.split('CVSS Metrics:')[1].split('\nMy Interpretation: ')[0]
    
    # Prepare the final message
    cve_message = f"CVE-ID: {cve_id}\nPublish Date: {publish_date}\n\nFormal Description: \n{formal_description}\n\nExpanded Interpretation (Provided by ChatGPT): \n{message_content}\n\nCVSS Metrics:{cvss_metrics}\n"
    final_string += cve_message
    print("Email Sent")
    send_email(final_string)