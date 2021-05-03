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

FOLDER_PATH = "images"


def download_image(image, image_number, filename):
    file_path = "{folder_path}/{image_number}{filename}.jpg"
    image.save(file_path.format(folder_path=FOLDER_PATH, image_number=image_number, filename=filename))


def correct_picture_resolution(image_url):
    response = requests.get(image_url, verify=False)
    response.raise_for_status()
    encoded_image = response.content
    image_stream = io.BytesIO(encoded_image)
    decoded_image = Image.open(image_stream)
    width, height = (1080, 1080)
    decoded_image.thumbnail((width, height))
    return decoded_image


def fetch_spacex_last_launch(launch_number):
    site_url = "https://api.spacexdata.com/v3/launches/{launch_number}".format(launch_number=launch_number)
    response = requests.get(site_url)
    response.raise_for_status()
    flights_images = response.json()["links"]["flickr_images"]
    for image_number, image_url in enumerate(flights_images):
        try:
            download_image(correct_picture_resolution(image_url), image_number + 1, "spacex")
        except OSError:
            print("Картинка не сохранилась")


def fetch_hubble_collection(collection_name):
    site_url = "http://hubblesite.org/api/v3/images/{collection_name}".format(collection_name=collection_name)
    response = requests.get(site_url)
    response.raise_for_status()
    for image in response.json():
        image_id = image["id"]
        response = requests.get("http://hubblesite.org/api/v3/image/{id}".format(id=image_id))
        response.raise_for_status()
        space_image = response.json()["image_files"][-1]
        space_image_url = "https:{}".format(space_image["file_url"])
        try:
            download_image(correct_picture_resolution(space_image_url), image_id, "hubble")
        except OSError:
            print("Картинка не сохранилась")


def upload_photo_instagram(login, password):
    shutil.rmtree("config", ignore_errors=True)
    images = glob.glob("./{folder_path}/*.jpg".format(folder_path=FOLDER_PATH))
    images = sorted(images)
    bot = Bot()
    bot.login(username=login, password=password)
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


def main():
    load_dotenv()
    requests.packages.urllib3.disable_warnings()

    os.makedirs(FOLDER_PATH, exist_ok=True)

    login, password = os.environ["INSTA_LOGIN"], os.environ["INSTA_PASSWORD"]

    args = get_cmd_args()
    launch_number = args.launch_number
    collection_name = args.collection_name

    fetch_spacex_last_launch(launch_number)
    fetch_hubble_collection(collection_name)
    upload_photo_instagram(login, password)


if __name__ == "__main__":
    main()
