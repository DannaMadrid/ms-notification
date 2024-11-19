from flask import Blueprint, request, jsonify
from Services.emailService import send_email
from Services.templateService import load_html_template

pruebaConexion_blueprint = Blueprint('PruebaConexion', __name__)

@pruebaConexion_blueprint.route('', methods=['POST'])
def PruebaConexion():

    data = request.json
    recipient = data.get('recipient')
    movie = data.get('movie')
    
    template = load_html_template('conexionMsLog.html')
    
    if not template:
        return jsonify({'error': 'Template not found'}), 404

    body_html = template.render(movie=movie)
    subject = "Pruba de conexion con ms-log"
    if body_html:
        body_html = body_html.replace('{{movie}}', movie)  # Reemplaza el marcador

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