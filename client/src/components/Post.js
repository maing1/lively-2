import React, { useState } from "react";
import Comment from "./Comment";
import 'bootstrap/dist/css/bootstrap.min.css';

const Post = ({ post, onLike, onComment }) => {
  const { id, username, content, image, likes_count = 0, comments = [] } = post || {};
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

  if (!post) return null;

  return (
    <div className="post">
      <div className="d-flex align-items-center mb-3">
        <h5 className="mb-0">{username}</h5>
      </div>
      <p className="mb-3">{content}</p>
      {image && (
        <img 
          src={image} 
          alt="Post" 
          className="img-fluid rounded mb-3" 
          style={{ maxHeight: '400px', objectFit: 'cover' }}
        />
      )}
      <div className="post-actions mb-3">
        <button className="btn btn-outline-primary btn-sm" onClick={handleLike}>
          ❤️ {likes_count} Likes
        </button>
      </div>
      <div className="comments-section mb-3">
        {comments && comments.length > 0 ? (
          comments.map((comment) => (
            <Comment key={comment.id} comment={comment} />
          ))
        ) : (
          <p className="text-muted small"></p>
        )}
      </div>
      <form onSubmit={handleCommentSubmit} className="mt-3">
        <div className="input-group">
          <input
            type="text"
            className="form-control"
            placeholder="Write a comment..."
            value={commentText}
            onChange={(e) => setCommentText(e.target.value)}
          />
          <button type="submit" className="btn btn-primary">
            Comment
          </button>
        </div>
      </form>
    </div>
  );
};

export default Post;
