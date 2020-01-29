#!/usr/bin/env python3
# Sergey Chugay

import requests
import json
import operator
from operator import itemgetter
import time
import wget
import os
import argparse

# Get arguments of comand line


def get_args():
    parser = argparse.ArgumentParser(
        description="Please use argument for runnig script ./insta.py -u username")
    parser.add_argument("-u", "--username", required=True,
                        help="username of instagram")
    return parser.parse_args()


args = get_args()
who = args.username

# Headers for REST
headers = {'Content-Type': 'application/json; charset=UTF-8',
           'accept': 'application/json, text/javascript, */*; q=0.01'}

r = requests.get("https://instagram.com/%s/?__a=1" % who, headers=headers)
if r.ok:
    if os.path.isdir('./downloads_%s' % who):
        path = './downloads_%s' % who
    else:
        path = os.mkdir('./downloads_%s' % who)
    o = json.loads(r.text)[
        'graphql']['user']['edge_owner_to_timeline_media']['edges']

    urls_dis = list(map(itemgetter('display_url'),
                        list(map(itemgetter('node'), o))))

    for url in urls_dis:
        wget.download(url, './downloads_%s/%s.jpg' %
                      (who, time.strftime(who + "_%Y%m%d-%H%M%S")))
        time.sleep(1)
    print()
    print('Downloaded from %s' % who)
else:
    print('User not found')
