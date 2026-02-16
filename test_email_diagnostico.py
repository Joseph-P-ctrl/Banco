"""
Script de diagnóstico para envío de correo Microsoft 365
"""
import smtplib
from email.message import EmailMessage
import socket

SENDER = 'u212prac01@distriluz.com.pe'
PASSWORD = 'Pr4ct2..2026'
RECIPIENT = 'u212prac01@distriluz.com.pe'

print("=== Diagnóstico de Conexión Microsoft 365 ===\n")

# 1. Verificar conectividad de red
print("1. Verificando conectividad de red a smtp.office365.com...")
try:
    socket.create_connection(("smtp.office365.com", 587), timeout=10)
    print("   ✓ Conexión de red exitosa\n")
except Exception as e:
    print(f"   ✗ Error de conexión de red: {e}\n")
    exit(1)

# 2. Verificar conexión SMTP
print("2. Conectando a SMTP...")
try:
    smtp = smtplib.SMTP('smtp.office365.com', 587, timeout=30)
    print("   ✓ Conexión SMTP establecida\n")
    
    # 3. EHLO inicial
    print("3. Enviando EHLO inicial...")
    code, response = smtp.ehlo()
    print(f"   Código: {code}")
    print(f"   Respuesta: {response.decode()[:200]}...\n")
    
    # 4. STARTTLS
    print("4. Iniciando STARTTLS...")
    smtp.starttls()
    print("   ✓ STARTTLS iniciado\n")
    
    # 5. EHLO después de STARTTLS
    print("5. Enviando EHLO después de STARTTLS...")
    code, response = smtp.ehlo()
    print(f"   Código: {code}")
    print(f"   Respuesta: {response.decode()[:200]}...\n")
    
    # 6. Autenticación
    print("6. Intentando autenticación...")
    print(f"   Usuario: {SENDER}")
    print(f"   Contraseña: {'*' * len(PASSWORD)}")
    try:
        smtp.login(SENDER, PASSWORD)
        print("   ✓ Autenticación exitosa!\n")
        
        # 7. Enviar correo de prueba
        print("7. Intentando enviar correo de prueba...")
        msg = EmailMessage()
        msg['Subject'] = 'Prueba diagnóstico - Microsoft 365'
        msg['From'] = SENDER
        msg['To'] = RECIPIENT
        msg.set_content('Este es un correo de prueba de diagnóstico.')
        
        smtp.send_message(msg)
        print("   ✓✓✓ CORREO ENVIADO EXITOSAMENTE! ✓✓✓\n")
        
    except smtplib.SMTPAuthenticationError as e:
        print(f"   ✗ Error de autenticación: {e}\n")
        print("   POSIBLES CAUSAS:")
        print("   - La autenticación SMTP no está habilitada en Microsoft 365")
        print("   - El usuario o contraseña son incorrectos")
        print("   - La cuenta requiere autenticación moderna (OAuth2)")
        print("   - Autenticación de dos factores está activada")
        print("\n   SOLUCIONES:")
        print("   1. Inicia sesión en https://outlook.office365.com")
        print("   2. Ve a Configuración > Correo > Sincronización de correo electrónico")
        print("   3. Verifica que 'POP y SMTP autenticado' esté habilitado")
        print("   4. O contacta al administrador de TI para habilitar SMTP\n")
    except Exception as e:
        print(f"   ✗ Error al enviar: {e}\n")
    
    finally:
        smtp.quit()
        
except Exception as e:
    print(f"   ✗ Error general: {e}\n")

print("\n=== Fin del diagnóstico ===")
