@app.route('/profile/<int:user_id>', methods=['GET', 'PUT'])
def profile(user_id):
    user = db.session.get(User, user_id)
    if not user:
        return {"error": "User not found"}, 404

    if request.method == 'GET':
        return {
            "username": user.username,
            "email": user.email,
            "bio": user.bio,
            "profile_picture": user.profile_picture
        }, 200

    if request.method == 'PUT':
        data = request.get_json()
        if "bio" in data:
            user.bio = data["bio"]
        if "profile_picture" in data:
            user.profile_picture = data["profile_picture"]
        db.session.commit()
        return {"message": "Profile updated successfully"}, 200