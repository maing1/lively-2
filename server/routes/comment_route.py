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
    
    @app.route('/comments/<int:comment_id>', methods=['DELETE'])
    @jwt_required()
    def delete_comment(comment_id):
        user_id = get_jwt_identity()
        comment = db.session.get(Comment, comment_id)

        if not comment:
            return {"message": "Comment not found"}, 404

        if comment.user_id != user_id:
            return {"message": "You do not have permission to delete this comment"}, 403

        db.session.delete(comment)
        db.session.commit()

        return {"message": "Comment deleted successfully"}, 200