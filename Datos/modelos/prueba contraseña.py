import re

def validate():
    while True:
        password = input("Ingrese una contraseña: ")
        if len(password) < 8:
            print("Asegúrese de que su contraseña tenga al menos 8 caracteres")
        elif re.search('[0-9]', password) is None:
            print("Asegúrese de que su contraseña tenga un número")
        elif re.search('[A-Z]', password) is None:
            print("Asegúrese de que su contraseña tenga una letra mayúscula")
        else:
            print("Su contraseña parece correcta")
            break

validate()