
from flask import jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import User, db

def init_auth_route(app, bcrypt):
    @app.route('/signup', methods=['POST'])
    def signup():
        data = request.get_json()
        password = data['password']
        username = data['username']
        email = data['email']

        if not username or not email or not password:
            return jsonify({'error': 'Username, email, and password are required.'}), 400

        if User.query.filter_by(email=email).first():
            return jsonify({'error': 'Email already exists!'}), 400

        if User.query.filter_by(username=username).first():
            return jsonify({'error': 'Username already taken!'}), 400

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(password=hashed_password, username=username, email=email)

        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'User created successfully!'}), 201

    @app.route('/login', methods=['POST'])
    def login():
        data = request.get_json()

        email = data['email']
        password = data['password']

        if 'email' not in data or 'password' not in data:
            return jsonify({'message': 'Missing email or password!'}), 400

        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, password):
            access_token = create_access_token(identity=user.id)
            return jsonify({'message': 'Login Success!', 'access_token': access_token})

        return jsonify({'message': 'Login Failed!'}), 401
    
    @app.route('/get_user_name', methods=['GET'])
    @jwt_required()
    def get_user_name():
        user_id = get_jwt_identity()
        user = User.query.filter_by(id=user_id).first()

        if user:
            return jsonify({
                'message': 'User found',
                'username': user.username,
                'email': user.email,
                'bio': user.bio,
                'profile_picture': user.profile_picture
            })
        else:
            return jsonify({'message': 'User not found'}), 404


