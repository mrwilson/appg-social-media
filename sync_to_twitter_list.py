from tweepy import OAuthHandler, API
import credentials
import json

APPG_LIST_ID = 1307681477178650627  # https://twitter.com/i/lists/1307681477178650627

auth = OAuthHandler(credentials.CONSUMER_KEY, credentials.CONSUMER_SECRET)
auth.set_access_token(credentials.ACCESS_TOKEN, credentials.ACCESS_TOKEN_SECRET)

twitter = API(auth)

for appg in json.load(open("./appg-social-media.json")):
    if len(appg['twitter']) == 0:
        continue

    print("Adding Twitter for %s : %s" % (appg['name'], appg['twitter']))
    twitter.add_list_members(screen_name=[appg['twitter']], list_id=APPG_LIST_ID)
