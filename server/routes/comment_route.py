from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import User, Post, Comment, db

def init_comment_route(app):
    @app.route('/comments', methods=['POST'])
    @jwt_required()
    def comment():
        data = request.get_json()
        user_id = get_jwt_identity()

        post_id = data.get('post_id')
        content = data.get('content')

        required_fields = ['post_id','content']
        for field in required_fields:
            if field not in data:
                return jsonify({'message': f'Missing required field: {field}'}), 400

        post = db.session.get(Post, post_id)
        user = db.session.get(User, user_id)

        if not post or not user:
            return {"message": "Post or User not found"}, 404

        new_comment = Comment(post_id=post_id, user_id=user_id, content=content)
        db.session.add(new_comment)
        db.session.commit()

        return {"message": "Comment added successfully"}, 201