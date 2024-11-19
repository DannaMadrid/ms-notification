from flask import Blueprint, request, jsonify
from Services.emailService import send_email
from Services.templateService import load_html_template

payment_blueprint = Blueprint('payment', __name__)

@payment_blueprint.route('', methods=['POST'])
def send_payment_notification():
    data = request.json
    recipient = data.get('recipient')
    username = data.get('username')
    amount = data.get('amount')
    description = data.get('description')

    template = load_html_template('payment_notification.html')
    if not template:
        return jsonify({'error': 'Template not found'}), 404

    body_html = template.render(username=username, amount=amount, description=description)
    subject = "Confirmación de pago recibido"
    success = send_email(subject, recipient, body_html)

    if success:
        return jsonify({'message': 'Notification email sent successfully'})
    else:
        return jsonify({'error': 'Failed to send email'})
