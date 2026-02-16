"""
Script alternativo para Microsoft Exchange (sin autenticación SMTP externa)
Intentando usar el servidor Exchange local
"""
import smtplib
from email.message import EmailMessage

SENDER = 'u212prac01@distriluz.com.pe'
PASSWORD = 'Pr4ct2..2026'
RECIPIENT = 'u212prac01@distriluz.com.pe'

print("=== Intentando con diferentes servidores SMTP ===\n")

# Lista de servidores SMTP que podríamos probar
servers = [
    ('smtp.office365.com', 587, 'STARTTLS'),
    ('outlook.office365.com', 587, 'STARTTLS'),
    ('mail.distriluz.com.pe', 587, 'STARTTLS'),
    ('mail.distriluz.com.pe', 25, 'STARTTLS'),
    ('smtp.distriluz.com.pe', 587, 'STARTTLS'),
    ('smtp.distriluz.com.pe', 25, 'STARTTLS'),
    ('exchange.distriluz.com.pe', 587, 'STARTTLS'),
    ('exchange.distriluz.com.pe', 25, 'STARTTLS'),
]

for server, port, method in servers:
    print(f"\nProbando: {server}:{port} ({method})")
    print("-" * 50)
    try:
        smtp = smtplib.SMTP(server, port, timeout=10)
        code, response = smtp.ehlo()
        print(f"✓ Conexión exitosa")
        print(f"  Respuesta EHLO: {code}")
        
        if method == 'STARTTLS':
            smtp.starttls()
            smtp.ehlo()
            print(f"✓ STARTTLS exitoso")
        
        # Intentar autenticación
        try:
            smtp.login(SENDER, PASSWORD)
            print(f"✓✓ AUTENTICACIÓN EXITOSA!")
            
            # Intentar enviar correo
            msg = EmailMessage()
            msg['Subject'] = 'Prueba Exchange - Servidor encontrado'
            msg['From'] = SENDER
            msg['To'] = RECIPIENT
            msg.set_content('Correo de prueba exitoso desde el servidor correcto.')
            
            smtp.send_message(msg)
            print(f"✓✓✓ CORREO ENVIADO EXITOSAMENTE!")
            print(f"\n*** USAR ESTE SERVIDOR: {server}:{port} ***\n")
            smtp.quit()
            break
            
        except smtplib.SMTPAuthenticationError as e:
            print(f"✗ Error de autenticación: {e}")
        except Exception as e:
            print(f"✗ Error al enviar: {e}")
        
        smtp.quit()
        
    except ConnectionRefusedError:
        print(f"✗ Conexión rechazada (puerto cerrado o firewall)")
    except TimeoutError:
        print(f"✗ Timeout (servidor no responde)")
    except Exception as e:
        print(f"✗ Error: {e}")

print("\n=== Fin de pruebas ===")
print("\nSi ningún servidor funcionó:")
print("1. Contacta al área de TI para obtener el servidor SMTP correcto")
print("2. Solicita que habiliten SMTP AUTH en tu cuenta")
print("3. O solicita un servidor de relay SMTP interno sin autenticación")
