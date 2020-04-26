import requests
import os
from zipfile import ZipFile
import subprocess
import re
import xml.etree.ElementTree as ElementTree
import random
from bs4 import BeautifulSoup
import pickle
from itertools import cycle

USER_AGENT_LIST = [
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'
]


def get_user_agent(page):
    user_agent_pool = cycle(USER_AGENT_LIST)
    user_agent = ""
    headers = dict()
    found = False
    for count, _ in enumerate(USER_AGENT_LIST):
        user_agent = next(user_agent_pool)
        headers = {'user-agent': user_agent}
        print("Request #{0} for user-agent {1}".format(count, user_agent))
        try:
            response = requests.get(page, headers=headers, timeout=10.0)
            response.raise_for_status()
            if response.status_code == 200:
                print("got an user-agent.. breaking")
                found = True
                break
        except requests.exceptions.HTTPError:
            print("Skipping. Connection error")
        print()

    if found:
        return user_agent, headers
    else:
        SystemExit("no user-agent found.. exiting.")


# TODO: this is called twice, this needs to be handled
user_agent, headers = get_user_agent("https://www.educative.io")


def get_proxies():
    print("proxies not found... retrieving list of proxies")
    proxy_url = 'https://free-proxy-list.net/'  # doesn't work, better to not use it
    r = requests.get(proxy_url, headers=headers)
    r.raise_for_status()
    proxies = set()
    if r.status_code == 200:
        try:
            soup = BeautifulSoup(r.text, 'html5lib')
            soup_tr = soup.find('table').find('tbody').find_all('tr')
            for tr in soup_tr:
                ip = tr.find_all('td')[0].text
                port = tr.find_all('td')[1].text
                proxy = ":".join([ip, port])
                proxies.add(proxy)
        except requests.exceptions.HTTPError as err:
            print("exception in requests " + str(err))
            raise SystemExit(err)

    # writing pickle in a file
    # with open('proxies.pkl', 'wb') as handle:
    #    pickle.dump(proxies, handle, protocol=pickle.HIGHEST_PROTOCOL)
    # writing pickle from a file
    # with open('proxies.pkl', 'rb') as handle:
    #    proxies = pickle.load(handle)

    return proxies


def create_driver_folder():
    dirname, _ = os.path.split(os.path.abspath(__file__))
    driver_path = os.path.join(dirname, "drivers")
    if not os.path.exists(driver_path):
        os.mkdir(driver_path)
    return driver_path


def get_system_chrome_version():
    # check if google-chrome is installed in the system or else throw error
    p = subprocess.Popen(['google-chrome', '--version'], stdout=subprocess.PIPE)
    _stdout, _ = p.communicate()
    stdout = _stdout.decode('utf-8')
    if stdout.endswith("\n"):
        stdout = stdout.replace("\n", "")
    print("installed chrome version: " + stdout)

    re_compile = re.compile(r"([\d.]+)")
    version_number = re_compile.findall(stdout)[0]  # 80.0.3987.132
    return version_number


def parse_chrome_driver_version():
    driver_url = "http://chromedriver.storage.googleapis.com/"
    version_number = get_system_chrome_version()
    major_version = ".".join(version_number.split(".")[0:2])  # 80.0
    try:
        r = requests.get(url=driver_url, headers=headers)
        r.raise_for_status()
        r_xmls = r.content.decode("utf-8")
        root = ElementTree.fromstring(r_xmls)
        found = False
        driver_version = ""
        for elem in root.iter():
            if "Key" in elem.tag:
                if major_version in elem.text:
                    found = True
                    driver_version = elem.text
                    break
        if found:
            return os.path.join(driver_url, driver_version)
        else:
            raise KeyError("driver version not found")

    except requests.exceptions.HTTPError as err:
        print("exception in requests " + str(err))
        raise SystemExit(err)


def download_chrome_driver(driver_path):
    file_path_driver = os.path.join(driver_path, "chromedriver")

    # if exists then return the driver path
    if os.path.exists(file_path_driver):
        return file_path_driver

    # or continue making one
    print("chromedriver not found")
    file_path_zipped = os.path.join(driver_path, "chromedriver_linux64.zip")
    chrome_driver_url = parse_chrome_driver_version()
    print(chrome_driver_url)  # 'https://chromedriver.storage.googleapis.com/80.0.3987.106/chromedriver_linux64.zip'

    if not os.path.exists(file_path_driver):
        if not os.path.exists(file_path_zipped):
            try:
                r = requests.get(url=chrome_driver_url, allow_redirects=True, headers=headers, stream=True)
                r.raise_for_status()
                if r.status_code == 200:
                    print("connected")
                    print("downloading " + os.path.basename(file_path_zipped))
                    try:
                        with open(file_path_zipped, "wb") as fw:
                            for chunk in r.iter_content(chunk_size=256):
                                if chunk:
                                    fw.write(chunk)
                    except Exception as exception:
                        print("error downloading ", exception)
                    else:
                        print("downloaded " + os.path.basename(file_path_zipped))
            except requests.exceptions.HTTPError as err:
                print("exception in requests " + str(err))
                raise SystemExit(err)

        if os.path.exists(file_path_zipped):
            print("unzipping " + os.path.basename(file_path_zipped))
            zf = ZipFile(file_path_zipped, 'r')
            try:
                zf.extractall(path=os.path.dirname(file_path_driver))
                os.chmod(path=file_path_driver, mode=0o755)
            finally:
                zf.close()
            print("unzipped " + os.path.basename(file_path_zipped))

            if os.path.exists(file_path_driver):
                os.remove(path=file_path_zipped)
    return file_path_driver


def get_chrome_driver():
    driver_path = create_driver_folder()
    chrome_driver = download_chrome_driver(driver_path)
    if os.path.exists(chrome_driver):
        print("chromedriver path: " + chrome_driver)
        return chrome_driver
    else:
        raise FileNotFoundError("file not found")


if __name__ == "__main__":
    proxies = get_proxies()
    print(proxies)
    print("user-agent: " + user_agent + "headers: " + str(headers))
    # chrome_driver_path = get_chrome_driver()
    # print(chrome_driver_path)
