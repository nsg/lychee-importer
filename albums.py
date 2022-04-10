import requests
import os
import json
import glob

LYCHEE_SERVER_URL=os.getenv("LYCHEE_SERVER_URL")
LYCHEE_API_KEY=os.getenv("LYCHEE_API_KEY")
LYCHEE_USER=os.getenv("LYCHEE_USER")
LYCHEE_PASSWORD=os.getenv("LYCHEE_PASSWORD")
LYCHEE_CONTAINER_NAME=os.getenv("LYCHEE_CONTAINER_NAME")
SOURCE_IMAGES=os.getenv("SOURCE_IMAGES")
OUTPUT_DIR=os.getenv("OUTPUT_DIR")

HEADERS = {
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Authorization": LYCHEE_API_KEY
}

def lychee_request(lychee_function, data={}, cookies={}):
    function_data = { "function": lychee_function }
    return requests.post(f"{LYCHEE_SERVER_URL}/api/{lychee_function}", headers=HEADERS, cookies=cookies, data={**function_data, **data})

def login():
    data = {
	    "username": LYCHEE_USER,
	    "password": LYCHEE_PASSWORD
    }
    r = lychee_request("Session::login", data)

    return r.cookies

def albums(cookies):
    r = lychee_request("Albums::get", {}, cookies)
    return json.loads(r.text)

def scan_images():
    folders = glob.glob(f"{SOURCE_IMAGES}/*")
    return [os.path.basename(folder) for folder in folders]

cookies = login()
resp = albums(cookies)

lychee_albums = {}
for album in resp["albums"]:
    lychee_albums[album['title']] = album['id']

f = open(f"{OUTPUT_DIR}/lychee-importer.sh", "w")
f.write("#!/bin/bash\n\n")
f.write(f"artisan() {{\n  /usr/bin/docker exec {LYCHEE_CONTAINER_NAME} php artisan \"$@\"\n}}\n\n")
f.write("mkdir -p /tmp/lychee-importer-process\n\n")
for album in scan_images():
    album_id = lychee_albums.get(album, None)
    f.write(f"# Album \"{album}\"\n")
    if album_id:
        f.write(f"artisan lychee:sync --album_id={album_id} --no-interaction -- \"{SOURCE_IMAGES}/{album}\"\n\n")
    else:
        f.write(f"ln -s \"{SOURCE_IMAGES}/{album}\" \"/tmp/lychee-importer-process/{album}\"\n")
        f.write(f"artisan lychee:sync --no-interaction -- /tmp/lychee-importer-process\n")
        f.write(f"rm \"/tmp/lychee-importer-process/{album}\"\n\n")

f.close()
os.chmod(f"{OUTPUT_DIR}/lychee-importer.sh", 0o755)
