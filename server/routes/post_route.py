@app.route('/posts', methods=['POST'])
def create_post():
    data = request.get_json()
    user_id = data.get('user_id')
    content = data.get('content')
    image = data.get('image')

    if not user_id or not content:
        return {"message": "Missing required fields"}, 400

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

@app.route('/posts/<int:id>', methods=['DELETE'])
def delete_post(id):
    post = db.session.get(Post, id)
    if not post:
        return {"message": "Post not found"}, 404

    db.session.delete(post)
    db.session.commit()

    return {"message": "Post deleted successfully"}, 200