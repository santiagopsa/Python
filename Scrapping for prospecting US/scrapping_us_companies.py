import requests
import json
import keys

api_key = keys.crunchbase_api_key
url = 'https://api.crunchbase.com/api/v4/searches/organizations'

# Prepare the request headers and payload
headers = {
    'Content-Type': 'application/json',
    'x-cb-user-key': api_key
}

payload = {
    "field_ids": ["identifier"],
    "limit": 1000,
    "page": 1
}

count = 0

while True:
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    data = response.json()

    organizations = data['entities']

    if not organizations:
        print("No organizations found.")
        break
    else:
        for organization in organizations:
            properties = organization['properties']
            name = properties['identifier']['value']
            if name:
                print(name)
                count += 1

    # Check if there are more pages to retrieve
    paging = data.get('paging', {})
    next_page = paging.get('next')
    if not next_page:
        break

    # Update the payload with the next page number
    page_number = next_page.get('number')
    payload['page'] = page_number
    # Update the limit to the maximum available per page
    payload['limit'] = min(paging.get('total_items', 0) - count, 1000)

print("Total number of organizations retrieved:", count)
