from flask import Flask
from controllers.welcomController import welcome_blueprint
from controllers.paymentController import payment_blueprint
from controllers.secondFAController import secondFA_blueprint
from controllers.PasswordController import ResetPassword_blueprint
from controllers.PruebaController import pruebaConexion_blueprint
from controllers.ContractController import contract_blueprint
from controllers.orderController import order_blueprint
from controllers.tranchesController import tranch_blueprint

app = Flask(__name__)

# Registrar los blueprints
app.register_blueprint(welcome_blueprint, url_prefix='/welcome')
app.register_blueprint(payment_blueprint, url_prefix='/paymentNotification')
app.register_blueprint(secondFA_blueprint, url_prefix='/2FA')
app.register_blueprint(ResetPassword_blueprint, url_prefix='/resetPassword')
app.register_blueprint(pruebaConexion_blueprint, url_prefix='/PruebaConexion')
app.register_blueprint(contract_blueprint, url_prefix='/contract')
app.register_blueprint(order_blueprint, url_prefix='/order')
app.register_blueprint(tranch_blueprint, url_prefix='/tranch')

if __name__ == "__main__":
    app.run(debug=True)
