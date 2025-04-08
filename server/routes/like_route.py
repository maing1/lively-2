@app.route('/posts/<int:post_id>/likes', methods=['POST', 'DELETE'])
def manage_likes(post_id):
    post = db.session.get(Post, post_id)
    if not post:
        return {"error": "Post not found"}, 404

    user_id = 1  # Replace with session or JWT identity in real app

    if request.method == 'POST':
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

    if request.method == 'DELETE':
        like = Like.query.filter_by(user_id=user_id, post_id=post_id).first()
        if not like:
            return {"error": "Like not found"}, 404

        db.session.delete(like)
        db.session.commit()

        return {
            "message": "Like removed successfully",
            "likes_count": len(post.likes)
        }, 200