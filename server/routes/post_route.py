from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import User, Post, db

def init_post_route(app):
    @app.route('/posts', methods=['POST'])
    @jwt_required()
    def create_post():
        data = request.get_json()
        user_id = get_jwt_identity()

        content = data.get('content')
        image = data.get('image')

        required_fields = ['content', 'image']
        for field in required_fields:
            if field not in data:
                return jsonify({'message': f'Missing required field: {field}'}), 400

        user = db.session.get(User, user_id)
        if not user:
            return {"message": "User not found"}, 404

        new_post = Post(user_id=user.id, content=content, image=image)
        db.session.add(new_post)
        db.session.commit()

        return {
            "message": "Post created successfully",
            "post": {
                "id": new_post.id,
                "content": new_post.content,
                "image": new_post.image,
                "user_id": new_post.user_id
            }
        }, 201

    @app.route('/posts/<int:post_id>', methods=['DELETE'])
    @jwt_required()
    def delete_post(post_id):
        user_id = get_jwt_identity()
        post = db.session.get(Post, post_id)

        if not post:
            return {"message": "Post not found"}, 404
        
        if post.user_id != user_id:
            return {"message": "You do not have permission to delete this post"}, 403

        db.session.delete(post)
        db.session.commit()

        return {"message": "Post deleted successfully"}, 200