# havamal-talks
This Repo is designed to save you time.
## NVD Content
### Purpose
This project is designed to provide a list of CVEs catagorized by NIST. The listed CVEs are then pushed through chatGPT to provide a commical, yet instructional summary, along with all the relevant CVSS scoring details. The tool can be ran either ad hoc through the terminal, or deployed as a one time use, trigger based docker container. 

#### Local Deployment Dependancies
This project requires the following non-default modules:

* requests
* openai
* datetime

To install these items, please deploy them with 
~~~~
pip3 install requests openai datetime
~~~~
#### Local Deployment Environmental Variables
To deploy this script, you first have to set your environmental variables. These variables are listed below:

* TIME_CONSTRAINT="Number of Days from current measured back in time to track NVD data"
    - example: export TIME_CONSTRAINT=1
* CVSS_SEVERITY="Priority of the Data Provided"
    - example: export CVSS_SEVERITY="CRITICAL"
    - example: export CVSS_SEVERITY="HIGH"
    - example: export CVSS_SEVERITY="MEDIUM"
    - example: export CVSS_SEVERITY="LOW"
* OAI_TOKEN="OpenAi API Token"
    - example: export OAI_TOKEN="you can build your own by making an API account with openAI"

#### Running the Local Deployment

To deploy this script, just run "python3 havamal-nvd-local.py" after you have set all your local environmental variables from within the havamal-nvd folder. 

#### Docker Deployment Environmental Variables
To deploy this script, you first have to set your docker environmental variables. These variables are listed below:

* TIME_CONSTRAINT="Number of Days from current measured back in time to track NVD data"
* CVSS_SEVERITY="Priority of the Data Provided"
* SMTP_SERVER="SMTP Server adderss"
* SENDER_EMAIL="SMPT Email Address"
* RECIPIENT_EMAIL="Recipient Email Address"
* OAI_TOKEN="OpenAi API Token"
* SMTP_PORT="SMTP Port"
* SMTP_PASSWORD="SMTP Password"
* SMTP_USERNAME="SMTP Username"
* EMAIL_SUBJECT="Email Subject Line"

#### Building the Docker Container

For my usecase, I built a scheduled container deployment using AWS Elastic Container Service.

To build the docker container, simple run the following command "docker build ." from within the havamal-nvd folder

## Cover Letter Builder
### Purpose
The purpose of this cover letter builder is to help you simplify the process of applying to jobs. Cover Letters are stupid and irrelevant. Rather than trying to write a non-generic cover letter every time you apply to a job, let chatgpt do it for you.

### Local Deployment Dependancies
This project requires the following non-default modules:

* openai
* PyPDF2

To install these items, please deploy them with
~~~~
pip3 install requests openai pypdf2
~~~~

### Building the Local Deployment
1. Write your resume, in a format that does not use any special formatting (so chatgpt can read it)
2. Place your resume in the havamal-coverletter folder, and name it resume.pdf (make sure you export your resume in pdf format)
3. Copy and paste the job application you are applying to as a txt document named application.txt, and then add that to the havamal-coverletter folder. 
4. run the following command: "python3 havamal-coverletter.py
5. Watch your cover letter print out on the screen!
