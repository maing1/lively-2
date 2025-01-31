import React from "react";

const Comment = ({ comment }) => {
  return (
    <div className="comment">
      <strong>{comment.username}:</strong> {comment.content}
    </div>
  );
};

export default Comment;
