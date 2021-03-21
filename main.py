import requests
import os


def download_images(site_url):
    os.makedirs("images/", exist_ok=True)
    file_path = "images/{image_number}{filename}"
    response = requests.get(site_url)
    response.raise_for_status()
    images_info = response.json()
    return images_info, file_path


def fetch_spacex_last_launch(images_url, filename):
    images_info, file_path = download_images(site_url="https://api.spacexdata.com/v4/launches/latest")
    flights_images = images_info['links']['flickr']['original']
    for image_number, image in enumerate(flights_images):
        response = requests.get(image)
        response.raise_for_status()
        with open(file_path.format(image_number=image_number + 1, filename=filename), "wb") as img:
            img.write(response.content)
    return flights_images


def get_widening(image_url):
    return image_url.split(".")[-1]


def main():
    requests.packages.urllib3.disable_warnings()

    fetch_spacex_last_launch(images_url=fetch_spacex_last_launch, filename="spacex")
    fetch_hubble_photos("hubble")


if __name__ == '__main__':
    main()
