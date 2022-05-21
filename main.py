import csv
from pytube import extract
import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

def video_id(url):
    id = extract.video_id(url)
    return id

if __name__ == "__main__":

    linki = []
    with open('links.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile,delimiter=' ', quotechar='|')
        for row in spamreader:
            linki.append(row)

    linki_new = []
    for i in range(len(linki)):
        linki_new.append(video_id(str(linki[i])))

    print(linki_new)

    #create playlist part here

    scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]


    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "YOUR_CLIENT_SECRET_FILE.json"

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    for item in linki_new:
        request = youtube.playlistItems().insert(
            part="snippet",
            body={
                "snippet": {
                "playlistId": "PLKYFB1OFvLxd6n7FD_DSU8XglqLXIA6wO",
                "position": 0,
                "resourceId": {
                    "kind": "youtube#video",
                    "videoId": item
                }
                }
            }
        )
        response = request.execute()

    print(response)