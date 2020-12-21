"""
@author sendQueue <Vinii>
Further info at Vinii.de or github@vinii.de, file created at
19.11.2020 and last edited 20.12.2020. Use is only authorized if given credit!
"""

import argparse
import threading
import time

import requests

parser = argparse.ArgumentParser(description="This script is ONLY for the .me version of Strawpoll")
parser.add_argument("id", help="Strawpoll ID -> .me/xxxx (xxxx is the id)")
parser.add_argument("option", help="Checkbox number -> 1. answer or 2. answer.. so on.")
parser.add_argument("-d", help="Delay in ms -> Default: 0.2 seconds till new thread.")
parser.add_argument("-mt", help="Max amount of threads -> Default: 16")
parser.add_argument("-to", help="Proxy timeout -> Default: 10 seconds")

full_args = parser.parse_args()

count = 0
working_proxies = []

OKGREEN = '\033[92m'
WARNING = '\033[93m'
ENDC = '\033[0m'

motd = """"
 ____  ____  __ _  ____   __   _  _  ____  _  _  ____ 
/ ___)(  __)(  ( \(    \ /  \ / )( \(  __)/ )( \(  __)
\___ \ ) _) /    / ) D ((  O )) \/ ( ) _) ) \/ ( ) _) 
(____/(____)\_)__)(____/ \__\)\____/(____)\____/(____)
                                    
        \033[93mstrawpoll.me \033[0mip bypassing voting bot
                                  - by Vinii | sendQueue    
                                                  
"""


def init(args):
    print(motd)

    header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko)'
                            'Chrome/87.0.4280.88 Safari/537.36'}
    url = "https://www.strawpoll.me/" + args.id

    # initialize args
    if args.d is None:
        d = 0.05
    else:
        d = int(args.d) / 1000

    if args.mt is None:
        mt = 16
    else:
        mt = int(args.mt)

    if args.to is None:
        to = 10
    else:
        to = int(args.to)

    option = int(args.option)

    # read proxies file and parse proxy
    try:
        proxies = open("proxies.txt", "r").read().split("\n")
        print(OKGREEN + "Total proxies: ", len(proxies), ENDC)

        p_count = 0
        global count
        count = 0
        while True:
            proxy = proxies[p_count]
            p_count += 1
            if p_count >= len(proxies):
                print(WARNING + "Used all proxies. Finishing remaining threads" + ENDC)
                break

            thread = threading.Thread(target=do_poll, args=(url, header, option, proxy, to))
            thread.daemon = True
            thread.start()

            # keep thread limiter
            while threading.active_count() >= mt:
                time.sleep(0.05)

            # delay before adding thread
            time.sleep(d)

        # wait till all threads are done
        while threading.active_count() > 1:
            pass
        else:
            print(OKGREEN + "Finished botting with" + WARNING, count, OKGREEN + "successful votes!" + ENDC)

    except FileNotFoundError:
        print("proxies.txt not found! If running on windows: Change to valid windows path")


def do_poll(url, header, op, proxy, to):
    proxies = {"https": "https://" + proxy}
    if len(proxy) < 4:
        return
    try:
        req = requests.get(url, headers=header, proxies=proxies, timeout=to)
        # find oids --> "checkbox id"
        oids = str(find_checkbox(req.text, op))

        # find tokens
        sec_token = str(find_sec_token(req.text))
        field_token = str(find_field_token(req.text))

        page = requests.post(url, cookies=req.cookies, data={"security-token": sec_token + "&" + field_token, "options": oids},
                             headers=header, proxies=proxies, timeout=to)

        if page.text.find("\"success\":\"success\"") != -1:
            global count
            count += 1
            working_proxies.append(proxy)
            print(OKGREEN + "1 Vote added!" + ENDC)

    except requests.exceptions.ReadTimeout:
        print_warning("ReadTimeout")
        pass
    except requests.exceptions.ProxyError:
        print_warning("ProxyError")
        pass
    except requests.exceptions.ConnectionError:
        print_warning("ConnectionError")
        pass


def find_field_token(content):
    field_token = content[content.find("field-authenticity-token"):]
    field_token = field_token[field_token.find("name=\"") + len("name=\""):]
    return field_token[:field_token.find("\"")]


def find_sec_token(content):
    sec_token = content[content.find("security-token"):]
    sec_token = sec_token[sec_token.find("value=\"") + len("value=\""):]
    return sec_token[:sec_token.find("\"")]


def find_checkbox(content, op):
    option = content[content.find("options"):]
    option = option[option.find("value=\"") + len("value=\""):]
    option = option[:option.find("\"")]
    try:
        return int(option) + op - 1
    except ValueError:
        return 0


def print_warning(warning):
    print(WARNING + warning + ENDC)


init(full_args)
