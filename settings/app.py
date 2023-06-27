from flask import Flask
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from werkzeug.security import check_password_hash

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'your-secret-key'
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['JWT_TOKEN_LOCATION'] = ['headers', 'query_string']
jwt = JWTManager(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@db:5432/db_name'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    wallet = db.relationship('Wallet', backref='user', uselist=False)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def verify_password(self, password):
        return check_password_hash(self.password, password)


class Wallet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    address = db.Column(db.String(100), unique=True, nullable=False)
    private_key = db.Column(db.String(), default=0.0)
    transactions = db.relationship('Transaction', backref='wallet', lazy=True)

    def insert(self):
        db.session.add(self)
        db.session.commit()


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    wallet_id = db.Column(db.Integer, db.ForeignKey('wallet.id'), nullable=False)
    hash = db.Column(db.String(100), unique=True, nullable=False)
    currency = db.Column(db.String(20), nullable=False)
    amount = db.Column(db.Float, nullable=False)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def get_all(self, short=False):
        if short:
            return {
                "currency": self.currency,
                "amount": self.amount,
                "hash": self.hash
            }

        return {
            "id": self.id,
            "wallet_id": self.wallet_id,
            "currency": self.currency,
            "amount": self.amount,
            "hash": self.hash
        }

    @classmethod
    def get_transactions(cls, currency=None, amount=None, tx_hash=None, page=1, per_page=10):
        query = cls.query

        if currency:
            query = query.filter_by(currency=currency)
        if amount:
            query = query.filter_by(amount=amount)
        if tx_hash:
            query = query.filter_by(hash=tx_hash)

        query = query.order_by(cls.amount.desc())

        transactions = query.paginate(per_page=per_page, page=page, error_out=False).items

        return [transaction.get_all() for transaction in transactions]


from server.register import UserRegistrationResource, LoginResource
from server.eth import TransactionResource, GenerateWalletResource, TransactionFilterResource

api = Api(app)
api.add_resource(UserRegistrationResource, '/register')
api.add_resource(GenerateWalletResource, '/generate_wallets')
api.add_resource(TransactionResource, '/transaction')
api.add_resource(LoginResource, '/login')
api.add_resource(TransactionFilterResource, '/transactions/get')

with app.app_context():
    db.create_all()
