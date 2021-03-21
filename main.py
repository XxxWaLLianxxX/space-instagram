import requests
import os


def download_images(image_url, image_number, filename, widening):
    os.makedirs("images/", exist_ok=True)
    file_path = "images/{image_number}{filename}.{widening}"
    response = requests.get(image_url, verify=False)
    response.raise_for_status()
    with open(file_path.format(image_number=image_number, filename=filename, widening=widening), "wb") as img:
        img.write(response.content)


def fetch_spacex_last_launch(filename):
    site_url = "https://api.spacexdata.com/v3/launches/45"
    response = requests.get(site_url)
    response.raise_for_status()
    flights_images = response.json()["links"]["flickr_images"]
    for image_number, image_url in enumerate(flights_images):
        download_images(image_url, image_number + 1, filename, get_widening(image_url))


def fetch_hubble_photos(filename):
    site_url = "http://hubblesite.org/api/v3/images/spacecraft"
    response = requests.get(site_url)
    response.raise_for_status()
    for image in response.json():
        image_id = image["id"]
        response = requests.get("http://hubblesite.org/api/v3/image/{id}".format(id=image_id))
        response.raise_for_status()
        space_image = response.json()["image_files"][-1]
        space_image_url = "https:{}".format(space_image["file_url"])
        download_images(space_image_url, image_id, filename, get_widening(space_image_url))


def get_widening(image_url):
    return image_url.split(".")[-1]


def main():
    requests.packages.urllib3.disable_warnings()

    fetch_spacex_last_launch("spacex")
    fetch_hubble_photos("hubble")


if __name__ == '__main__':
    main()
