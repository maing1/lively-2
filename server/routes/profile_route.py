from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import User, db

def init_profile_route(app):
    @app.route('/profile', methods=['GET'])
    @jwt_required()
    def get_profile():
        user_id = get_jwt_identity()
        user = db.session.get(User, user_id)
        if not user:
            return {"error": "User not found"}, 404

        return jsonify({
                "username": user.username,
                "email": user.email,
                "bio": user.bio,
                "profile_picture": user.profile_picture
            }), 200

    @app.route('/profile', methods=['PUT'])
    @jwt_required()
    def update_profile():
        user_id = get_jwt_identity()
        user = db.session.get(User, user_id)
        if not user:
            return {"error": "User not found"}, 404
        
        data = request.get_json()
        if "bio" in data:
            user.bio = data["bio"]
        if "profile_picture" in data:
            user.profile_picture = data["profile_picture"]
            
        db.session.commit()
        return {"message": "Profile updated successfully"}, 200