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

        with open("catalogo.pdf", "rb") as f:
            attachment = f.read()
        response = requests.post(
            keys.mailgun_url_boreal,
            auth=("api", keys.mailgun_api_key_boreal),
            data={"from": "Caro de Boreal <borealreposteria@gmail.com>",
                  "to": [email],
                  "subject": f"{company} + Boreal Repostería- Regalos Corporativos ",
                  "text": f'''Hola {name},

¿Cómo estás?

Sabemos que las personas son el activo más importante de tu empresa y nosotros contamos con opciones espectaculares para sorprender a tu equipo de trabajo, colaboradores, clientes, etc.
Boreal Repostería es el aliado perfecto para que regales experiencias innovadoras y deliciosas que generan bienestar, logran un mayor sentido de pertenencia y te permiten tener empleados más felices, empoderados y comprometidos.

Mi nombre es Carolina Mejía, soy la creadora de Boreal y me encantaría compartirte nuestro Catálogo de Corporativos en el que puedes encontrar las diferentes opciones que manejamos para empresas y las formas de personalización de cada una. 
Podemos realizar empaques con tu identidad de marca, logo e incluir los postres que más te gusten de nuestro portafolio.
Podrías agendar producciones para temporadas especiales o negociar entregas parciales durante el año si así lo necesitas.

Para cotizaciones puedes escribirnos a nuestra línea de WhatsApp o correo y estaremos felices de ayudarte en lo que necesites.
WhatsApp 3113356963
Correo: borealreposteria@gmail.com
Tu equipo y {company} de trabajo se merece lo mejor y nosotros queremos ser tu aliado para generar bienestar en {company}.

Quedamos muy atentos a lo que necesiten de nuestra parte.
Saludos,'''},
            files=[("attachment", ("catalogo.pdf", attachment, "application/pdf"))])
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
df = pd.read_excel('large_file_test.xls', engine='xlrd')

# Convert to CSV
df.to_csv('large_file_test.csv', index=False)
data = pd.read_csv("large_file_test.csv")
delivered_emails = []

for index, row in data.iterrows():
    recipient_email = str(row["correo_comercial"])
    recipient_name = str(row["rep_legal"])
    recipient_company = str(row["razon_social"])
    first_name = recipient_name.split()[0]
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
