from tweepy import OAuthHandler, API, Cursor
import credentials
import json

APPG_LIST_ID = 1307681477178650627  # https://twitter.com/i/lists/1307681477178650627

auth = OAuthHandler(credentials.CONSUMER_KEY, credentials.CONSUMER_SECRET)
auth.set_access_token(credentials.ACCESS_TOKEN, credentials.ACCESS_TOKEN_SECRET)

twitter = API(auth)


def appgs_in_twitter_list():
    appgs = []
    for appg in Cursor(twitter.list_members, list_id=APPG_LIST_ID).items():
        appgs.append(appg.screen_name.lower())
    return appgs


def appgs_in_json():
    return json.load(open("./appg-social-media.json"))


twitter_list = appgs_in_twitter_list()
json_list = appgs_in_json()

for appg in [appg for appg in json_list if appg["twitter"].lower() not in twitter_list]:
    if appg["twitter"].lower() not in twitter_list or len(appg["twitter"]) == 0:
        continue

    print("Adding Twitter for %s : %s" % (appg["name"], appg["twitter"]))
    twitter.add_list_members(screen_name=[appg["twitter"]], list_id=APPG_LIST_ID)

json_handles = [appg["twitter"].lower() for appg in json_list]

for appg in twitter_list:
    if appg in json_handles:
        continue
    print("%s in Twitter list but not JSON, removing" % appg)
    twitter.remove_list_members(screen_name=[appg], list_id=APPG_LIST_ID)
