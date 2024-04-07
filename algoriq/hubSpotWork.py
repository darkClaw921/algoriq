import requests
from dotenv import load_dotenv
import logging
load_dotenv()
import os

HUBSPOT_API_KEY = os.getenv('YOUR_HUBSPOT_API_KEY')

def create_hubspot_lead(email):
    url = f"https://api.hubapi.com/contacts/v1/contact/createOrUpdate/email/{email}/"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {HUBSPOT_API_KEY}"
    }
    data = {
        "properties": [
            {
                "property": "email",
                "value": email
            }
        ]
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        logging.info(f"Lead created for email: {email}")
    else:
        logging.error(f"Failed to create lead. Status code: {response.status_code}, Response: {response.text}")
