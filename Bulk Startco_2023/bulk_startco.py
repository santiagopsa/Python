import pandas as pd
import requests
import keys
import re
import os

def send_simple_message(email,name,company):
    try:
        # Creating a sent emails csv file in case the code fails or there are repeted emails
        if not os.path.exists("emails.csv") or os.path.getsize("emails.csv") == 0:
            emails_df = pd.DataFrame(columns=['email'])
        else:
            emails_df = pd.read_csv('emails.csv', delimiter=',')

        if email in emails_df['email'].values:
            print("Email already sent to this address.")
            return "Email already sent", None

        with open("one_pager.pdf", "rb") as f:
            attachment = f.read()
        response = requests.post(
            keys.mailgun_url,
            auth=("api", keys.mailgun_api_key),
            data={"from": "Dani <daniela.olaya@peaku.co>",
                  "to": [email],
                  "subject": f"{name} cuento con tu voto? :)",
                  "text": f'''Hola {name},
Me ayudas con tu voto? solo si te gusta nuestra Startup :)

Te paso el link, agradezco tu apoyo de antemano !

https://virtual-stage.eventtia.com/es/startcobogota23/stage/230304?module=Surveys&surveyId=10223

Daniela,
Executive at PeakU
daniela.olaya@peaku.co
Whatsapp: +57 3217763184
'''},
            files=[("attachment", ("one_pager.pdf", attachment, "application/pdf"))])
        response.raise_for_status()
        # Parse the JSON data returned by the API
        data = response.json()
        print(data['id'])
        print(email)
        output = "Email sent successfully"
        print(output)
        temporary_data = {'email': [email]}
        temporary_df = pd.DataFrame(temporary_data)
        emails_df = pd.concat([emails_df,temporary_df])
        emails_df.to_csv('emails.csv', index=False)
        return output, data['id']
    except requests.exceptions.HTTPError as errh:
        output = "HTTP Error:" + str(errh)
        print(output)
        return output, data['id']
    except requests.exceptions.ConnectionError as errc:
        output = "Error Connecting:" + str(errc)
        print(output)
        return output, data['id']
    except requests.exceptions.Timeout as errt:
        output = "Timeout Error:" + str(errt)
        print(output)
        return output
    except requests.exceptions.RequestException as err:
        output = "Something went wrong:" + str(err)
        print(output)
        return output, data['id']


# Load the Excel file
df = pd.read_excel('startco.xls', engine='xlrd')

# Convert to CSV
df.to_csv('startco.csv', index=False)
data = pd.read_csv("startco.csv")
delivered_emails = []
data["name"].fillna("", inplace=True)
data["firm"].fillna("", inplace=True)

for index, row in data.iterrows():
    recipient_email = str(row["email"])
    recipient_name = str(row["name"])
    recipient_company = str(row["firm"])
    if recipient_name != '':
        first_name = recipient_name.split()[0]
    if recipient_company != '':
        company_name = recipient_company.split()[0]
    first_camel = ''.join(x for x in first_name.title() if not x.isspace())
    company_camel = ''.join(x for x in company_name.title() if not x.isspace())
    email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    email_regex_no_space = r"^\S+@\S+\.\S+$"
    if re.match(email_regex, recipient_email) and re.match(email_regex_no_space, recipient_email):
        # send email
        salida, id = send_simple_message(recipient_email,first_camel,company_camel)
        if "Email sent successfully" in salida:
            delivered_emails.append(id)
            delivered_emails.append(recipient_email)
        elif "Email already sent" in salida:
            pass
        else:
            print("Invalid email address")
