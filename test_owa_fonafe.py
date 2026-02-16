"""
Prueba de envío con el servidor owa.fonafe.gob.pe
"""
import smtplib
from email.message import EmailMessage

SENDER = 'u212prac01@distriluz.com.pe'
PASSWORD = 'Pr4ct2..2026'
RECIPIENT = 'u212prac01@distriluz.com.pe'

print("=== Probando servidor: owa.fonafe.gob.pe ===\n")

# Probar diferentes puertos
ports = [587, 25, 465]

for port in ports:
    print(f"\n{'='*60}")
    print(f"Probando puerto: {port}")
    print('='*60)
    
    try:
        if port == 465:
            # SSL directo
            print("Usando SMTP_SSL...")
            smtp = smtplib.SMTP_SSL('owa.fonafe.gob.pe', port, timeout=30)
            smtp.ehlo()
        else:
            # STARTTLS
            print("Usando SMTP con STARTTLS...")
            smtp = smtplib.SMTP('owa.fonafe.gob.pe', port, timeout=30)
            code, response = smtp.ehlo()
            print(f"✓ EHLO: {code}")
            smtp.starttls()
            print("✓ STARTTLS exitoso")
            smtp.ehlo()
        
        print("Intentando autenticación...")
        smtp.login(SENDER, PASSWORD)
        print("✓✓ AUTENTICACIÓN EXITOSA!")
        
        # Enviar correo de prueba
        print("Enviando correo de prueba...")
        msg = EmailMessage()
        msg['Subject'] = 'Prueba exitosa - owa.fonafe.gob.pe'
        msg['From'] = SENDER
        msg['To'] = RECIPIENT
        msg.set_content('¡Correo de prueba enviado exitosamente desde el sistema!\n\nServidor: owa.fonafe.gob.pe\nPuerto: ' + str(port))
        
        smtp.send_message(msg)
        print("✓✓✓ CORREO ENVIADO EXITOSAMENTE!")
        print(f"\n*** CONFIGURACIÓN CORRECTA ***")
        print(f"Servidor: owa.fonafe.gob.pe")
        print(f"Puerto: {port}")
        print(f"Método: {'SSL' if port == 465 else 'STARTTLS'}")
        
        smtp.quit()
        break
        
    except Exception as e:
        print(f"✗ Error: {e}")
        print(f"  Tipo: {type(e).__name__}")

print("\n" + "="*60)
print("Fin de pruebas")
print("="*60)
