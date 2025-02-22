#!/usr/bin/env python3

# Standard library imports

# Remote library imports
from flask import request,make_response, jsonify, session
from flask_restful import Resource

# Local imports
from config import app, db, api
# Add your model imports
from models import db, User, Post, Like, Comment

# Views go here!

class Signup(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        
        # validations
        if not username or not email or not password:
            return {"message": "Missing required fields"}, 400
        
        
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return {"message": "User already exists"}, 400
        
        new_user = User(username=username, email=email)
        new_user.password_hash = password  # Set password hash here
        db.session.add(new_user)
        db.session.commit()
        
        return {"message": "User created successfully"}, 201
    
api.add_resource(Signup, '/users')
    
class Login(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        # Validate input
        if not email or not password:
            return {"message": "Missing required fields"}, 400
        
        user = User.query.filter_by(email=email).first()
        if not user or not user.authenticate(password):
            return {"message": "Invalid Password"}, 401
        
        return {"message": "Login successful"}, 200
api.add_resource(Login, '/login')

# class Profile(Resource):
#     def get(self, username):
#         # Fetch user by username
#         user = User.query.filter_by(username=username).first()
#         if not user:
#             return {"message": "User not found"}, 404
        
#         # Return user's profile data
#         profile = {
#             "username": user.username,
#             "bio": user.bio,
#             "profile_picture": user.profile_picture
#         }
        
#         return jsonify(profile)
    
#     def put(self, username):
#         data = request.get_json()
#         user = User.query.filter_by(username=username).first()
        
#         if not user:
#             return {"message": "User not found"}, 404
        
#         # Update bio and profile picture if provided
#         if 'bio' in data:
#             user.bio = data['bio']
#         if 'profile_picture' in data:
#             user.profile_picture = data['profile_picture']
        
#         db.session.commit()
        
#         return {"message": "Profile updated successfully", "username": user.username}, 200
    
# api.add_resource(Profile, '/profile/<string:username>')

class Profile(Resource):
    def get(self, user_id):
        """Retrieve user profile."""
        user = User.query.get(user_id)
        if not user:
            return {"error": "User not found"}, 404

        return {
            "username": user.username,
            "email": user.email,
            "bio": user.bio,
            "profile_picture": user.profile_picture
        }, 200

    def put(self, user_id):
        """Update user profile."""
        user = User.query.get(user_id)
        if not user:
            return {"error": "User not found"}, 404

        data = request.get_json()
        if "bio" in data:
            user.bio = data["bio"]
        if "profile_picture" in data:
            user.profile_picture = data["profile_picture"]

        db.session.commit()
        return {"message": "Profile updated successfully"}, 200
    
api.add_resource(Profile, "/profile/<int:user_id>")

class Posts(Resource):
    def post(self):
        data = request.get_json()
        user_id = data.get('user_id')  # Change to user_id
        content = data.get('content')
        image = data.get('image')
        
        # Basic validation
        if not user_id or not content:
            return {"message": "Missing required fields"}, 400
        
        # Fetch the user by user_id
        user = User.query.get(user_id)
        if not user:
            return {"message": "User not found"}, 404
        
        # Create the post
        new_post = Post(user_id=user.id, content=content, image=image)  # Changed Posts to Post
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
    
    def delete(self, id):
        post = Post.query.get(id)
        if not post:
            return {"message": "Post not found"}, 404
        
        db.session.delete(post)
        db.session.commit()
        
        return {"message": "Post deleted successfully"}, 200
    
api.add_resource(Posts, '/posts', '/posts/<int:id>')

class Feed(Resource):
    def get(self):
        posts = Post.query.all()
        posts_list = [
            {
                "id": post.id,
                "user_id": post.user_id,
                "username": post.user.username,  # Access username through the relationship
                "content": post.content,
                "image": post.image,
                "likes_count": len(post.likes),
                "comments_count": len(post.comments)
            } 
            for post in posts
        ]
        
        return jsonify(posts_list)

api.add_resource(Feed, '/feed')

class Likes(Resource):
    def post(self, post_id):
        """Add a like to a post"""
        post = Post.query.get(post_id)
        if not post:
            return {"error": "Post not found"}, 404

        # For now, we'll use a hardcoded user_id since we removed authentication
        user_id = 1  # This matches our hardcoded user in the frontend
        
        # Check if user already liked the post
        existing_like = Like.query.filter_by(user_id=user_id, post_id=post_id).first()
        if existing_like:
            return {"error": "Already liked"}, 400

        new_like = Like(user_id=user_id, post_id=post_id)
        db.session.add(new_like)
        db.session.commit()

        return {
            "message": "Post liked successfully",
            "likes_count": len(post.likes)
        }, 201

    def delete(self, post_id):
        """Remove a like from a post"""
        post = Post.query.get(post_id)
        if not post:
            return {"error": "Post not found"}, 404

        # For now, we'll use a hardcoded user_id since we removed authentication
        user_id = 1

        like = Like.query.filter_by(user_id=user_id, post_id=post_id).first()
        if not like:
            return {"error": "Like not found"}, 404

        db.session.delete(like)
        db.session.commit()

        return {
            "message": "Like removed successfully",
            "likes_count": len(post.likes)
        }, 200

api.add_resource(Likes, '/posts/<int:post_id>/likes')

class Comments(Resource):
    def post(self, post_id):
        data = request.get_json()
        user_id = data.get('user_id')
        content = data.get('content')
        
        # Basic validation
        if not user_id or not content:
            return {"message": "Missing required fields"}, 400
        
        post = Post.query.get(post_id)
        user = User.query.get(user_id)

        if not post or not user:
            return {"message": "Post or User not found"}, 404
        
        new_comment = Comment(post_id=post_id, user_id=user_id, content=content)
        db.session.add(new_comment)
        db.session.commit()
        
        return {"message": "Comment added successfully"}, 201
    
api.add_resource(Comments, '/posts/<int:post_id>/comments')

if __name__ == '__main__':
    app.run(port=5555, debug=True)

