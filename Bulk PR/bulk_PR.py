import pandas as pd
import requests
import keys
import re
import os


def send_simple_message(email, name, company):
    try:
        # Creating a sent emails csv file in case the code fails or there are repeted emails
        if not os.path.exists("emails.csv") or os.path.getsize("emails.csv") == 0:
            emails_df = pd.DataFrame(columns=['email'])
        else:
            emails_df = pd.read_csv('emails.csv', delimiter=',')

        if email in emails_df['email'].values:
            print("Email already sent to this address.")
            return "Email already sent", None

        with open("Future_AI.docx", "rb") as f:
            attachment = f.read()
        response = requests.post(
            keys.mailgun_url,
            auth=("api", keys.mailgun_api_key),
            data={"from": "Santiago <santiago@peaku.co>",
                  "to": [email],
                  "subject": f"An Update on PeakU - {company}",
                  "text": f'''Hi {name},

I hope this email finds you well. I came across your work and I thought you might be interested in an article I recently wrote about PeakU

PeakU combines ATS with technical, cognitive, and personality tests, and global talent management tools. Its machine learning algorithm has seen growth due to the shift towards remote work, enabling companies to find top talent globally while saving time and money.

I've attached the article for your review. If you're interested in publishing it, I'd be more than happy to provide additional information or answer any questions you may have.

Best regards,
Santiago González
https://www.linkedin.com/in/santiagogonzalezr/
peaku.ai'''},
            files=[("attachment", ("Future_AI.docx", attachment, "application/vnd.openxmlformats-officedocument.wordprocessingml.document"))])
        response.raise_for_status()
        # Parse the JSON data returned by the API
        data = response.json()
        print(data['id'])
        print(email)
        output = "Email sent successfully"
        print(output)
        temporary_data = {'email': [email]}
        temporary_df = pd.DataFrame(temporary_data)
        emails_df = pd.concat([emails_df, temporary_df])
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
df = pd.read_excel('pr2.xls', engine='xlrd')

# Convert to CSV
df.to_csv('pr2.csv', index=False)
data = pd.read_csv("pr2.csv")
delivered_emails = []
data["Email"].fillna("", inplace=True)
data["Journalists Name"].fillna("", inplace=True)
data["Media name"].fillna("", inplace=True)

for index, row in data.iterrows():
    recipient_email = str(row["Email"])
    recipient_name = str(row["Journalists Name"])
    recipient_company = str(row["Media name"])
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
        salida, id = send_simple_message(recipient_email, first_camel, company_camel)
        if "Email sent successfully" in salida:
            delivered_emails.append(id)
            delivered_emails.append(recipient_email)
        elif "Email already sent" in salida:
            pass
        else:
            print("Invalid email address")

# Save the list of delivered emails to a text file
with open("delivered_emails.txt", "w") as f:
    for email in delivered_emails:
        f.write(email + "\n")