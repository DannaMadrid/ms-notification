from flask import Blueprint, request, jsonify
from Services.emailService import send_email
from Services.templateService import load_html_template

ResetPassword_blueprint = Blueprint('resetPassword', __name__)

@ResetPassword_blueprint.route('', methods=['POST'])
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