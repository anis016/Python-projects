import pickle
import os
import json


def get_file(page):
    course_title = page.split("/")[-1]
    for _file in os.listdir("."):
        if os.path.isfile(_file) and _file.startswith(course_title):
            return _file
    return None


def download(page):
    course_file = get_file(page)
    with open(course_file, 'rb') as handle:
        pkl_content = pickle.load(handle)
        contents = json.loads(pkl_content)
        for content in contents:
            print(content)


if __name__ == "__main__":
    page = "https://www.educative.io/courses/python-201-interactively-learn-advanced-concepts-in-python-3"
    download(page)
