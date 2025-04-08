from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import User, Post, Comment, db

def init_comment_route(app, db):
    @app.route('/posts/<int:post_id>/comments', methods=['POST'])
    def comment(post_id):
        data = request.get_json()
        user_id = data.get('user_id')
        content = data.get('content')

        if not user_id or not content:
            return {"message": "Missing required fields"}, 400

        post = db.session.get(Post, post_id)
        user = db.session.get(User, user_id)

        if not post or not user:
            return {"message": "Post or User not found"}, 404

        new_comment = Comment(post_id=post_id, user_id=user_id, content=content)
        db.session.add(new_comment)
        db.session.commit()

        return {"message": "Comment added successfully"}, 201