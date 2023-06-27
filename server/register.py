from flask import request
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_restful import Resource, reqparse
from werkzeug.exceptions import Unauthorized

from settings.app import User


class UserRegistrationResource(Resource):
    def post(self):
        data = request.get_json()

        email = data.get('email')
        password = data.get('password')

        user = User(email=email, password=password)
        user.insert()

        return {'message': 'User registered successfully.'}, 201


class LoginResource(Resource):
    def post(self):

        data = request.get_json()
        email = data.get('email')

        db_user: User = User.query.filter_by(email=email).first()
        if not db_user:
            raise Unauthorized

        access_token = create_access_token(identity=db_user.id)
        refresh_token = create_refresh_token(identity=db_user.id)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token
        }, "Logged in successfully"
