from app import app
from models import db, User, Post, Comment, Like
from werkzeug.security import generate_password_hash
from faker import Faker
import random

fake = Faker()

def seed_data():
    print("Dropping existing tables...")
    db.drop_all()
    print("Creating tables...")
    db.create_all()

    print("Seeding users...")
    users = []
    for _ in range(10):
        user = User(
            username=fake.user_name(),
            email=fake.unique.email(),
            password=generate_password_hash("password"),  # Default password for testing
            bio=fake.sentence(nb_words=10),
            profile_picture=fake.image_url()
        )
        users.append(user)
        db.session.add(user)

    db.session.commit()

    print("Seeding posts...")
    posts = []
    for _ in range(20):
        post = Post(
            user=random.choice(users),
            content=fake.text(max_nb_chars=200),
            image=fake.image_url()
        )
        posts.append(post)
        db.session.add(post)

    db.session.commit()

    print("Seeding comments...")
    for _ in range(30):
        comment = Comment(
            user_id=random.choice(users).id,
            post_id=random.choice(posts).id,
            content=fake.sentence()
        )
        db.session.add(comment)

    print("Seeding likes...")
    for _ in range(40):
        like = Like(
            user_id=random.choice(users).id,
            post_id=random.choice(posts).id
        )
        db.session.add(like)

    db.session.commit()
    print("Seeding complete!")

if __name__ == '__main__':
    with app.app_context():
        seed_data()
