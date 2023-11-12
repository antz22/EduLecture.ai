import os.path

import urllib.request
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from PIL import Image

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/presentations.readonly"]

def authentication():
  """Shows basic usage of the Slides API.
  Prints the number of slides and elements in a sample presentation.
  """
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("cloud/token.json"):
    creds = Credentials.from_authorized_user_file("cloud/token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "cloud/credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=50720)
    # Save the credentials for the next run
    with open("cloud/token.json", "w") as token:
      token.write(creds.to_json())
    
  service = build("slides", "v1", credentials=creds)
  return service

def generate_text(presentation_id, image_folder_path):
  service = authentication()
  # Create text file to store speaker notes
  text_file_path = image_folder_path + "/speaker_notes.txt"
  text_file = open(text_file_path, "w")

  # Call the Slides API
  presentation = (
      service.presentations().get(presentationId=presentation_id).execute()
  )
  slides = presentation.get("slides")

  for i, slide in enumerate(slides):
    # Generate Text file
    page_id = slide.get("objectId")
    page = service.presentations().pages().get(presentationId=presentation_id, pageObjectId=page_id).execute()
    note_id = page["slideProperties"]["notesPage"]["notesProperties"]["speakerNotesObjectId"]
    page_ele = page["slideProperties"]["notesPage"]["pageElements"]
    for j, obj in enumerate(page_ele):  
      if (note_id == page_ele[j]["objectId"]):
        if ("text" in page_ele[j]["shape"]):
          note = page_ele[j]["shape"]["text"]["textElements"][1]["textRun"]["content"]
          text_file.write(note)
          text_file.write("***** \n")
        else:
          text_file.write("***** \n")

  return text_file_path

def generate_images(presentation_id, image_folder_path):
  service = authentication()

  # Call the Slides API
  presentation = (
    service.presentations().get(presentationId=presentation_id).execute()
  )
  slides = presentation.get("slides")
  
  # constructing temp-lectures directory
  os.mkdir(image_folder_path)

  for i, slide in enumerate(slides):
    page_id = slide.get("objectId")
    page_thumbnail = service.presentations().pages().getThumbnail(presentationId=presentation_id, pageObjectId=page_id).execute()
    image_url = page_thumbnail["contentUrl"]
    filename = image_folder_path + "/slide" + str(i + 1) + ".png"
    urllib.request.urlretrieve(image_url, filename)

  return image_folder_path
