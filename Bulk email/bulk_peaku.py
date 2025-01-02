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

def send_email_with_resumes(email, name, company, experiment_label):
    try:
        # Create a log of sent emails to avoid duplicates
        if not os.path.exists("emails.csv") or os.path.getsize("emails.csv") == 0:
            emails_df = pd.DataFrame(columns=['email'])
        else:
            emails_df = pd.read_csv('emails.csv', delimiter=',')

        if email in emails_df['email'].values:
            print("Email already sent to this address.")
            return "Email already sent", None

        # Define combinaciones de asuntos, cuerpos de mensaje y adjuntos con etiquetas
        experiments = {
            "A": {
                "subject": "Adjunto reporte de salarios tech en Colombia",
                "body": f"""Hola {name},

                Noté que en {company} están contratando perfiles tech, y quería pasarte un reporte de salarios en base a nuestra experiencia y base de datos. Te adjunto, totalmente gratis, nuestro **Reporte de Salarios para Desarrolladores en Colombia**, que incluye:

                • Salarios promedio según años de experiencia (Junior, Mid, Senior).  
                • Rangos de compensación por stack de tecnología (Backend, Frontend, Full-Stack, etc.).  

                El objetivo es que puedas comparar fácilmente los montos de referencia en el mercado actual y así ajustar tus decisiones de reclutamiento en base a los datos del mercado.

                **Aclaración**: Contamos con un software SaaS especializado en contratar perfiles TI. Sin embargo, primero prefiero compartirte este documento y si necesitas acceso a nuestra plataforma, te lo puedo dar.

                Si te interesa profundizar más o tienes dudas sobre cómo optimizar tus procesos de reclutamiento, ¡cuenta conmigo!


            Saludos,
            Santiago González Ramírez
            Lider de plataforma PeakU
            """,
                "attachments": ["estudio-salarios.pdf"]
            },
            "B": {
                "subject": "Desarrolladores Backend filtrados",
                "body": f"""Hola {name},

            Estamos emocionados de presentarte a nuestros candidatos más destacados para el puesto de Desarrollador Backend. Nuestra plataforma ha seleccionado automáticamente a tres candidatos que podrían ser perfectos para tu empresa.

            Aquí tienes un resumen de sus perfiles:

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

            Descubre cómo nuestra plataforma puede ayudarte a encontrar el talento ideal de manera rápida y eficiente. Ofrecemos una prueba gratuita para que puedas explorar todas nuestras funcionalidades.

            ¿Te gustaría probarlo? Responde a este correo y te daremos acceso inmediato.

            Saludos,
            Santiago González Ramírez
            Lider de plataforma PeakU
            """,
                "attachments": ["jhon.pdf", "cesar.pdf", "johan.pdf"]
            },
            "C": {
                "subject": "Prueba gratuita: Evalúa a tu próximo backend developer sin costo",
                "body": f"""Hola {name},

            He visto que {company} está en la búsqueda de un desarrollador backend. Quiero ofrecerte **acceso gratuito** a nuestra plataforma para que encuentres y evalúes a tus candidatos tech de manera rápida y eficaz.

            ¿Cómo funciona?
            1. Te doy un acceso de prueba a nuestro módulo específico para reclutamiento backend.  
            2. Subes los CVs o referencias de los candidatos que ya tengas (o publicas tu vacante).  
            3. La plataforma analiza automáticamente su experiencia, stack de tecnologías y habilidades clave, mostrándote quién se ajusta mejor a tus necesidades.

            Gracias a este acceso podrás ver cómo la automatización de nuestro SaaS reduce el tiempo de evaluación y te ayuda a priorizar a los candidatos más prometedores.

            **Aclaración**: Nuestro modelo de negocio consiste en una suscripción mensual para empresas que reclutan perfiles TI de forma recurrente. Sin embargo, antes de proponerte nada, prefiero que pruebes por ti mismo cómo funciona.

            ¿Qué te parece?  
            ¿Te gustaría probarlo para ver que tal funciona?

            Saludos,
            Santiago González Ramírez
            Lider de plataforma PeakU
            """,
                "attachments": []
            }
            # Puedes agregar más combinaciones aquí
        }

        # Seleccionar el asunto, cuerpo de mensaje y adjuntos basado en la etiqueta del experimento
        selected_experiment = experiments[experiment_label]
        subject = selected_experiment["subject"]
        body = selected_experiment["body"]
        attachment_files = selected_experiment["attachments"]

        # Attach resumes
        attachments = []
        for filename in attachment_files:
            try:
                with open(filename, "rb") as f:
                    attachments.append(("attachment", (filename, f.read(), "application/pdf")))
            except FileNotFoundError:
                print(f"Error: El archivo {filename} no se encontró.")
            except IOError as e:
                print(f"Error al abrir el archivo {filename}: {e}")

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
        status, email_id = send_email_with_resumes(recipient_email, recipient_name, recipient_company, "A")
        if "Email sent successfully" in status:
            delivered_emails.append(recipient_email)

# Save the list of delivered emails to a text file
with open("delivered_emails.txt", "w") as f:
    for email in delivered_emails:
        f.write(email + "\n")

print("All emails processed.")
