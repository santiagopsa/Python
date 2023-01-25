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

        with open("Infografico_PeakU.pdf", "rb") as f:
            attachment = f.read()
        response = requests.post(
            keys.mailgun_url,
            auth=("api", keys.mailgun_api_key),
            data={"from": "Santiago de PeakU <santiago@peaku.co>",
                  "to": [email],
                  "subject": f"{name} - PeakU <> {company} ",
                  "text": f'''Hola {name},

Encontrar empleados comprometidos que realmente traigan valor, ha sido una de las tareas más dificiles en mi camino como emprendedor.

Mi nombre es Santiago y quería compartir contigo una plataforma que creamos con el objetivo de resolver este problema:

Reinventamos la selección! 
En lugar de hacer pruebas estandarizadas, hacemos simulaciones de situaciones reales del día a día acorde al perfil que estés buscando.
 
¿Y por qué esto es mejor?

Estudios han demostrado que el mejor predictor de desempeño en cualquier tarea, es hacer la tarea en sí misma.

Usamos IA para reproducir esas situaciones de la vida real, ya sea escribiendo código para aplicaciones reales o simulando conversaciones con clientes potenciales (role-play). Además, nuestra IA aprende de miles de casos anteriores para sugerirte al candidato ideal.

Los resultados son absolutamente impresionantes. Nuestra plataforma le entrega a nuestros clientes los mejores candidatos y les permite mejorar la productividad y aumentar la retención de los buenos empleados!
Te comparto un infográfico que explica cómo funciona lo que hacemos, porque estoy convencido de que {company} es de las empresas que realmente puede usar todo el potencial de la plataforma.
Por esta razón, quiero darles un usuario para {company} (sin costo), el cual podrán activar durante el mes de Enero.
Tenemos usuarios limitados!
Quedo atento a que me confirmes si te gustaría activarlo o lo asigno a a alguien más :)

¿Tienes un espacio para que nos conectemos y crearte un usuario de prueba?, si es así comparteme tu numero y cuadramos por Whatsapp

Nota: esta oferta solo aplica para clientes nuevos !

Saludos, 
Santiago de PeakU.
santiago@peaku.co
https://peaku.co/es/empresas'''},
            files=[("attachment", ("Infografico_PeakU.pdf", attachment, "application/pdf"))])
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
df = pd.read_excel('mailtosend.xls', engine='xlrd')

# Convert to CSV
df.to_csv('mailtosend.csv', index=False)
data = pd.read_csv("mailtosend.csv")
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

