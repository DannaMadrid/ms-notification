from flask import Blueprint, request, jsonify
from Services.emailService import send_email
from Services.templateService import load_html_template

contract_blueprint = Blueprint('contract', __name__)

@contract_blueprint.route('', methods=['POST'])
def new_contract():
    data = request.json
    recipient = data.get('recipient')
    description = data.get('description')
    date = data.get('date')
    customer = data.get('customer')

    template = load_html_template('NuevoContrato.html')
    if not template:
        return jsonify({'error': 'Template not found'}), 404

    body_html = template.render(description=description, date=date, customer=customer)
    subject = "Nuevo contrato"
    if body_html:
        body_html = body_html.replace('{{ description }}', description)  # Reemplaza el marcador
        body_html = body_html.replace('{{ date }}', date)  # Reemplaza el marcador
        body_html = body_html.replace('{{ customer }}', customer)  # Reemplaza el marcador
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