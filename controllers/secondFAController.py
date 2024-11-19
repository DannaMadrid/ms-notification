from flask import Blueprint, request, jsonify
from Services.emailService import send_email
from Services.templateService import load_html_template

secondFA_blueprint = Blueprint('2FA', __name__)

@secondFA_blueprint.route('', methods=['POST'])
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