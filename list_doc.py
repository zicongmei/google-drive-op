import os.path
import logging

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/drive.metadata.readonly"]

TOKEN_PATH = ".tmp/token.json"
CLIENT_SECRET_FILE = "client_secret.json" 

def main():
  """Shows basic usage of the Drive v3 API.
  Prints the names and ids of the first 10 files the user has access to.
  """
  logger.info("Starting Google Drive API client.")
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists(TOKEN_PATH):
    logger.info(f"Found existing token file: {TOKEN_PATH}")
    creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
  else:
    logger.info(f"No existing token file found at {TOKEN_PATH}.")

  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      logger.info("Credentials expired, attempting to refresh token.")
      creds.refresh(Request())
      logger.info("Token refreshed successfully.")
    else:
      logger.info("No valid credentials or refresh token available. Initiating new authorization flow.")
      # Ensure the client secret file exists
      if not os.path.exists(CLIENT_SECRET_FILE):
          logger.error(f"Error: OAuth client secret file '{CLIENT_SECRET_FILE}' not found.")
          logger.error("Please run gcp_oauth.py to get instructions on generating it, or download your client_secret.json from GCP.")
          return

      logger.info(f"Using client secret file: {CLIENT_SECRET_FILE}")
      flow = InstalledAppFlow.from_client_secrets_file(
          CLIENT_SECRET_FILE, SCOPES # Use the new constant
      )
      logger.info("Starting local server for OAuth authorization.")
      creds = flow.run_local_server(port=0)
      logger.info("Authorization successful.")
    # Save the credentials for the next run
    logger.info(f"Saving credentials to {TOKEN_PATH}")
    os.makedirs(os.path.dirname(TOKEN_PATH), exist_ok=True)
    with open(TOKEN_PATH, "w") as token:
      token.write(creds.to_json())
    logger.info("Credentials saved.")

  try:
    logger.info("Building Google Drive API service.")
    service = build("drive", "v3", credentials=creds)
    logger.info("Drive API service built successfully.")

    # Call the Drive v3 API
    logger.info("Calling Drive v3 API to list files (pageSize=10).")
    results = (
        service.files()
        .list(pageSize=10, fields="nextPageToken, files(id, name)")
        .execute()
    )
    items = results.get("files", [])
    logger.info("API call executed.")

    if not items:
      logger.info("No files found.")
      print("No files found.")
      return
    logger.info(f"Found {len(items)} files. Printing names and IDs:")
    print("Files:")
    for item in items:
      print(f"{item['name']} ({item['id']})")
  except HttpError as error:
    logger.error(f"An HTTP error occurred: {error}", exc_info=True)
    # TODO(developer) - Handle errors from drive API.
    print(f"An error occurred: {error}")
  except Exception as error:
    logger.critical(f"An unexpected error occurred: {error}", exc_info=True)
    print(f"An unexpected error occurred: {error}")
  finally:
    logger.info("Google Drive API client finished.")


if __name__ == "__main__":
  main()
