import requests, json, sys
import pandas as pd
import os
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler

CLIENT_ID = '' # Needs to be filled in to work!
CLIENT_SECRET = '' # Needs to be filled in to work!

BASE_URL = 'https://api.twitch.tv/helix/'
INDENT = 2

COUNT = 0

# Takes a custom query from user and gets the response object
def get_response(query):
  url  = BASE_URL + query
  HEADERS = {'Client-ID': CLIENT_ID , 'Authorization': f"Bearer {get_access_token()}"}
  response = requests.get(url, headers=HEADERS)
  return response

# Get Access Token
def get_access_token():
    x = requests.post(f"https://id.twitch.tv/oauth2/token?client_id={CLIENT_ID}&client_secret={CLIENT_SECRET}&grant_type=client_credentials")
    return json.loads(x.text)["access_token"]

# Takes a response object and prints it on the console with proper format
def print_response(response):
  response_json = response.json()
  print_response = json.dumps(response_json, indent=INDENT)
  print(print_response)
  return response.json()

# Get Top 100 Streams
def getStreams():
  query = 'streams?first={0}'.format(100)
  response = get_response(query)
  return response

# Get User-Channel Data
def getUser(user_id):
  query = 'users?id={0}'.format(user_id)
  response = get_response(query)
  return response

# Get User Followers
def getFollowerCount(user_id):   
  query = 'users/follows?to_id={0}&first=1'.format(user_id)
  response = get_response(query)
  return response

# Get User Videos (20, all)
def getVideos(user_id):
  query = 'videos?user_id={0}'.format(user_id)
  response = get_response(query)
  return response

# Get User Clips (20, all)
def getClips(user_id):
  query = 'clips?broadcaster_id={0}'.format(user_id)
  response = get_response(query)
  return response
 
# Get all data, function needed for scheduling 
def getData():
  print("job executing...")
  global COUNT, scheduler

  streams = getStreams().json()
  streamsDF = pd.json_normalize(streams['data'])

  userIds = list(streamsDF['user_id'])
  for userid in userIds:
    if not os.path.exists('data/' + str(userid)):
      os.mkdir('data/' + str(userid))

      # Get followercount of each streamer
      follower = getFollowerCount(userid).json()
      data = {'user_id': userid, 'total':  follower['total']} 
      followerDF = pd.DataFrame(data, index=[0])   

      # Get videos of each streamer
      videos = getVideos(userid).json()
      videosDF = pd.json_normalize(videos['data'])    

      # Get clips of each streamer
      clips = getClips(userid).json()
      clipsDF = pd.json_normalize(clips['data'])

      # Save data for specific streamer
      followerDF.to_csv('data/' + str(userid) + '/' + 'follower' + '.csv')
      videosDF.to_csv('data/' + str(userid) + '/' + 'videos' + '.csv')
      clipsDF.to_csv('data/' + str(userid) + '/' + 'clips' + '.csv')

  now = datetime.now()
  file = 'Top100Streams_{0}'.format(now.strftime("%Y_%m_%d_%H_%M_%S"))
  streamsDF.to_csv('data/' + file + '.csv')

  COUNT = COUNT + 1
  if COUNT == 24:
      scheduler.remove_job('getData')


if __name__ == "__main__":
  scheduler = BlockingScheduler()
  scheduler.add_job(getData, 'interval', hours=2, id='getData')

  print("---------------------------------")
  print("Start")
  print("---------------------------------")

  scheduler.start()

  print("---------------------------------")
  print("End")
  print("---------------------------------")

