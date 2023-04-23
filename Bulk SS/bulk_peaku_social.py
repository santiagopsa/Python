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

        with open("seguridad_social.pdf", "rb") as f:
            attachment = f.read()
        response = requests.post(
            keys.mailgun_url,
            auth=("api", keys.mailgun_api_key),
            data={"from": "Stephanny <stephanny@peaku.co>",
                  "to": [email],
                  "subject": f"Seguridad social - {company} ",
                  "text": f'''Hola {name},

Espero que estes muy bien,

En PeakU, nos hemos dado a la tarea de especializarnos en todo el proceso de afiliación y administración de empleados ante los diferentes proveedores de seguridad social.

Estaba viendo lo que hace {company} y quería mostrarles como funciona pues pienso que les podría servir de verdad.

Dentro las funciones de la plataforma están:

1. Afiliación de empleados ante los proveedores de seguridad social
2. Manejo de novedades como vacaciones, incapacidades, permisos, entre otros
3. Creación mensual de planilla para todos los empleados y envío del link para pago
4. Emisión de colillas de pago para enviar a tus colaboradores
5. Creación de cartas o certificados requeridos por los empleados

Además te asignamos un agente para que puedas resolver cualquier duda que tengas durante el proceso.

¿Tienes un espacio para que nos conectemos en una llamada y te pueda mostrar cómo funciona y darte más detalles de la promoción que tenemos para ti?, 

si es así compárteme tu número y cuadramos por Whatsapp.

Si no eres la persona correcta para hacer uso de esta prueba, te agradezco reenviárselo a la persona encargada


Saludos, 
Stepha de PeakU.
stephanny@peaku.co'''},
            files=[("attachment", ("seguridad_social.pdf", attachment, "application/pdf"))])
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
df = pd.read_excel('2022_jan-2022_dec_db.xls', engine='xlrd')

# Convert to CSV
df.to_csv('2022_jan-2022_dec_db.csv', index=False)
data = pd.read_csv("2022_jan-2022_dec_db.csv")
delivered_emails = []
data["rep_legal"].fillna("", inplace=True)

for index, row in data.iterrows():
    recipient_email = str(row["correo_comercial"])
    recipient_name = str(row["rep_legal"])
    recipient_company = str(row["razon_social"])
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

# Save the list of delivered emails to a text file
with open("delivered_emails.txt", "w") as f:
    for email in delivered_emails:
        f.write(email + "\n")

#Correo de seguridad social
'''¡Hola! 
¿Tienes problemas con la seguridad social de tus empleados? 
¡Puede ser que no estés haciendo las cosas bien! 
Muchas empresas pagan la planilla mensualmente y ni siquiera tienen a sus empleados afiliados a salud, pensión o riesgos profesionales, ste es un proceso muy engorroso y lleno de detalles. 

¡PeakU es una plataforma de tecnología que te ayuda a hacer este proceso más fácil ! 
¡Déjanos mostrarte cómo! 
¡Hablamos pronto!'''