from time import sleep
import requests
import os
import winreg
import configparser
import atexit
# Lee el archivo de configuración
config = configparser.ConfigParser()
config.read('config.cfg')

# Obtiene el usuario y la contraseña de la sección Credentials


proxy_enabled = config.get('Credentials' , 'proxy_system')
user = config.get('Credentials', 'user')
password = config.get('Credentials', 'pass')

#user = "xd"
#password = "123xd4"
#proxy_enabled = True
address = "proxy.uclv.cu"
port = "3128"

proxy_url  =  "http://" + user + ":" + password + "@" + address + ":" + port

url = "https://wifi.uclv.cu:8003/index.php?zone=uclv"

headers = {
    "content-type": "multipart/form-data; boundary=---011000010111000001101001"
}

data = """-----011000010111000001101001\r
Content-Disposition: form-data; name="auth_user"\r
\r
{}\r
-----011000010111000001101001\r
Content-Disposition: form-data; name="auth_pass"\r
\r
{}\r
-----011000010111000001101001\r
Content-Disposition: form-data; name="redirecturl"\r
\r
https://wwww.uclv.edu.cu\r
-----011000010111000001101001\r
Content-Disposition: form-data; name="accept"\r
\r
Login\r
-----011000010111000001101001--\r
""".format(user, password)

params = {"zone": "uclv"}


def disable_proxy():
    INTERNET_SETTINGS = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Internet Settings',0, winreg.KEY_ALL_ACCESS)
    winreg.SetValueEx(INTERNET_SETTINGS, 'ProxyEnable', 0, winreg.REG_DWORD, 0)
    winreg.CloseKey(INTERNET_SETTINGS)


atexit.register(disable_proxy) # <-- registrar la función `disable_proxy`


print("********************************************************************")
print("...Creado por Freddy Javier Saez Avila, estudiante de 1ero Ciencia de la computación \n* Bienvenido a La Puerta, esta aplicación te ayudará a acceder a los beneficios de la red uclv. Verifica que ya estés conectado a ésta(por wifi, cable, telepatía, lo que sea).\n")
print("********************************************************************\n\n")



print("Sin más, trataré de loguearte en la red uclv")

while True:
    try:
        response = requests.post(url, headers=headers, params=params, data=data)
        response.raise_for_status()
        # Se configura el proxy en el sistema
        INTERNET_SETTINGS = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Internet Settings',0, winreg.KEY_ALL_ACCESS)

        if proxy_enabled == "1":
            winreg.SetValueEx(INTERNET_SETTINGS, 'ProxyEnable', 0, winreg.REG_DWORD, 1)
            winreg.SetValueEx(INTERNET_SETTINGS, 'ProxyServer', 0, winreg.REG_SZ, f'{address}:{port}')
            winreg.SetValueEx(INTERNET_SETTINGS, 'ProxyUser', 0, winreg.REG_SZ, user)
            winreg.SetValueEx(INTERNET_SETTINGS, 'ProxyPass', 0, winreg.REG_SZ, password)
            print("********************************************************************\n\n")
            print("Felicidades perro, estás conectado. \nSe configuró el proxy de la UCLV en tu sistema, \nsi no quieres que este programa cambie tu configuracion de proxy de windows, \npuedes desactivar esta opción en el archivo config.cfg\n\n\nNo cierres esta ventana. Presiona Enter para cuando quieras terminar tu conexión ...")
            print("********************************************************************\n\n")
        else:
            winreg.SetValueEx(INTERNET_SETTINGS, 'ProxyEnable', 0, winreg.REG_DWORD, 0)
            print("********************************************************************\n\n")
            print("Felicidades perro, estás conectado. \nYa puedes cerrar este programa y activar el proxy en tu PC")
            print("********************************************************************\n\n")

        winreg.CloseKey(INTERNET_SETTINGS)
        break
    except Exception as e:
        print(f"\n---Hubo un error: Asegurate de que éste programa tenga acceso a {url}")
        for i in range(1,5):
            s=""
            for j in range(1, i):
                s+='.'
            print (s)
            sleep(2)
close = input()
