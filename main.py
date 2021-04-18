import argparse
import glob
import io
import os
import requests
import shutil
import time

from dotenv import load_dotenv
from instabot import Bot
from PIL import Image


def download_image(image_url, image_number, filename):
    os.makedirs("images/", exist_ok=True)
    file_path = "images/{image_number}{filename}.jpg"
    response = requests.get(image_url, verify=False)
    response.raise_for_status()
    encoded_image = response.content
    image_stream = io.BytesIO(encoded_image)
    decoded_image = Image.open(image_stream)
    width, height = (1080, 1080)
    decoded_image.thumbnail((width, height))
    try:
        decoded_image.save(file_path.format(image_number=image_number, filename=filename))
    except:
        print("Картинка не сохранилась")


def fetch_spacex_last_launch(launch_number):
    site_url = "https://api.spacexdata.com/v3/launches/{launch_number}".format(launch_number=launch_number)
    response = requests.get(site_url)
    response.raise_for_status()
    flights_images = response.json()["links"]["flickr_images"]
    for image_number, image_url in enumerate(flights_images):
        download_image(image_url, image_number + 1, "spacex")


def fetch_hubble_photo(collection_name):
    site_url = "http://hubblesite.org/api/v3/images/{collection_name}".format(collection_name=collection_name)
    response = requests.get(site_url)
    response.raise_for_status()
    for image in response.json():
        image_id = image["id"]
        response = requests.get("http://hubblesite.org/api/v3/image/{id}".format(id=image_id))
        response.raise_for_status()
        space_image = response.json()["image_files"][-1]
        space_image_url = "https:{}".format(space_image["file_url"])
        download_image(space_image_url, image_id, "hubble")


def upload_photo_instagram():
    shutil.rmtree("config", ignore_errors=True)
    folder_path = "./images"
    images = glob.glob(folder_path + "/*.jpg")
    images = sorted(images)
    bot = Bot()
    bot.login(username=os.environ["INSTA_LOGIN"], password=os.environ["INSTA_PASSWORD"])
    while True:
        for image in images:
            bot.upload_photo(image)
            if bot.api.last_response.status_code != 200:
                print(bot.api.last_response)
                break
        time.sleep(10)


def get_cmd_args():
    parser = argparse.ArgumentParser(description="Программа выкладывает фото в Instagram")
    parser.add_argument(
        "-ln",
        "--launch_number",
        help="Номер полета",
        default="2"
    )
    parser.add_argument(
        "-cn",
        "--collection_name",
        help="Название коллекции",
        default="spacecraft"
    )
    args = parser.parse_args()
    return args


args = get_cmd_args()
launch_number = args.launch_number
collection_name = args.collection_name


def main():
    load_dotenv()
    requests.packages.urllib3.disable_warnings()

    fetch_spacex_last_launch(launch_number)
    fetch_hubble_photo(collection_name)
    upload_photo_instagram()


if __name__ == '__main__':
    main()
