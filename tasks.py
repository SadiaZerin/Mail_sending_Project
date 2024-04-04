import os
import requests
import base64
import json
from email.message import EmailMessage
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from googleapiclient.errors import HttpError
from dotenv import load_dotenv
from validate_email import validate_email

load_dotenv()
  
def createAndSend_email_message(email,first_name,last_name):
     
            # Create an EmailMessage object
            message = EmailMessage()
            # Set the subject of the email
            message.set_content(f'Welcome, {first_name} {last_name}!')
            #message.set_content('Welcome to gmail')
            # Set the sender's email address
            message['Subject'] = 'Test Email'
            # Set the sender's email address
        
            message['From'] = 'sadiazerin99@gmail.com'
            # Set the recipient's email address
            message['To'] = email
            
            # Encode the message as bytes and encode it to a URL-safe base64 string
            data={'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}
           
      
             # Load credentials from token.json file
             with open('token.json', 'r') as token_file:
                 credentials_data = token_file.read()
         
             credentials = Credentials.from_authorized_user_info(json.loads(credentials_data))
         
             # Build Gmail service with provided credentials
             service = build('gmail', 'v1', credentials=credentials)
         
             # Send email
             try:
                sent_message = service.users().messages().send(userId='me', body=data).execute()
                print('Message sent successfully!')
                return True
             except HttpError as e:
                print(f'An error occurred while sending the email: {e}')

