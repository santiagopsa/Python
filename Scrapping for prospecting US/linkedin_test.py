import requests
import keys

url = 'https://www.linkedin.com/oauth/v2/introspectToken'

access_token = keys.linkedin_access_token
client_id = keys.linkedin_Client_id
client_secret = keys.linkedin_Client_secret

headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
}

data = {
    'token': access_token,
    'client_id': client_id,
    'client_secret': client_secret
}

response = requests.post(url, headers=headers, data=data)
data = response.json()

# Print the response data
print(data)
