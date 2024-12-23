import pandas as pd
import requests
import re
import os
from dotenv import load_dotenv
# Cargar variables del archivo .env
load_dotenv()

# Usar las claves
mailgun_api_key = os.getenv('MAILGUN_API_KEY')
mailgun_url = os.getenv('MAILGUN_URL')

def send_email_with_resumes(email, name, company):
    try:
        # Create a log of sent emails to avoid duplicates
        if not os.path.exists("emails.csv") or os.path.getsize("emails.csv") == 0:
            emails_df = pd.DataFrame(columns=['email'])
        else:
            emails_df = pd.read_csv('emails.csv', delimiter=',')

        if email in emails_df['email'].values:
            print("Email already sent to this address.")
            return "Email already sent", None

        # Email content
        subject = "Candidatos para Desarrollador Backend"
        body = f"""Hola {name},

Sabemos lo importante que es encontrar el talento ideal para el puesto de Desarrollador Backend que publicaste recientemente. Desde nuestra plataforma de reclutamiento, hemos analizado el perfil de la vacante y seleccionamos automáticamente a tres candidatos que podrían encajar con tus necesidades.

Te comparto un vistazo de lo que puedes encontrar al usar nuestra plataforma:

1. John Alexander Arias Díaz
   - Tecnologías: Python, Django, AWS, Docker, .Net
   - Experiencia: Más de 5 años desarrollando arquitecturas escalables y optimizando procesos backend para empresas de tecnología.
   - Salario esperado: COP $9.000.000 - $11.000.000 mensuales.

2. César Augusto Torres Ardila
   - Tecnologías: Java, Spring Boot, Kubernetes, Git.
   - Experiencia: 4 años en desarrollo backend para proyectos de alta complejidad, incluyendo contribuciones en repositorios de código abierto (GitHub).
   - Salario esperado: COP $8.000.000 - $10.000.000 mensuales.

3. Johan Rojas Rodríguez
   - Tecnologías: Node.js, Express, MongoDB, Azure.
   - Experiencia: Más de 3 años desarrollando e implementando soluciones backend, con enfoque en aplicaciones rápidas y seguras.
   - Salario esperado: COP $7.000.000 - $9.000.000 mensuales.

¿Por qué elegir nuestra plataforma?
Nuestra tecnología utiliza IA para hacer match en tiempo real entre las vacantes y nuestra base de datos de candidatos disponibles. Esto te ahorra tiempo y garantiza que siempre veas perfiles relevantes como los que te compartimos aquí.

Puedes explorar estos y otros perfiles directamente en nuestra plataforma. También ofrecemos una prueba gratuita para que descubras cómo puedes optimizar tu proceso de selección.

¿Te interesa probarlo? Responde a este correo y te compartimos acceso para que lo explores por ti mismo.

Saludos,
Santiago González Ramírez
Lider de plataforma PeakU
"""

        # Attach resumes
        attachments = []
        for filename in ["jhon.pdf", "cesar.pdf", "johan.pdf"]:
            with open(filename, "rb") as f:
                attachments.append(("attachment", (filename, f.read(), "application/pdf")))

        # Send the email via Mailgun
        response = requests.post(
            mailgun_url,
            auth=("api", mailgun_api_key),
            data={
                "from": "Santiago de PeakU <santiago@peaku.co>",
                "to": [email],
                "subject": subject,
                "text": body
            },
            files=attachments
        )
        response.raise_for_status()
        
        # Log sent email
        emails_df = pd.concat([emails_df, pd.DataFrame({'email': [email]})])
        emails_df.to_csv('emails.csv', index=False)
        print(f"Email sent successfully to {email}")
        return "Email sent successfully", response.json()['id']

    except requests.exceptions.RequestException as err:
        print(f"Error sending email: {err}")
        return "Error sending email", None

# Load and process data from Excel
data = pd.read_excel('mailtosend.xlsx', engine='openpyxl')

delivered_emails = []

# Iterate over recipients and send emails
for index, row in data.iterrows():
    recipient_email = str(row["email"])
    recipient_name = str(row["first_name"])
    recipient_company = str(row["company_name"])

    # Validate email format
    email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    if re.match(email_regex, recipient_email):
        status, email_id = send_email_with_resumes(recipient_email, recipient_name, recipient_company)
        if "Email sent successfully" in status:
            delivered_emails.append(recipient_email)

# Save the list of delivered emails to a text file
with open("delivered_emails.txt", "w") as f:
    for email in delivered_emails:
        f.write(email + "\n")

print("All emails processed.")
