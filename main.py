from flask import Flask, render_template, request, jsonify, json
import requests
from datetime import datetime

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def homepage():
    return render_template("index.html", title="Twitch Streamer VODs")


@app.route("/LoadVodList", methods=['GET', 'POST'])
def LoadVodList():

    #########################
    ## GETTING VIDEOS LIST ##
    #########################

    ## Its the name you see when you browse to the twitch url of the streamer
    USER_ID = request.args.get('input')

    CLIENT_ID = "ieshhz3qdq2c8iwnibrw9988d3trey" 
    SECRET = "drvli9opyl07t7i8o5drocdk8okhd2"

    ## First get a local access token. 
    secretKeyURL = "https://id.twitch.tv/oauth2/token?client_id={}&client_secret={}&grant_type=client_credentials".format(CLIENT_ID, SECRET)
    responseA = requests.post(secretKeyURL)
    accessTokenData = responseA.json()

    ## Then figure out the user id. 
    userIDURL = "https://api.twitch.tv/helix/users?login=%s"%USER_ID
    responseB = requests.get(userIDURL, headers={"Client-ID":CLIENT_ID,
                                                    'Authorization': "Bearer "+accessTokenData["access_token"]})
    userID = responseB.json()["data"][0]["id"]


    ## Now you can request the video data.
    findVideoURL = "https://api.twitch.tv/helix/videos?user_id=%s"%userID
    responseC= requests.get(findVideoURL, headers={"Client-ID":CLIENT_ID,
                                                    'Authorization': "Bearer "+accessTokenData["access_token"]})
    print(responseC.json())
    data_array = []
    data_array.append('VIDEOS')
    for video in responseC.json()["data"]:
        item = {}
        item['Title'] = video['title']
        item['Date'] = video['created_at'].split("T")[0]
        item['Duration'] = video['duration']
        item['Thumbnail_url'] = video['thumbnail_url'].replace('%','').format(width = "192", height = "108")
        item['vod_id'] = video['id']

        if len(data_array) < 11:
            data_array.append(item)
    
    #####################################
    ## VIDEOS RETRIEVED, GETTING CLIPS ##
    #####################################

    findVideoURL2 = "https://api.twitch.tv/helix/clips?broadcaster_id=%s"%userID
    responseD= requests.get(findVideoURL2, headers={"Client-ID":CLIENT_ID,
                                                    'Authorization': "Bearer "+accessTokenData["access_token"]})

    sorted_clips = sorted(responseD.json()['data'], key=lambda x: datetime.strptime(x['created_at'], '%Y-%m-%dT%H:%M:%SZ'), reverse=True)
    print(sorted_clips)

    data_array.append('CLIPS')
    for video in sorted_clips:
        item = {}
        item['Title'] = video['title']
        item['Date'] = video['created_at'].split("T")[0]
        item['Duration'] = str(video['duration']) + 's'
        item['Thumbnail_url'] = video['thumbnail_url'].replace('%','').format(width = "192", height = "108")
        item['clip_id'] = video['id']

        if len(data_array) < 22:
            data_array.append(item)
    
    return_json = json.dumps(data_array)
    return (jsonify({'response':return_json}))

def sortFunction(value):
    return value['created_at']

if __name__ == "__main__":
    app.run(debug=True)