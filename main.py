import io
import requests
import os

from PIL import Image


def download_images(image_url, image_number, filename):
    os.makedirs("images/", exist_ok=True)
    file_path = "images/{image_number}{filename}.jpg"
    response = requests.get(image_url, verify=False)
    response.raise_for_status()
    encoded_image = response.content
    image_stream = io.BytesIO(encoded_image)
    decoded_image = Image.open(image_stream)
    decoded_image.thumbnail((1080, 1080))
    try:
        decoded_image.save(file_path.format(image_number=image_number, filename=filename))
    except:
        print("Картинка не сохранилась")


def fetch_spacex_last_launch():
    site_url = "https://api.spacexdata.com/v3/launches/45"
    response = requests.get(site_url)
    response.raise_for_status()
    flights_images = response.json()["links"]["flickr_images"]
    for image_number, image_url in enumerate(flights_images):
        download_images(image_url, image_number + 1, "spacex")


def fetch_hubble_photos():
    site_url = "http://hubblesite.org/api/v3/images/spacecraft"
    response = requests.get(site_url)
    response.raise_for_status()
    for image in response.json():
        image_id = image["id"]
        response = requests.get("http://hubblesite.org/api/v3/image/{id}".format(id=image_id))
        response.raise_for_status()
        space_image = response.json()["image_files"][-1]
        space_image_url = "https:{}".format(space_image["file_url"])
        download_images(space_image_url, image_id, "hubble")


def main():
    requests.packages.urllib3.disable_warnings()

    fetch_spacex_last_launch()
    fetch_hubble_photos()


if __name__ == '__main__':
    main()
