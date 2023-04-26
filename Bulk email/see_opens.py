import requests
import keys
import pandas as pd

endpoint = f"https://api.mailgun.net/v3/{keys.mailgun_domain}/events"
params = {"begin": "Mon, 23 Jan 2023 13:00:00 EST", "ascending": "yes", "limit":"300"}
response = requests.get(
    endpoint,
    auth=("api", keys.mailgun_api_key),
    params=params
)
df= pd.DataFrame(columns=['email','status'])
response.raise_for_status()
data = response.json()
delivered_emails = []
count=0
for d in data.get('items'):
    #print(d)
    if '- PeakU <>' in d.get('message')['headers']['subject']:
        df1 = pd.DataFrame({
            'email':[d.get('recipient')],
            'status':[d.get('event')]
        },index=[count])
        df = pd.concat([df,df1])
        count += 1


df.to_csv('email_renponse.csv', index=False)


        #delivered_emails.append(d.get('recipient'))
        #delivered_emails.append(d.get('event'))

print(df)
    #print(d.keys())
  #  for m in d['message'].items():
   #     print(type(m[1]))
#print(data['items'][0]['message']['headers']['from'])