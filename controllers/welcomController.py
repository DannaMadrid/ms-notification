from flask import Blueprint, request, jsonify
from Services.emailService import send_email
from Services.templateService import load_html_template

welcome_blueprint = Blueprint('welcome', __name__)

@welcome_blueprint.route('', methods=['POST'])
def send_welcome_email():
    data = request.json
    recipient = data.get('recipient')
    username = data.get('username')

    template = load_html_template('bienvenida.html')
    if not template:
        return jsonify({'error': 'Template not found'}), 404

    body_html = template.render(username=username)
    subject = "Bienvenido a Nuestro Servicio"
    success = send_email(subject, recipient, body_html)

    if success:
        return jsonify({'message': 'Email sent successfully'})
    else:
        return jsonify({'error': 'Failed to send email'})
