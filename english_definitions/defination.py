# A program that returns english-word definitions

import requests
import json
import os

import secure


def read_app_keys(filename):
    password = secure.read_password()
    headers = secure.decrypt_file(password=password, filename=filename)
    return headers


def create_url(word):
    language = "en-gb"
    api = "https://od-api.oxforddictionaries.com:443/api/v2/entries"
    return "{0}/{1}/{2}".format(api, language, word.lower())


def get_definition(headers, url):
    results = ""
    try:
        r = requests.get(url=url, headers=headers)
        r.raise_for_status()
        if r.ok:
            results = r.json()['results'][0]
    except requests.exceptions.HTTPError as httperror:
        print(httperror)
    except requests.exceptions.RequestException as requesterror:
        print(requesterror)

    return results


def print_definition(results):
    for lexical_entry in results['lexicalEntries']:
        for entry in lexical_entry['entries']:
            for sense in entry['senses']:
                print('English definition: {0}'.format(sense['definitions'][0]))


if __name__ == "__main__":
    word = "Example"

    dirname, _ = os.path.split(os.path.abspath(__file__))
    filename = os.path.join(dirname, "oxford_api_key.enc")
    headers = read_app_keys(filename=filename)
    url = create_url(word=word)
    results = get_definition(headers=headers, url=url)

    print("Word: {0}\n".format(word))
    print_definition(results=results)
