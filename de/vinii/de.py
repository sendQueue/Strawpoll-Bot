"""
@author sendQueue <Vinii>
Further info at Vinii.de or github@vinii.de, file created at
19.11.2020 and last edited 20.12.2020. Use is only authorized if given credit!
"""

import argparse
import re
import threading
import time

import requests

parser = argparse.ArgumentParser(description="This script is ONLY for the .de version of Strawpoll")
parser.add_argument("id", help="Strawpoll ID -> .de/xxxx (xxxx is the id)")
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
                                    
        \033[93m strawpoll.de \033[0mip bypassing voting bot
                                  - by Vinii | sendQueue    
                                                  
"""


def init(args):
    print(motd)

    get_header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko)'
                      'Chrome/87.0.4280.88 Safari/537.36'}
    post_header = \
        {
            'Host': 'strawpoll.de',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko)'
                          'Chrome/87.0.4280.88 Safari/537.36',
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': 'https://strawpoll.de/' + args.id,
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Length': '31',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache',
            'Connection': 'close'
        }
    url = "https://strawpoll.de/" + args.id

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

            thread = threading.Thread(target=do_poll, args=(url, args.id, get_header, post_header, option, proxy, to))
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


def do_poll(url, id, get_header, post_header, op, proxy, to):
    proxies = {"https": "http://" + proxy}
    if len(proxy) < 4:
        return

    try:
        req = requests.get(url, get_header, proxies=proxies, timeout=to)
        # find oids --> "checkbox id"
        oids = "check" + str(find_checkbox(req.text, op))

        page = requests.post("https://strawpoll.de/vote", cookies=req.cookies, data={"pid": id, "oids": oids},
                             headers=post_header,
                             proxies=proxies, timeout=to)

        if "Set-Cookie" in page.headers:
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


def find_checkbox(content, op):
    checkbox = content[:content.find("check1")]
    checkbox = checkbox[len("id=\"check1"):]
    checkbox = checkbox[checkbox.find("checkbox\" name=\""):]
    checkbox = checkbox[len("checkbox\" name=\""):]
    checkbox = checkbox[:checkbox.find("\"")]
    match = re.match(r"([a-z]+)([0-9]+)", checkbox, re.I)
    if match:
        item = match.groups()
        # add option id
        return int(item[1]) + op - 1
    return 0


def print_warning(warning):
    print(WARNING + warning + ENDC)


init(full_args)
