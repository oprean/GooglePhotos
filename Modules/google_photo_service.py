from __future__ import print_function

from os.path import exists
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

#ALBUMS_JSON = "c:\Personal/projects/PythonDigitalFrame/GooglePhotos/Data/albums.json"
ALBUMS_JSON = "c:\Personal/projects/PythonDigitalFrame/GooglePhotos/Data/albums_short.json"

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/photoslibrary.readonly']


class GooglePhotos():
    def __init__(self):
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if exists('token.json'):
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
        self.categories = ['ANIMALS','FASHION','LANDMARKS','RECEIPTS','WEDDINGS',
                            'ARTS','FLOWERS','LANDSCAPES','SCREENSHOTS','WHITEBOARDS',
                            'BIRTHDAYS','FOOD','NIGHT','SELFIES',
                            'CITYSCAPES','GARDENS','PEOPLE','SPORT'
                            'CRAFTS','HOLIDAYS','PERFORMANCES','TRAVEL',
                            'DOCUMENTS','HOUSES','PETS','UTILITY']

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
            "albumId": albumId,
            "pageSize": 50
        }
        results = self.service.mediaItems().search(body=body).execute()

        self.mediaItems = results.get('mediaItems', [])
        return self.mediaItems
    
    # https://developers.google.com/photos/library/guides/apply-filters
    def getFilteredItems(self,filter):
        body = {
            "filters": {
                "contentFilter": {
                    "includedContentCategories": [
                    "HOLIDAYS"
                    ]
                },
                "mediaTypeFilter": {
                  "mediaTypes": [
                    "PHOTO"
                    ]
                }
            },
            "pageSize": 50
        }
        results = self.service.mediaItems().search(body=body).execute()

        self.mediaItems = results.get('mediaItems', [])
        return self.mediaItems


    def getItem(self, itemId):
        return 1