texto=input("Escribe un texto o un poema:")
numero_letras=texto.lower().count('a')
print(texto)
print(f"Hay {numero_letras} letras 'a' en el texto")
texto_lista=texto.split()
palabras_texto_lista=len(texto_lista)
print(f"Hay {palabras_texto_lista} palabras en el texto")
print(f"La primera palabra del texto es: {texto[0]} y la ultima es: {texto[-1]}")
print("Al reves el texto quedaria asi: "+" ".join(reversed(texto_lista)))
esta_py='python' in texto_lista
esta_o_no_esta_py={True:'si',False:'no'}
print(f'la palabra "python" {esta_o_no_esta_py[esta_py]} esta en el texto')
