import os.path

import google.auth
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/drive.file"]

def upload(video_name, video_title):
  """Shows basic usage of the Drive v3 API.
  Prints the names and ids of the first 10 files the user has access to.
  """
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("cloud/token_drive.json"):
    creds = Credentials.from_authorized_user_file("cloud/token_drive.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "cloud/credentials_drive.json", SCOPES
      )
      creds = flow.run_local_server(domain="localhost", port=60880)
    # Save the credentials for the next run
    with open("cloud/token_drive.json", "w") as token:
      token.write(creds.to_json())

  try:
    service = build("drive", "v3", credentials=creds)

    # create drive api client
    file_metadata = {"name": video_title}
    media = MediaFileUpload(video_name, mimetype="video/mp4")
    
    file = (
        service.files()
        .create(uploadType="media", body=file_metadata, media_body=media, fields="id").execute()
    )

    request_body = {
        'role': 'reader',
        'type': 'anyone'
    }
    service.permissions().create(
        fileId = file.get("id"),
        body=request_body
    ).execute()

    print(f'File ID: {file.get("id")}')
    print(f'File link: {file.get("resourceKey")}')
    url = "https://drive.google.com/file/d/" + file.get("id") + "/preview"
    print(url)
    return url

  except HttpError as error:
    print(f"An error occurred: {error}")