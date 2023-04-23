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
            data={"from": "Santiago <s@peaku.co>",
                  "to": [email],
                  "subject": f"SaaS AI HR-Tech Startup <> {company} ",
                  "text": f'''Hi {name},


As a startup founder in HR and Edtech, we are using AI to transform the vetting process. I came across your investor thesis and believe our company aligns well with your investment strategy.

Attached is a one-pager with more information, and I would be happy to answer any questions. Are you available for a call or coffee next week?

Best regards,

Santiago.
santiago@peaku.co
https://www.linkedin.com/in/santiagogonzalezr/
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
df = pd.read_excel('rest_of_investors_no_time.xls', engine='xlrd')

# Convert to CSV
df.to_csv('rest_of_investors_no_time.csv', index=False)
data = pd.read_csv("rest_of_investors_no_time.csv")
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
