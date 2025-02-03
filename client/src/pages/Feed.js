// src/pages/Feed.js
import { useEffect, useState } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import Post from '../components/Post';

const Feed = () => {
  const [posts, setPosts] = useState([]);

  useEffect(() => {
    const fetchPosts = async () => {
      try {
        const response = await fetch('http://localhost:5555/feed');
        const data = await response.json();
        console.log('Fetched posts:', data);
        const postsWithComments = data.map(post => ({
          ...post,
          comments: post.comments || [],
          likes_count: post.likes_count || 0
        }));
        setPosts(postsWithComments);
      } catch (error) {
        console.error('Error fetching posts:', error);
      }
    };

    fetchPosts();
  }, []);

  const handleLike = async (postId) => {
    try {
      const response = await fetch(`http://localhost:5555/posts/${postId}/likes`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });
      if (response.ok) {
        // Update the posts state to reflect the new like count
        setPosts(posts.map(post => 
          post.id === postId 
            ? { ...post, likes_count: post.likes_count + 1 }
            : post
        ));
      }
    } catch (error) {
      console.error('Error liking post:', error);
    }
  };

  const handleComment = async (postId, commentText) => {
    try {
      const response = await fetch(`http://localhost:5555/posts/${postId}/comments`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify({ content: commentText })
      });
      if (response.ok) {
        const newComment = await response.json();
        // Update the posts state to include the new comment
        setPosts(posts.map(post =>
          post.id === postId
            ? { ...post, comments: [...post.comments, newComment] }
            : post
        ));
      }
    } catch (error) {
      console.error('Error adding comment:', error);
    }
  };

  return (
    <div className="container mt-5">
      <h2 className="mb-4">Feed</h2>
      {posts.length === 0 ? (
        <div className="card">
          <div className="card-body text-center text-muted">
            <p className="mb-0">No posts yet.</p>
          </div>
        </div>
      ) : (
        <div className="row justify-content-center">
          <div className="col-md-8">
            <div className="row">
              {posts.map((post) => (
                <div key={post.id} className="col-md-6 mb-4">
                  <div className="card h-100">
                    <div className="card-body">
                      <Post 
                        post={post} 
                        onLike={handleLike} 
                        onComment={handleComment}
                      />
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Feed;
