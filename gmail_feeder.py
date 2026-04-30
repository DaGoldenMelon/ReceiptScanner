import os
import io
import base64
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def get_gmail_service():
    creds = None
    # The file token.json stores the user's access and refresh tokens
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Use your new credentials file here!
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials_gmail.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return build('gmail', 'v1', credentials=creds)

def search_netto_receipts(service):
    # We search specifically for your label
    query = 'label:NettoKassenbon newer_than:1d'
    
    results = service.users().messages().list(userId='me', q=query).execute()
    messages = results.get('messages', [])
    return messages

def download_pdf_attatchment(service, message_id):
    # 1. Get the full message details
    message = service.users().messages().get(userId='me', id=message_id).execute()
    payload = message.get('payload', {})
    parts = payload.get('parts', [])

    for part in parts:
        if part.get('filename') and part.get('filename').endswith('.pdf'):
            attachment_id = part['body']['attachmentId']
            attachment = service.users().messages().attachments().get(
                userId='me', messageId=message_id, id=attachment_id).execute()
            
            # Decode the base64 data
            data = attachment.get('data')
            file_data = base64.urlsafe_b64decode(data.encode('UTF-8'))

            # Save the file locally for a second
            file_path = f"temp_receipt_{message_id}.pdf"
            with open(file_path, 'wb') as f:
                f.write(file_data)
            
            print(f"Success! PDF saved as {file_path}")
            return file_path
    return None

def main():
    service = get_gmail_service()

    messages = search_netto_receipts(service)

    if not messages:
        print("No receipts found.")
    else:
        print(f"Found {len(messages)} messages in 'NettoKassenbon'!")

    file_path = download_pdf_attatchment(service, messages[0]['id'])

if __name__ == '__main__':
    main()