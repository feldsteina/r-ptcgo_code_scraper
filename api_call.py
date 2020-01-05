from google.cloud import vision
from google.protobuf.json_format import MessageToJson
import json
import requests
import re
import pyautogui as auto
import keyboard
from time import sleep
import api_keys


def ptcgo_auto_redeem(codes):
    if len(codes) <= 5:
        for item in codes:
            auto.moveTo(530, 890, duration=0.1)
            auto.click()
            sleep(0.2)
            keyboard.write(item)
            sleep(0.5)
            auto.moveTo(530, 980, duration=0.1)
            auto.click()
            sleep(0.2)
        auto.moveTo(1190, 980, duration=0.1)
        auto.click()
        sleep(0.5)
        auto.moveTo(820, 980, duration=0.1)
        auto.click()
        sleep(3)
    else:
        i = 0
        while i < len(codes):
            while ((i+1) % 6 != 0) & (i < len(codes)):
                auto.moveTo(530, 890, duration=0.1)
                auto.click()
                sleep(0.2)
                keyboard.write(codes[i])
                sleep(0.2)
                auto.moveTo(530, 980, duration=0.1)
                auto.click()
                sleep(0.2)
                i += 1
            auto.moveTo(1190, 980, duration=0.1)
            auto.click()
            sleep(0.5)
            auto.moveTo(820, 980, duration=0.1)
            auto.click()
            sleep(0.5)
            i += 1


def detect_text_uri(uri):
    """Detects text in the file located in Google Cloud Storage or on the Web.
    """

    client = vision.ImageAnnotatorClient()
    image = vision.types.Image()
    image.source.image_uri = uri

    response = client.text_detection(image=image)
    texts = response.text_annotations

    serialized = MessageToJson(response)

    parsed = json.loads(serialized)

    parsed = json.dumps(parsed, indent=4, sort_keys=True)

    r = re.compile("\\w{3}[-]{1}\\w{4}[-]{1}\\w{3}[-]{1}\\w{3}", re.MULTILINE)

    find_list = r.findall(parsed)

    code_list = []

    for item in find_list:
        if item not in code_list:
            code_list.append(item)

    for item in code_list:
        print(item)

    ptcgo_auto_redeem(code_list)


def reddit_feed(post_time):
    r = re.compile(
        "\\S*i\\.redd\\.it\\S*|\\S*i\\.imgur\\.com\\S*", re.MULTILINE)

    response = requests.get(
        "https://www.reddit.com/r/ptcgo/new.json?sort=new&limit=10",
        headers=api_keys.headers
    )

    json_data = json.loads(response.text)

    url_list = []

    post_data = json_data["data"]["children"]

    print("////////////////////////")

    for items in post_data:
        if items["data"]["created_utc"] > post_time:
            url_list.append(items["data"]["url"])
            print(f'{items["data"]["created_utc"]} > {post_time}')
        else:
            break

    print("========================")

    for items in url_list:
        print(items)

    print("========================")

    for items in post_data:
        if items["data"]["created_utc"] > post_time:
            print(items["data"]["created_utc"])
            post_time = items["data"]["created_utc"]
            print(post_time)
        else:
            break

    print("========================")

    image_urls = [x for x in url_list if r.findall(x)]

    for items in image_urls:
        print(items)
        detect_text_uri(items)

    print("========================")

    return post_time


def main():
    try:
        mrp = 10000
        while(True):
            auto.moveTo(720, 25, duration=0.1)
            auto.click()
            sleep(5)
            mrp = reddit_feed(mrp)
            auto.moveTo(630, 25, duration=0.1)
            auto.click()
            sleep(5)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
