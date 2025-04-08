from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import User, Post, db

def init_feed_route(app):
    @app.route('/feed', methods=['GET'])
    @jwt_required()
    def feed():
        posts = Post.query.all()
        posts_list = [
            {
                "id": post.id,
                "user_id": post.user_id,
                "username": post.user.username,
                "content": post.content,
                "image": post.image,
                "likes_count": len(post.likes),
                "comments_count": len(post.comments)
            } for post in posts
        ]
        return jsonify({
            'message': 'Posts retrieved successfully',
            'couriers': posts_list
        }), 200