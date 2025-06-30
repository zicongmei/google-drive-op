# google-drive-op

This repository contains a Python script (`list_doc.py`) that interacts with the Google Drive API to list documents.

## Setup and Usage

To run `list_doc.py`, you need to set up Google Cloud Platform credentials and download a `client_secret.json` file.

### 1. Enable the Google Drive API

1.  Go to the [Google Cloud Console](https://console.cloud.google.com/).
2.  Select or create a new project.
3.  In the navigation menu, go to **APIs & Services > Library**.
4.  Search for "Google Drive API" and select it.
5.  Click the "Enable" button.

### 2. Configure the OAuth Consent Screen

If this is your first time setting up OAuth credentials for this project:

1.  In the Google Cloud Console, navigate to **APIs & Services > OAuth consent screen**.
2.  Choose the "User type" (e.g., "External" if you are not part of a Google Workspace organization and want to use it with any Google account).
3.  Click "CREATE".
4.  Fill in the required fields:
    *   **App name**: e.g., `Drive API Quickstart`
    *   **User support email**: Your email address.
    *   **Developer contact information**: Your email address.
5.  Click "SAVE AND CONTINUE".
6.  **Scopes**: For this example, you don't need to add any specific scopes here as they will be requested by the application during authorization. Click "SAVE AND CONTINUE".
7.  **Test users**: If you chose "External" and your app is not yet verified, you'll need to add your Google account as a test user. Click "ADD USERS", enter your Google account email, and click "ADD".
8.  Click "SAVE AND CONTINUE".
9.  Review the summary and click "BACK TO DASHBOARD".

### 3. Create Desktop OAuth Client ID

1.  In the Google Cloud Console, navigate to **APIs & Services > Credentials**.
2.  Click "CREATE CREDENTIALS" and select "OAuth client ID".
3.  For "Application type", choose **Desktop app**.
4.  Enter a name for your client ID (e.g., `Drive Quickstart Desktop Client`).
5.  Click "CREATE".
6.  A dialog box will appear with your client ID and client secret. Click "DOWNLOAD JSON". This will download a file typically named `client_secret_YOUR_CLIENT_ID.json`.

### 4. Rename and Place the Client Secret File

1.  Locate the downloaded `client_secret_YOUR_CLIENT_ID.json` file.
2.  Rename this file to `client_secret.json`.
3.  Place the `client_secret.json` file in the same directory as the `list_doc.py` script.

    *Example directory structure:*
    ```
    google-drive-op/
    ├── list_doc.py
    └── client_secret.json
    ```

### 5. Install Dependencies

Ensure you have Python installed. Then install the required libraries:

```bash
pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

### 6. Run the Script

Now you can run the script:

```bash
python list_doc.py
```

The first time you run it, a browser window will open asking you to authorize the application. Follow the prompts to grant access. After successful authorization, a file named `.tmp/token.json` will be created in your project directory to store your credentials for future runs.