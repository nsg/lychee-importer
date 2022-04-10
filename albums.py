import requests
import os
import json

LYCHEE_SERVER_URL=os.getenv("LYCHEE_SERVER_URL")
LYCHEE_API_KEY=os.getenv("LYCHEE_API_KEY")
LYCHEE_USER=os.getenv("LYCHEE_USER")
LYCHEE_PASSWORD=os.getenv("LYCHEE_PASSWORD")

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

cookies = login()
resp = albums(cookies)

for album in resp["albums"]:
    print(album['id'])
    print(album['title'])
