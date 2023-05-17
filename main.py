import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

# Set up the Google Drive API client
def setup_drive_api_client(credentials_file):
    SCOPES = ['https://www.googleapis.com/auth/drive.file']
    creds = None

    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_file, SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build('drive', 'v3', credentials=creds)

# Upload an image file to Google Drive
def upload_image_to_drive(drive_service, image_path, folder_id=None):
    file_metadata = {
        'name': os.path.basename(image_path),
        'mimeType': 'image/png'
    }

    if folder_id:
        file_metadata['parents'] = [folder_id]

    media = MediaFileUpload(image_path, mimetype='image/png')

    try:
        file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        print(f'File ID: "{file.get("id")}".')
    except HttpError as error:
        print(f'An error occurred: {error}')
        file = None

    return file

def main():
    # Replace with the path to your downloaded JSON file
    CREDENTIALS_FILE = 'credentials.json'

    # Replace with the path to the image you want to upload
    IMAGE_PATH = 'example.png'

    # Optional: Replace with the ID of the folder you want to upload the image to
    FOLDER_ID = None

    drive_service = setup_drive_api_client(CREDENTIALS_FILE)
    upload_image_to_drive(drive_service, IMAGE_PATH, FOLDER_ID)

if __name__ == '__main__':
    main()