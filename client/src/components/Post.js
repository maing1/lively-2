import React, { useState } from "react";
import Comment from "./Comment";

const Post = ({ post, onLike, onComment }) => {
  const { id, username, content, image, likes_count, comments } = post;
  const [commentText, setCommentText] = useState("");

  const handleLike = () => {
    onLike(id);
  };

  const handleCommentSubmit = (e) => {
    e.preventDefault();
    if (commentText.trim()) {
      onComment(id, commentText);
      setCommentText("");
    }
  };

  return (
    <div className="post">
      <h4>{username}</h4>
      <p>{content}</p>
      {image && <img src={image} alt="Post" className="post-image" />}
      <div className="post-actions">
        <button onClick={handleLike}>❤️ {likes_count} Likes</button>
      </div>
      <div className="comments-section">
        {comments.map((comment) => (
          <Comment key={comment.id} comment={comment} />
        ))}
      </div>
      <form onSubmit={handleCommentSubmit}>
        <input
          type="text"
          placeholder="Write a comment..."
          value={commentText}
          onChange={(e) => setCommentText(e.target.value)}
        />
        <button type="submit">Comment</button>
      </form>
    </div>
  );
};

export default Post;
