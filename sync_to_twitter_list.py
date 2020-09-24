from tweepy import OAuthHandler, API, Cursor
import credentials
import json

APPG_LIST_ID = 1307681477178650627  # https://twitter.com/i/lists/1307681477178650627

auth = OAuthHandler(credentials.CONSUMER_KEY, credentials.CONSUMER_SECRET)
auth.set_access_token(credentials.ACCESS_TOKEN, credentials.ACCESS_TOKEN_SECRET)

twitter = API(auth)

appgs = json.load(open("./appg-social-media.json"))

for appg in appgs:
    if len(appg['twitter']) == 0:
        continue

    print("Adding Twitter for %s : %s" % (appg['name'], appg['twitter']))
    twitter.add_list_members(screen_name=[appg['twitter']], list_id=APPG_LIST_ID)

appg_names = [appg['twitter'].lower() for appg in appgs]

for appg in Cursor(twitter.list_members, list_id=APPG_LIST_ID).items():
    if appg.screen_name.lower() not in appg_names:
        print("%s in Twitter list but not JSON, removing" % appg.screen_name.lower())
        twitter.remove_list_members(screen_name=appg.screen_name, list_id=APPG_LIST_ID)

