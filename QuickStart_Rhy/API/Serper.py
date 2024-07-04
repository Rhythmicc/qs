from . import pre_check

serper_api_key = pre_check('serper')


def __do_request(query, action):
    import json
    import requests

    url = f"https://google.serper.dev/{action}"
    payload = json.dumps({
        "q": query
    })
    headers = {
        'X-API-KEY': serper_api_key,
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json()


def search(query):
    return __do_request(query, "search")

def images(query):
    return __do_request(query, "images")

def videos(query):
    return __do_request(query, "videos")

def places(query):
    return __do_request(query, "places")

def maps(query):
    return __do_request(query, "maps")

def news(query):
    return __do_request(query, "news")

def shopping(query):
    return __do_request(query, "shopping")

def scholar(query):
    return __do_request(query, "scholar")

def patents(query):
    return __do_request(query, "patents")

def autocomplete(query):
    return __do_request(query, "autocomplete")
