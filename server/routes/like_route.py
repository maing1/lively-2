from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import User, Post, Like, db

def init_like_route(app):
    @app.route('/posts/<int:post_id>/likes', methods=['POST'])
    @jwt_required()
    def like_post(post_id):
        post = db.session.get(Post, post_id)
        if not post:
            return jsonify({"error": "Post not found"}), 404

        user_id = get_jwt_identity()

        existing_like = Like.query.filter_by(user_id=user_id, post_id=post_id).first()
        if existing_like:
            return jsonify({"error": "Already liked"}), 400

        new_like = Like(user_id=user_id, post_id=post_id)
        db.session.add(new_like)
        db.session.commit()

        return jsonify({
            "message": "Post liked successfully",
            "likes_count": len(post.likes)
        }), 201

    @app.route('/posts/<int:post_id>/likes', methods=['DELETE'])
    @jwt_required()
    def unlike_post(post_id):
        post = db.session.get(Post, post_id)
        if not post:
            return jsonify({"error": "Post not found"}), 404

        user_id = get_jwt_identity()

        like = Like.query.filter_by(user_id=user_id, post_id=post_id).first()
        if not like:
            return jsonify({"error": "Like not found"}), 404

        db.session.delete(like)
        db.session.commit()

        return jsonify({
            "message": "Like removed successfully",
            "likes_count": len(post.likes)
        }), 200