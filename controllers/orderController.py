from flask import Blueprint, request, jsonify
from Services.emailService import send_email
from Services.templateService import load_html_template

order_blueprint = Blueprint('order', __name__)

@order_blueprint.route('', methods=['POST'])
def new_order():
    data = request.json
    recipient = data.get('recipient')
    rutaid = data.get('rutaid')
    contractid = data.get('contractid')
    date_order = data.get('date_order')
    type = data.get('type')
    address = data.get('address')
    municipality = data.get('municipality')
    departament = data.get('departament')

    template = load_html_template('OrderController.html')
    if not template:
        return jsonify({'error': 'Template not found'}), 404

    body_html = template.render(rutaid=rutaid, contractid=contractid, date_order=date_order, type=type, address=address, municipality=municipality, departament=departament)
    subject = "Seguimiento ruta"
    if body_html:
        body_html = body_html.replace('{{ rutaid }}', str(rutaid))  # Reemplaza el marcador, solo recibe cadenas asi que debe converir los numeros en cadenas
        body_html = body_html.replace('{{ contractid }}', str(contractid))  # Reemplaza el marcador
        body_html = body_html.replace('{{ date_order }}', date_order)  # Reemplaza el marcador
        body_html = body_html.replace('{{ type }}', type)  # Reemplaza el marcador
        body_html = body_html.replace('{{ address }}', str(address))  # Reemplaza el marcador
        body_html = body_html.replace('{{ municipality }}', municipality)  # Reemplaza el marcador
        body_html = body_html.replace('{{ departament }}', departament)  # Reemplaza el marcador

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