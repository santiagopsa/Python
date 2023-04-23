import pandas as pd
import requests
import keys
import re
import os

def send_simple_message(email,name,company,code):
    try:
        # Creating a sent emails csv file in case the code fails or there are repeted emails
        if not os.path.exists("emails.csv") or os.path.getsize("emails.csv") == 0:
            emails_df = pd.DataFrame(columns=['email'])
        else:
            emails_df = pd.read_csv('emails.csv', delimiter=',')

        if email in emails_df['email'].values:
            print("Email already sent to this address.")
            return "Email already sent", None

        with open("validadores.pdf", "rb") as f:
            attachment = f.read()
        response = requests.post(
            keys.mailgun_url,
            auth=("api", keys.mailgun_api_key),
            data={"from": "Rosa <rosa@peaku.co>",
                  "to": [email],
                  "subject": f"Base de datos candidatos {company} ",
                  "html": f'''Hola {name},<br><br>

Quería compartirles nuestra base de candidatos validados en la industria de {company}<br><br>

Aquí pueden buscar candidatos de acuerdo a la experiencia que estén buscando.<br><br>

Mientras tanto les dejo un link para que puedas ver como funciona<br>

https://peaku.co/es/empresas/usuarios?work_area_code={code}<br><br>

Igual si quieres aprovechar al máximo la plataforma y ver todas las funcionalidades, me compartes tu whatsapp y nos conectamos<br><br>

Si no eres la persona encargada en recursos humanos, le puedes reenviar este correo :)<br><br>

Igual si quieres mas información, me cuentas !<br><br>

Saludos, <br>
Rosa de PeakU.<br>
rosa@peaku.co<br>
COLBD23_CAT<br><br><br><br><br>
<a href="%unsubscribe_url%">Click aquí para desuscribir</a>'''},
            files=[("attachment", ("validadores.pdf", attachment, "application/pdf"))])
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
df = pd.read_excel('col_2023.xls', engine='xlrd')

# Convert to CSV
df.to_csv('col_2023.csv', index=False)
data = pd.read_csv("col_2023.csv")
delivered_emails = []
data["rep_legal"].fillna("", inplace=True)

for index, row in data.iterrows():
    recipient_email = str(row["correo_comercial"])
    recipient_name = str(row["rep_legal"])
    recipient_company = str(row["razon_social"])
    recipient_code = str(row["codigo"])
    if recipient_name != '':
        first_name = recipient_name.split()[0]
    if recipient_company != '':
        company_name = recipient_company.split()[0]
    first_camel = ''.join(x for x in first_name.title() if not x.isspace())
    company_camel = ''.join(x for x in company_name.title() if not x.isspace())
    email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    email_regex_no_space = r"^\S+@\S+\.\S+$"
    if re.match(email_regex, recipient_email) and re.match(email_regex_no_space, recipient_email) and recipient_email[-1]!='.':
    # send email
        salida, id = send_simple_message(recipient_email,first_camel,company_camel,recipient_code)
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
