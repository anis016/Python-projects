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
    print(results.strip())


if __name__ == "__main__":
    word = "example"

    dirname, _ = os.path.split(os.path.abspath(__file__))
    filename = os.path.join(dirname, "oxford_api_key.enc")
    headers = read_app_keys(filename=filename)
    url = create_url(word=word)
    results = get_definition(headers=headers, url=url)
    # results = '''
    # [{'id': 'example', 'language': 'en-gb', 'lexicalEntries': [{'entries': [{'etymologies': ['late Middle English: from Old French, from Latin exemplum, from eximere‘take out’, from ex-‘out’ + emere‘take’. Compare with sample'], 'senses': [{'definitions': ['a thing characteristic of its kind or illustrating a general rule'], 'examples': [{'text': 'advertising provides a good example of an industry where dreams have faded'}], 'id': 'm_en_gbus0339130.007', 'shortDefinitions': ['thing characteristic of its kind'], 'subsenses': [{'definitions': ['a written problem or exercise designed to illustrate a rule'], 'examples': [{'text': 'a workbook and a data set will enable the researcher to follow worked examples'}], 'id': 'm_en_gbus0339130.012', 'shortDefinitions': ['problem or exercise illustrating rule']}], 'synonyms': [{'id': 'specimen', 'language': 'en', 'text': 'specimen'}, {'id': 'sample', 'language': 'en', 'text': 'sample'}, {'language': 'en', 'text': 'exemplar'}, {'language': 'en', 'text': 'exemplification'}, {'id': 'instance', 'language': 'en', 'text': 'instance'}, {'id': 'case', 'language': 'en', 'text': 'case'}, {'language': 'en', 'text': 'representative case'}, {'language': 'en', 'text': 'typical case'}, {'id': 'case_in_point', 'language': 'en', 'text': 'case in point'}, {'id': 'illustration', 'language': 'en', 'text': 'illustration'}], 'thesaurusLinks': [{'entry_id': 'example', 'sense_id': 't_en_gb0005163.001'}]}, {'definitions': ['a person or thing regarded in terms of their fitness to be imitated'], 'examples': [{'text': 'it is important that parents should set an example'}, {'text': "he followed his brother's example and deserted his family"}], 'id': 'm_en_gbus0339130.014', 'shortDefinitions': ['person or thing imitated'], 'synonyms': [{'id': 'precedent', 'language': 'en', 'text': 'precedent'}, {'id': 'lead', 'language': 'en', 'text': 'lead'}, {'id': 'guide', 'language': 'en', 'text': 'guide'}, {'id': 'model', 'language': 'en', 'text': 'model'}, {'id': 'pattern', 'language': 'en', 'text': 'pattern'}, {'id': 'blueprint', 'language': 'en', 'text': 'blueprint'}, {'language': 'en', 'text': 'template'}, {'id': 'paradigm', 'language': 'en', 'text': 'paradigm'}, {'language': 'en', 'text': 'exemplar'}, {'id': 'ideal', 'language': 'en', 'text': 'ideal'}, {'id': 'standard', 'language': 'en', 'text': 'standard'}], 'thesaurusLinks': [{'entry_id': 'example', 'sense_id': 't_en_gb0005163.002'}]}]}], 'language': 'en-gb', 'lexicalCategory': {'id': 'noun', 'text': 'Noun'}, 'phrases': [{'id': 'for_example', 'text': 'for example'}, {'id': 'make_an_example_of', 'text': 'make an example of'}], 'pronunciations': [{'audioFile': 'http://audio.oxforddictionaries.com/en/mp3/example_gb_1.mp3', 'dialects': ['British English'], 'phoneticNotation': 'IPA', 'phoneticSpelling': 'ɪɡˈzɑːmp(ə)l'}, {'dialects': ['British English'], 'phoneticNotation': 'IPA', 'phoneticSpelling': 'ɛɡˈzɑːmp(ə)l'}], 'text': 'example'}, {'entries': [{'notes': [{'text': '"be exampled"', 'type': 'wordFormNote'}], 'senses': [{'definitions': ['be illustrated or exemplified'], 'examples': [{'text': 'the extent of Allied naval support is exampled by the navigational specialists provided'}], 'id': 'm_en_gbus0339130.016', 'shortDefinitions': ['be illustrated or exemplified']}]}], 'language': 'en-gb', 'lexicalCategory': {'id': 'verb', 'text': 'Verb'}, 'phrases': [{'id': 'for_example', 'text': 'for example'}, {'id': 'make_an_example_of', 'text': 'make an example of'}], 'pronunciations': [{'audioFile': 'http://audio.oxforddictionaries.com/en/mp3/example_gb_1.mp3', 'dialects': ['British English'], 'phoneticNotation': 'IPA', 'phoneticSpelling': 'ɪɡˈzɑːmp(ə)l'}, {'dialects': ['British English'], 'phoneticNotation': 'IPA', 'phoneticSpelling': 'ɛɡˈzɑːmp(ə)l'}], 'text': 'example'}], 'type': 'headword', 'word': 'example'}]
    # '''

    print_definition(results=results)
