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

        with open("One-pager.pdf", "rb") as f:
            attachment = f.read()
        response = requests.post(
            keys.mailgun_url,
            auth=("api", keys.mailgun_api_key),
            data={"from": "Rosa <rosa@peaku.co>",
                  "to": [email],
                  "subject":  f"Encontro PeakU <> {company} ",
                  "html": f'''Oi, tudo bem?,<br><br>
Cara, tava querendo saber se a {company} faz avaliações recorrentes dos colaboradores em relação ao conhecimento, habilidades sociais, motivação e clima organizacional. A gente tem uma plataforma de avaliação com testes para os funcionários:<br><br>

<b>Cognitivo</b>: Velocidade de aprendizado e habilidade de resolver problemas.<br>
<b>Conhecimento</b>: Testes para avaliar conhecimento.<br>
<b>Habilidades sociais</b>: Traços de personalidade importantes.<br>
<b>Clima organizacional e plano de carreira</b>: Percepção dos colaboradores sobre a empresa e os colegas.<br><br>

Posso criar um usuário pra {company} pra vocês experimentarem. Você tem um tempinho pra gente se conectar e configurar o usuário de teste? Se tiver, me passa teu número e a gente combina pelo Whatsapp.<br><br>

Abraços,<br>
Rosa da PeakU<br>
rosa@peaku.co<br>
https://peaku.co/pt/sales/assessments<br>
BREP<br><br><br><br><br>
<a href="%unsubscribe_url%">Clique aqui para se desinscrever</a>'''},
            files=[("attachment", ("One-pager.pdf", attachment, "application/pdf"))])
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
df = pd.read_excel('Brasil-Mailings_1-50000.xls', engine='xlrd')

# Convert to CSV
df.to_csv('Brasil-Mailings_1-50000.csv', index=False)
data = pd.read_csv("Brasil-Mailings_1-50000.csv")
delivered_emails = []
#data["rep_legal"].fillna("", inplace=True)

for index, row in data.iterrows():
    recipient_email = str(row["correo_comercial"])
    #recipient_name = str(row["rep_legal"])
    recipient_company = str(row["razon_social"])
    #if recipient_name != '':
     #   first_name = recipient_name.split()[0]
    if recipient_company != '':
        company_name = recipient_company.split()[0]
    #first_camel = ''.join(x for x in first_name.title() if not x.isspace())
    first_camel=''
    company_camel = ''.join(x for x in company_name.title() if not x.isspace())
    email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    email_regex_no_space = r"^\S+@\S+\.\S+$"
    if re.match(email_regex, recipient_email) and re.match(email_regex_no_space, recipient_email) and recipient_email[-1]!='.':
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
