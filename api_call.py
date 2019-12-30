import json
import requests
import re
import api_keys
import praw
import pyautogui as auto
import keyboard
from time import sleep


def ptcgo_auto_redeem(codes):
    if len(codes) <= 10:
        for item in codes:
            auto.moveTo(532, 892, duration=0.1)
            auto.click()
            sleep(0.2)
            item_keys = [char for char in item]
            keyboard.write(item)
            sleep(0.5)
            auto.moveTo(532, 982, duration=0.1)
            auto.click()
            sleep(0.2)
        # print(auto.position())
        return 0


def detect_text_uri(uri):
    """Detects text in the file located in Google Cloud Storage or on the Web.
    """
    from google.cloud import vision
    from google.protobuf.json_format import MessageToJson

    client = vision.ImageAnnotatorClient()
    image = vision.types.Image()
    image.source.image_uri = uri

    response = client.text_detection(image=image)
    texts = response.text_annotations

    serialized = MessageToJson(response)

    parsed = json.loads(serialized)
    # parsed = json.loads(serialized)

    parsed = json.dumps(parsed, indent=4, sort_keys=True)

    r = re.compile("\\w{3}[-]{1}\\w{4}[-]{1}\\w{3}[-]{1}\\w{3}", re.MULTILINE)

    find_list = r.findall(parsed)

    code_list = []
    for item in find_list:
        if item not in code_list:
            code_list.append(item)

    # for item in code_list:
    #     print(item)

    ptcgo_auto_redeem(code_list)


mrp = 10000


def reddit_feed():
    global mrp
    r = re.compile(
        "\\S*i\\.redd\\.it\\S*|\\S*i\\.imgur\\.com\\S*", re.MULTILINE)

    reddit = praw.Reddit(client_id=api_keys.client_id,
                         client_secret=api_keys.client_secret,
                         user_agent=api_keys.user_agent)

    new_posts = reddit.subreddit('ptcgo').new(limit=10)

    post_urls = []

    for items in new_posts:
        if (items.created_utc > mrp):
            print(f"{items.created_utc}  >  {mrp}")
            post_urls.append(items.url)
        else:
            break
    print("------------------------")

    i = 0

    for items in new_posts:
        if i < 1:
            print(items.created_utc)
            mrp = items.created_utc
            print(mrp)
        else:
            break
        i = i + 1

    print("========================")

    image_urls = [x for x in post_urls if r.findall(x)]

    # for items in image_urls:
    #     detect_text_uri(items)

    return mrp


def main():
    try:
        # mrp = "asdf"
        while(True):
            reddit_feed()
            sleep(5)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
