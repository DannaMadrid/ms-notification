from flask import Blueprint, request, jsonify
from Services.emailService import send_email
from Services.templateService import load_html_template

tranch_blueprint = Blueprint('tranch', __name__)

@tranch_blueprint.route('', methods=['POST'])
def new_order():
    data = request.json
    recipient = data.get('recipient')
    routeid = data.get('routeid')
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    origin = data.get('origin')
    destination = data.get('destination')

    if not isinstance(routeid, int):  # Verifica si routeid es un entero
        return jsonify({'error': 'El campo routeid debe ser un número'}), 400


    template = load_html_template('Tranches.html')
    if not template:
        return jsonify({'error': 'Template not found'}), 404

    body_html = template.render(routeid=routeid, start_date=start_date, end_date=end_date, origin=origin, destination=destination)
    subject = "Seguimiento de Tramo"
    if body_html:
        body_html = body_html.replace('{{ routeid }}', str(routeid))  # Reemplaza el marcador
        body_html = body_html.replace('{{ start_date }}', start_date)  # Reemplaza el marcador
        body_html = body_html.replace('{{ end_date }}', end_date)  # Reemplaza el marcador
        body_html = body_html.replace('{{ origin }}', origin)  # Reemplaza el marcador
        body_html = body_html.replace('{{ destination }}', destination)  # Reemplaza el marcador
        
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