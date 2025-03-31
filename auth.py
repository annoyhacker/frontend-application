from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from models import User, db
from flask_jwt_extended import create_access_token

auth = Blueprint('auth', __name__)

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        try:
            if request.is_json:
                data = request.get_json()
            else:
                data = request.form
            
            name = data.get('name')
            email = data.get('email')
            password = data.get('password')

            if not all([name, email, password]):
                raise ValueError('All fields are required')

            if User.query.filter_by(email=email).first():
                raise ValueError('Email already exists')

            user = User(name=name, email=email)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()

            if request.is_json:
                return jsonify(message='Signup successful'), 201
            return redirect(url_for('auth.login'))
        
        except Exception as e:
            if request.is_json:
                return jsonify(error=str(e)), 400
            return render_template('signup.html', error=str(e)), 400
    
    return render_template('signup.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            if request.is_json:
                data = request.get_json()
            else:
                data = request.form

            email = data.get('email')
            password = data.get('password')

            user = User.query.filter_by(email=email).first()
            if not user or not user.check_password(password):
                raise ValueError('Invalid credentials')

            access_token = create_access_token(identity=user.email)
            
            if request.is_json:
                return jsonify(access_token=access_token)
            
            response = redirect(url_for('home'))
            response.set_cookie('access_token', access_token)
            return response

        except Exception as e:
            if request.is_json:
                return jsonify(error=str(e)), 401
            return render_template('login.html', error=str(e)), 401
    
    return render_template('login.html')

@auth.route('/logout')
def logout():
    response = redirect(url_for('auth.login'))
    response.delete_cookie('access_token')
    return response