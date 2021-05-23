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


def download_image(image_url, image_number, filename, folder_path):
    response = requests.get(image_url, verify=False)
    response.raise_for_status()
    image_stream = io.BytesIO(response.content)
    decoded_image = Image.open(image_stream)
    file_path = "{folder_path}/{image_number}{filename}.jpg"
    decoded_image.save(file_path.format(folder_path=folder_path, image_number=image_number, filename=filename))


def correct_picture_resolution(folder_path):
    images = glob.glob("./{folder_path}/*.jpg".format(folder_path=folder_path))
    for image in images:
        image = Image.open(image)
        width, height = (1080, 1080)
        image.thumbnail((width, height))


def fetch_spacex_launch(launch_number):
    site_url = "https://api.spacexdata.com/v3/launches/{launch_number}".format(launch_number=launch_number)
    response = requests.get(site_url, verify=False)
    response.raise_for_status()
    flights_images = response.json()["links"]["flickr_images"]
    return flights_images


def fetch_hubble_collection(collection_name):
    site_url = "http://hubblesite.org/api/v3/images/{collection_name}".format(collection_name=collection_name)
    response = requests.get(site_url, verify=False)
    response.raise_for_status()
    space_image_urls = []
    for image in response.json():
        response = requests.get("http://hubblesite.org/api/v3/image/{id}".format(id=image["id"]), verify=False)
        response.raise_for_status()
        space_image = response.json()["image_files"][-1]
        space_image_urls.append("https:{}".format(space_image["file_url"]))
    return space_image_urls


def upload_photo_instagram(login, password, folder_path):
    shutil.rmtree("config", ignore_errors=True)
    images = glob.glob("./{folder_path}/*.jpg".format(folder_path=folder_path))
    images = sorted(images)
    bot = Bot()
    bot.login(username=login, password=password)
    for image in images:
        bot.upload_photo(image)
        if bot.api.last_response.status_code != 200:
            raise requests.HTTPError(bot.api.last_response)
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


def main(folder_path):
    load_dotenv()
    requests.packages.urllib3.disable_warnings()

    os.makedirs(folder_path, exist_ok=True)

    login, password = os.environ["INSTA_LOGIN"], os.environ["INSTA_PASSWORD"]

    args = get_cmd_args()
    launch_number = args.launch_number
    collection_name = args.collection_name

    flights_images = fetch_spacex_launch(launch_number)
    space_image_urls = fetch_hubble_collection(collection_name)
    for image_number, image_url in enumerate(flights_images, start=1):
        try:
            download_image(image_url, image_number, "spacex", "images")
        except OSError:
            print("Картинка не сохранилась")
    for image_number, space_image_url in enumerate(space_image_urls, start=1):
        try:
            download_image(space_image_url, image_number, "hubble", "images")
        except OSError:
            print("Картинка не сохранилась")
    try:
        correct_picture_resolution("images")
    except OSError:
        print("Не удалось обрезать")
    upload_photo_instagram(login, password, "images")


if __name__ == "__main__":
    main("images")
