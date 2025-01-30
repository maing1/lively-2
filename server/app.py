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
    
api.add_resource(Signup, '/signup')
    
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

class Profile(Resource):
    def get(self, username):
        # Fetch user by username
        user = User.query.filter_by(username=username).first()
        if not user:
            return {"message": "User not found"}, 404
        
        # Return user's profile data
        profile = {
            "username": user.username,
            "bio": user.bio,
            "profile_picture": user.profile_picture
        }
        
        return jsonify(profile)
    
    def put(self, username):
        data = request.get_json()
        user = User.query.filter_by(username=username).first()
        
        if not user:
            return {"message": "User not found"}, 404
        
        # Update bio and profile picture if provided
        if 'bio' in data:
            user.bio = data['bio']
        if 'profile_picture' in data:
            user.profile_picture = data['profile_picture']
        
        db.session.commit()
        
        return {"message": "Profile updated successfully", "username": user.username}, 200
    
api.add_resource(Profile, '/profile/<string:username>')

class Posts(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')  # Change user_id to username
        content = data.get('content')
        image = data.get('image')
        
        # Basic validation
        if not username or not content:
            return {"message": "Missing required fields"}, 400
        
        # Fetch the user by username
        user = User.query.filter_by(username=username).first()
        if not user:
            return {"message": "User not found"}, 404
        
        # Create the post with the user_id
        new_post = Posts(user_id=user.id, content=content, image=image)
        db.session.add(new_post)
        db.session.commit()
        
        return {"message": "Post created successfully"}, 201
    
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
                "username": post.username,  # Access the username via the Post model
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
    def post(self):
        data = request.get_json()

        user_id = data.get('user_id')
        post_id = data.get('post_id')

        if not user_id or not post_id:
            return {"error": "Missing user_id or post_id"}, 400

        user = User.query.get(user_id)
        post = Post.query.get(post_id)

        if not user or not post:
            return {"error": "Invalid user_id or post_id"}, 400

        existing_like = Like.query.filter_by(user_id=user_id, post_id=post_id).first()
        if existing_like:
            return {"error": "User already liked this post"}, 400

        new_like = Like(user_id=user_id, post_id=post_id)
        db.session.add(new_like)
        db.session.commit()

        return {"message": "Post liked successfully!"}, 201

    def delete(self):
        data = request.get_json()
        user_id = data.get('user_id')
        post_id = data.get('post_id')

        like = Like.query.filter_by(user_id=user_id, post_id=post_id).first()
        if like:
            db.session.delete(like)
            db.session.commit()
            return {"message": "Post unliked successfully!"}, 200
        return {"error": "Like not found"}, 404

api.add_resource(Likes, '/likes')

class CommentOnPost(Resource):
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
    
api.add_resource(CommentOnPost, '/post/<int:post_id>/comment')

if __name__ == '__main__':
    app.run(port=5555, debug=True)

