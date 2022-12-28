import re

def verificar_email(email):
    verificar=re.search(r'(^[\w]+)@([\w]+)([.]com$)|(^[\w]+)@([\w]+)[.]com[.](\w*)',email)
    print(verificar)
    if verificar != None:
        print('Ok')
    else:
        print('La dirección de email es incorrecta')

verificar_email('santiago@peakucom')