#!/usr/bin/env python3

from flask import request, session, jsonify, make_response
from flask_restful import Resource

from config import app, db, api
from models import User

class ClearSession(Resource):

    def delete(self):
    
        session['page_views'] = None
        session['user_id'] = None

        return {}, 204

class Signup(Resource):
    
    def post(self):
        json = request.get_json()
        user = User(
            username=json['username']
        )
        user.password_hash = json['password']
        db.session.add(user)
        db.session.commit()
        return user.to_dict(), 201

class CheckSession(Resource):
    
    def get(self):
        user_id = session.get('user_id')
        if not user_id:
            return '', 204
        
        user = User.query.get(user_id)
        if user:
            return {'username': user.username}, 200
        return '', 204

class Login(Resource):
    
    def post(self):
        data = request.get_json()
        username = data['username']
        password = data['password']
        
        user = User.query.filter_by(username=username).first()
        if user and user.authenticate(password):
            session['user_id'] = user.id
            return {'username': user.username}, 200
        return {'error': 'Invalid credentials'}, 401



class Logout(Resource):
    
    def delete(self):
        session.clear()
        return '', 204
    
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(CheckSession, '/check_session')
api.add_resource(ClearSession, '/clear', endpoint='clear')
api.add_resource(Signup, '/signup', endpoint='signup')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
