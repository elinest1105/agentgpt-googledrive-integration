import requests
from bs4 import BeautifulSoup
import re
import os
import dropbox
from io import BytesIO
from urllib.parse import urljoin

def find_banner_ads(url, brand):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    img_tags = soup.find_all('img', alt=re.compile(brand, re.IGNORECASE))
    return [urljoin(url, img['src']) for img in img_tags]

def download_images(urls):
    images = []
    for url in urls:
        response = requests.get(url)
        image_data = BytesIO(response.content)
        images.append(image_data)
    return images

def upload_to_dropbox(images, access_token):
    dbx = dropbox.Dropbox(access_token)
    for idx, img in enumerate(images):
        file_name = f'/Skyrizi_banner_ad_{idx + 1}.jpg'
        dbx.files_upload(img.getvalue(), file_name)

def main():
    access_token = 'sl.Be2zuCcevNeB0xSJPb5QYEHGG_P9aa2CIbXBRnQ9Vpr57SmJGE2ip9xCBohWLTmY4gfw3VgsYnmAZEM3VYf6lPnMDda8Cs4ggg9j20QOOy7MPmm9nstYri-OzCFPBkZt13pVWho'
    skyrizi_url = 'https://www.skyrizi.com/'
    brand = 'Skyrizi'

    ad_urls = find_banner_ads(skyrizi_url, brand)
    images = download_images(ad_urls)
    upload_to_dropbox(images, access_token)

if __name__ == '__main__':
    main()