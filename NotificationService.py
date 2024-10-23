import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)

#env = Environment(loader=FileSystemLoader('templates'))
env = Environment(loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')))
# Función para leer un archivo HTML desde la carpeta templates
def load_html_template(template_name):
    try:
        template = env.get_template(template_name)
        return template
    except Exception:
        return None

# Función para enviar correos
def send_email(subject, recipient_email, body_html):
    email_sender = os.getenv('GoogleMail__EmailSender')
    email_password = os.getenv('GoogleMail__ApiKey')
    smtp_server = os.getenv('GoogleMail__Host')
    smtp_port = os.getenv('GoogleMail__Port')

    print(f'Email sender: {email_sender}')
    print(f'Email password: {email_password}')
    print(f'SMTP server: {smtp_server}')
    print(f'SMTP port: {smtp_port}')

    # Crear el mensaje
    msg = MIMEMultipart()
    msg['From'] = email_sender
    msg['To'] = recipient_email
    msg['Subject'] = subject

    # Agregar el cuerpo del mensaje en formato HTML
    msg.attach(MIMEText(body_html, 'html'))

    try:
        # Conectar al servidor SMTP de Gmail
        with smtplib.SMTP(smtp_server, int(smtp_port)) as server:
            server.starttls()  # Asegura la conexión
            server.login(email_sender, email_password)
            server.sendmail(email_sender, recipient_email, msg.as_string())

        return True
    except Exception as e:
        return False, str(e)

# Endpoint para enviar el correo
@app.route('/welcom', methods=['POST'])
def Send_welcom():
    data = request.json
    recipient = data.get('recipient')
    username = data.get('username')
    
    template = load_html_template('bienvenida.html')
    if not template:
        return jsonify({'error': 'Template not found'}), 404

    body_html = template.render(username=username) 
    subject = "Bienvenido a Nuestro Servicio"
    if body_html:
        body_html = body_html.replace('{{ username }}', username)  # Reemplaza el marcador

        success = send_email(subject, recipient, body_html)
        print(f'Success: {success}')
        if success:
            print('Email sent successfully')
            return jsonify({'message': 'Email sent successfully'})
        else:
            print(f'Failed to send email')
            return jsonify({'error': 'Failed to send email'})
    else:
        return jsonify({'error': 'Template not found'})

#endpoint para enviar notificacion de pago        
@app.route('/paymentNotification', methods=['POST'])
def send_payment_notification():
    data = request.json
    recipient = data.get('recipient')
    username = data.get('username')
    amount = data.get('amount')
    description = data.get('description')

    # Cargar la plantilla de notificación de pago
    template = load_html_template('payment_notification.html')

    if not template:
        return jsonify({'error': 'Template not found'}), 404

    body_html = template.render(username=username, amount=amount, description=description)
    subject = "Confirmación de pago recibido"

    success = send_email(subject, recipient, body_html)
    if success:
        return jsonify({'message': 'Notification email sent successfully'})
    else:
        return jsonify({'error': 'Failed to send notification email'})

    


@app.route('/2FA', methods=['POST'])
def Send_2FA():

    data = request.json
    recipient = data.get('recipient')
    username = data.get('username')
    factor = data.get('factor')
    
    template = load_html_template('bienvenidados.html')
    
    if not template:
        return jsonify({'error': 'Template not found'}), 404

    body_html = template.render(username=username, factor=factor)
    subject = "Codigo de verificación"
    if body_html:
        body_html = body_html.replace('{{ username }}', username)  # Reemplaza el marcador
        body_html = body_html.replace('{{factor}}', factor)  # Reemplaza el marcador

        success = send_email(subject, recipient, body_html)
        print(f'Success: {success}')
        if success:
            print('Email sent successfully')
            return jsonify({'message': 'Email sent successfully'})
        else:
            print(f'Failed to send email')
            return jsonify({'error': 'Failed to send email'})
    else:
        return jsonify({'error': 'Template not found'})

@app.route('/resetPassword', methods=['POST'])
def Send_Password():
    data = request.json
    recipient = data.get('recipient')
    username = data.get('username')
    password = data.get('password')
    
    template = load_html_template('Password.html')
    
    if not template:
        return jsonify({'error': 'Template not found'}), 404

    body_html = template.render(username=username, password=password, email=recipient)
    subject = "Recuperacion de contraseña"
    if body_html:
        body_html = body_html.replace('{{ username }}', username)  # Reemplaza el marcador
        body_html = body_html.replace('{{email}}', recipient)  # Reemplaza el marcador
        body_html = body_html.replace('{{password}}', password)  # Reemplaza el marcador

        success = send_email(subject, recipient, body_html)
        print(f'Success: {success}')
        if success:
            print('Email sent successfully')
            return jsonify({'message': 'Email sent successfully'})
        else:
            print(f'Failed to send email')
            return jsonify({'error': 'Failed to send email'})
    else:
        return jsonify({'error': 'Template not found'})
if __name__ == "__main__":
    app.run(debug=True)