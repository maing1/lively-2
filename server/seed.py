#!/usr/bin/env python3

# Standard library imports
from random import randint, choice as rc

# Remote library imports
from faker import Faker

# # Local imports
# from app import app
# from models import db, User, Post, Like, Comment,Follower

# if __name__ == '__main__':
#     fake = Faker()
#     with app.app_context():
#         print("Starting seed...")
#         # Seed code goes here!

from app import app, db  # Import the app and db from your main app file
from models import User, Post, Like, Comment # Import your models

# Create the seed data
def seed_data():
    with app.app_context():
        # Drop existing tables and recreate them
        print("Dropping existing tables...")
        db.drop_all()
        print("Creating tables...")
        db.create_all()

        # Seed Users
        print("Seeding users...")
        user1 = User(username="user1", email="user1@example.com")
        user1._password_hash = "password123" 

        user2 = User(username="user2", email="user2@example.com")
        user2._password_hash = "password123"

        user3 = User(username="user3", email="user3@example.com")
        user3._password_hash = "password123"

        db.session.add_all([user1, user2, user3])
        db.session.commit()
        print("Users added to the session.")

        # Seed Posts
        print("Seeding posts...")
        post1 = Post(content="First rose of the season!", user_id=user1.id, image = "https://i.pinimg.com/originals/14/86/86/148686b4a830e06d8089db5cb1e521f4.jpg" )
        post2 = Post(content="My fur baby!", user_id=user2.id, image = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSimtZyskdR3y0AtCiHyEebU1o7mZQFOA6F0Q&s")
        post3 = Post(content="OOTD!", user_id=user3.id, image = "https://i.pinimg.com/736x/09/56/cd/0956cde2f34c21cca779f52f4ce5c786.jpg")

        db.session.add_all([post1, post2, post3])
        db.session.commit()
        print("Posts added to the session.")

        # Seed Likes
        print("Seeding likes...")
        like1 = Like(user_id=user1.id, post_id=post2.id)  # User1 likes User2's post
        like2 = Like(user_id=user2.id, post_id=post3.id)  # User2 likes User3's post
        like3 = Like(user_id=user3.id, post_id=post1.id)  # User3 likes User1's post

        db.session.add_all([like1, like2, like3])
        db.session.commit()
        print("Likes added to the session.")

        # Seed Comments
        print("Seeding comments...")
        comment1 = Comment(content="Nice post!", user_id=user1.id, post_id=post2.id)
        comment2 = Comment(content="Awesome!", user_id=user2.id, post_id=post3.id)
        comment3 = Comment(content="Great thoughts!", user_id=user3.id, post_id=post1.id)

        db.session.add_all([comment1, comment2, comment3])
        db.session.commit()
        print("Comments added to the session.")


# Run the seed function
if __name__ == "__main__":
    print("Starting the seeding process...")
    seed_data()
    print("Seeding process complete!")

        
