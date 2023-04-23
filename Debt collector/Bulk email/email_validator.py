import requests
import keys

def validate_email():
    # Make a GET request to the Mailgun validation endpoint
        return requests.post(
            "https://api.mailgun.net/v4/address/validate",
            auth=("api", keys.mailgun_api_key),
            params={"address": 'santiagopsa@gmail.com'})

result = validate_email()
print(result.reason)
print(result.json())