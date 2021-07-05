import os

from urllib.request import Request, urlopen
from tempfile import NamedTemporaryFile

from django.core.files import File


def save_image(image_field, image_url):
    request = Request(image_url, headers={
        "User-Agent": "Mozilla/5.0",
        "X-Api-Key": os.environ["POKEMONTCG_IO_API_KEY"]
    })
    img_temp = NamedTemporaryFile(delete=True)
    img_temp.write(urlopen(request).read())
    img_temp.flush()
    image_field.save("image.jpg", File(img_temp))
