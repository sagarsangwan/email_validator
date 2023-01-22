#Email Validation API

A simple Flask API that takes an email address as input in a GET request on the homepage, checks if the supplied email is valid, looks up the MX records and tries to use them to connect to the SMTP server. If any of the steps fail, the program automatically outputs a negative response.

##Getting Started

####Prerequisites
-Python 3.x
-Flask
-dnspython
-smtplib

####Installing
1. Clone the repository: git clone https://github.com/sagarsangwan/email-validation-api.git
2. Install the required packages: pip install -r requirements.txt


####Usage
1. Clone the repository
2. Run the app.py file
3. Open a browser and go to http://localhost:5000/email=
4. The API will return a JSON object with the status of the email validation, either "valid" or "invalid". If any errors occur, an "error" field will be present in the JSON object with a description of the error.
