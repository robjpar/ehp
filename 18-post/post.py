import requests

target_url = 'http://10.0.2.14/dvwa/login.php'
# data_dict = {'username': 'blahblah', 'password': 'blahblah', 'Login': 'submit'}
data_dict = {'username': 'admin', 'password': 'password', 'Login': 'submit'}
response = requests.post(target_url, data=data_dict)
content = response.content.decode()
print(content)
