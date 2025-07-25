# Google Drive API Setup Guide

## Overview
This guide helps you set up Google Drive API integration to automatically extract information from your Google Drive documents.

## Step 1: Create Google Cloud Project

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Google Drive API:
   - Go to "APIs & Services" > "Library"
   - Search for "Google Drive API"
   - Click "Enable"

## Step 2: Create Credentials

1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "OAuth 2.0 Client IDs"
3. If prompted, configure the OAuth consent screen:
   - Choose "External" user type
   - Fill in the required fields (App name, User support email, Developer contact)
   - Add your email to test users
4. For Application type, choose "Desktop application"
5. Give it a name (e.g., "Investment Memo Generator")
6. Click "Create"

## Step 3: Download Credentials

1. After creating the OAuth client, click the download button
2. Save the downloaded file as `credentials.json` in your project directory
3. **Important**: Never commit this file to version control

## Step 4: File Sharing Requirements

For the app to access your Google Drive files, you need to:

1. **Make files shareable**: Right-click on files in Google Drive and select "Share"
2. **Set permissions**: Choose "Anyone with the link can view"
3. **Get the file ID**: Copy the shareable link and extract the file ID

### Example File ID Extraction:
- **Google Drive File**: `https://drive.google.com/file/d/1abc123xyz789/view`
- **File ID**: `1abc123xyz789`

- **Google Docs**: `https://docs.google.com/document/d/1abc123xyz789/edit`
- **File ID**: `1abc123xyz789`

## Step 5: First Time Authentication

1. When you first click "Connect to Google Drive" in the app
2. You'll see an authorization URL in the app
3. Visit that URL in your browser
4. Sign in with your Google account
5. Grant permissions to the app
6. Copy the authorization code and paste it back in the app

## Supported File Types

The app can process the following file types from Google Drive:
- **PDF files** (.pdf)
- **Word documents** (.docx)
- **Excel spreadsheets** (.xlsx, .xls)
- **Text files** (.txt)
- **Google Docs** (exported as text)
- **Google Sheets** (exported as Excel)

## Security Notes

- Your `credentials.json` file contains sensitive information
- The app only requests read-only access to your Google Drive
- Authentication tokens are stored locally in `token.pickle`
- You can revoke access anytime from your Google Account settings

## Troubleshooting

### Common Issues:

1. **"Credentials not found"**: Make sure `credentials.json` is in the project directory
2. **"Access denied"**: Check that files are shared properly
3. **"File not found"**: Verify the file ID is correct
4. **"Quota exceeded"**: Google Drive API has usage limits

### Getting Help:

If you encounter issues:
1. Check the Google Cloud Console for API quotas
2. Verify your OAuth consent screen is configured
3. Ensure files have proper sharing permissions
4. Check the Streamlit app logs for detailed error messages

## Optional: Service Account (Advanced)

For production use, consider using a service account instead of OAuth:

1. Create a service account in Google Cloud Console
2. Download the service account key as JSON
3. Share your Google Drive files with the service account email
4. Update the app code to use service account authentication

This method doesn't require interactive authentication but requires manual sharing of each file. 