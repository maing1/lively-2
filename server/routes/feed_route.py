@app.route('/feed', methods=['GET'])
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
    return jsonify(posts_list)