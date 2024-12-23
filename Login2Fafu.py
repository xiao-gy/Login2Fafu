import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse, parse_qs, urlencode
import random
import time
import json
import argparse

parser = argparse.ArgumentParser(description='Login to FAFU network')

parser.add_argument('-u', '--username', type=str, help='Username')
parser.add_argument('-p', '--password', type=str, help='Password')
parser.add_argument('-s', '--suffix', type=str, help='Suffix')
parser.add_argument('-s5', '--socks5_proxy', type=str, default=None, help='Proxy to Login')
parser.add_argument('-t', '--time_sleep', type=int, default=300, help='Time sleep')

accounts = []

socks5_proxy = ''

def get_login_params(socks5_proxy=None):
    url = 'http://2.2.2.2'
    try:
        r = requests.get(url,proxies=socks5_proxy,timeout=5)
    except Exception as e:
        print('Error: ', e)
        return None
    if  r.status_code == 200 :
        #print(r.text)
        soup = BeautifulSoup(r.text, 'html.parser')
        script_tag = soup.find('script', string=lambda text: "location.href" in text)
        if script_tag:
            #print(script_tag.text)
            script_text = script_tag.string
            url_pattern = r'location\.href="(.*?)"'
            url_match = re.search(url_pattern, script_text)
            if url_match:
                #print(url_match.group(1))
                parsed_url = urlparse(url_match.group(1))
                query_params = parse_qs(parsed_url.query)
                query_params['wlanusermac'][0] = query_params['wlanusermac'][0].replace('-', '').upper()
                print(query_params)
                return query_params
            else:
                print('Error: url not found')
    else :
        print('Error: ', r.status_code)
    return None

def login(params, account, socks5_proxy=None):
    checkLogin_url = 'http://210.34.84.127:801/eportal/portal/custom/checkLogin'
    checkLogin_params = {
        'callback': 'dr1003',
        'user_account': account['id'],
        'user_password': account['password'],
        'wlan_user_ip': params['wlanuserip'][0],
        'wlan_user_mac': params['wlanusermac'][0],
        'account_suffix': account['suffix'],
        'phone_flag': '1',
        'jsVersion': '4.2.1',
        'v': '5080',
        'lang': 'zh'
    }

    login_url = 'http://210.34.84.127:801/eportal/portal/login'
    login_params = params = {
        "callback": "dr1005",
        "login_method": "1",
        "user_account": f",1,{account['id']}{account['suffix']}",
        "user_password": account['password'],
        "wlan_user_ip": params['wlanuserip'][0],
        "wlan_user_ipv6": "",
        "wlan_user_mac": params['wlanusermac'][0],
        "wlan_ac_ip": params['wlanacip'][0],
        "wlan_ac_name": params['wlanacname'][0],
        "jsVersion": "4.2.1",
        "login_t": "4",
        "js_status": "0",
        "is_page": "1",
        "is_page_new": str(random.randint(10000, 99999)),
        "terminal_type": "2",
        "lang": "zh-cn",
        "v": "3497",
        "lang": "zh"
    }
    query_string = urlencode(checkLogin_params)
    #print(f"{checkLogin_url}?{query_string}")
    try:
        r = requests.get(f"{checkLogin_url}?{query_string}", proxies=socks5_proxy, timeout=5)
    except Exception as e:
        print('Error: ', e)
        return 0
    print(r.text)
    data = json.loads(r.text[r.text.find('{') : r.text.rfind('}')+1])
    if data.get('result') == -1:
        return 0
    time.sleep(1)
    query_string = urlencode(login_params)
    #print(f"{login_url}?{query_string}")
    try:
        r = requests.get(f"{login_url}?{query_string}", params=login_params, proxies=socks5_proxy, timeout=5)
    except Exception as e:
        print('Error: ', e)
        return 0
    print(r.text)
    data = json.loads(r.text[r.text.find('{') : r.text.rfind('}')+1])
    if data.get('ret_code') == -1:
        return -1
    return 1

if __name__ == '__main__':
    args = parser.parse_args()
    #print(args)
    time.sleep(args.time_sleep)
    if args.socks5_proxy:
        socks5_proxy = {'http': args.socks5_proxy}
        print(f"端口号{socks5_proxy['http'][socks5_proxy['http'].rfind(':')+1:]}:")
    accounts.append({'id': args.username, 'password': args.password, 'suffix': args.suffix},)
    params = get_login_params(socks5_proxy)
    if params:
        if login(params, accounts[0], socks5_proxy) == -1:
            exit()
        else:
            pass