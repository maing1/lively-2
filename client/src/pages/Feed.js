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
          'Content-Type': 'application/json'
        }
      });
      
      if (response.ok) {
        const data = await response.json();
        // Update the posts state with the new likes count from the server
        setPosts(posts.map(post => 
          post.id === postId 
            ? { ...post, likes_count: data.likes_count }
            : post
        ));
      } else {
        const error = await response.json();
        console.error('Error liking post:', error);
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
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ 
          user_id: 1,  // Using the same hardcoded user_id as in the rest of the app
          content: commentText 
        })
      });
      if (response.ok) {
        // Refresh the posts to show the new comment
        const feedResponse = await fetch('http://localhost:5555/feed');
        const updatedPosts = await feedResponse.json();
        setPosts(updatedPosts);
      }
    } catch (error) {
      console.error('Error adding comment:', error);
    }
  };

  return (
    <div className="container mt-5">
      <h2 className="text-center">Feed</h2>
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
