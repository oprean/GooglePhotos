from __future__ import print_function

from os.path import exists
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

ALBUMS_JSON = "c:\Personal/projects/PythonDigitalFrame/GooglePhotos/Data/albums.json"

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/photoslibrary.readonly']


class GooglePhotos():
    def __init__(self):
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'client_secret.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
        self.service = build('photoslibrary', 'v1', credentials=creds, static_discovery=False)
        if exists(ALBUMS_JSON):
            f = open(ALBUMS_JSON)
            self.albums = json.load(f)
        else:
            self.updateAlbums()

    def updateAlbums(self):
        token = None
        while True:
            results = self.service.albums().list(
                pageSize=50,
                pageToken=token,
                #fields="nextPageToken,albums(id,title)"
            ).execute()
            self.albums.extend(results.get('albums', []))
            token = results.get('nextPageToken')
            if not token:
                break
        json_string =  json.dumps(self.albums,indent=4)
        with open(ALBUMS_JSON, 'w') as f:
            f.write(json_string)

    def getAlbumItems(self,albumId):
        body = {
            "albumId": 'AOFW6EPvOoyegvp2XA7PXR7H_VrZZoi17hfmUURCrvyEEDK7RIPS31MOQa6TsR8W8VmGmVQXBSGo',
            "pageSize": 10
        }
        results = self.service.mediaItems().search(body=body).execute()

        self.mediaItems = results.get('mediaItems', [])
        return self.mediaItems
    
    def getItem(self, itemId):
        return 1

def main():
    """Shows basic usage of the People API.
    Prints the name of the first 10 connections.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('photoslibrary', 'v1', credentials=creds, static_discovery=False)    
        """albums = []
        token = None
        while True:
            results = service.albums().list(
                pageSize=50,
                pageToken=token,
                #fields="nextPageToken,albums(id,title)"
            ).execute()
            albums.extend(results.get('albums', []))
            token = results.get('nextPageToken')
            if not token:
                break

        for album in albums:
            title = album.get('title', [])
            id = album.get('id', [])
            #print(id, title)
        json_string =  json.dumps(albums,indent=4)
        with open(ALBUMS_JSON, 'w') as f:
            f.write(json_string)

        return    """
        body = {
            "albumId": 'AOFW6EPvOoyegvp2XA7PXR7H_VrZZoi17hfmUURCrvyEEDK7RIPS31MOQa6TsR8W8VmGmVQXBSGo',
            "pageSize": 10
            }
        results = service.mediaItems().search(body=body).execute()

        mediaItems = results.get('mediaItems', [])
        # https://developers.google.com/photos/library/guides/access-media-items
        for photo in mediaItems:
            url = photo.get('baseUrl', [])
            print(url)


        # https://developers.google.com/photos/library/guides/apply-filters
    except HttpError as err:
        print(err)

# https://dev.to/davidedelpapa/manage-your-google-photo-account-with-python-p-2-3kaa
if __name__ == '__main__':
    main()