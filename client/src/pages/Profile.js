// // src/pages/Profile.js
// import { useState, useEffect } from 'react';
// import { Formik, Field, Form } from 'formik';

// const Profile = () => {
//   const [profile, setProfile] = useState(null);

//   useEffect(() => {
//     const fetchProfile = async () => {
//       try {
//         const response = await fetch('http://localhost:5555/profile/username'); // Replace with actual username
//         const data = await response.json();
//         setProfile(data);
//       } catch (error) {
//         console.error('Error fetching profile:', error);
//       }
//     };

//     fetchProfile();
//   }, []);

//   const handleProfileUpdate = async (values) => {
//     try {
//       const response = await fetch('http://localhost:5555/profile/username/update', { // Replace with actual username
//         method: 'PUT',
//         headers: {
//           'Content-Type': 'application/json',
//         },
//         body: JSON.stringify(values),
//       });

//       if (!response.ok) {
//         throw new Error('Error updating profile');
//       }

//       alert('Profile updated successfully');
//     } catch (error) {
//       console.error('Profile update error:', error);
//     }
//   };

//   if (!profile) return <div>Loading...</div>;

//   return (
//     <div>
//       <h2>Profile</h2>
//       <Formik
//         initialValues={{
//           bio: profile.bio,
//           profile_picture: profile.profile_picture,
//         }}
//         onSubmit={handleProfileUpdate}
//       >
//         <Form>
//           <div>
//             <Field name="bio" as="textarea" placeholder="Bio" />
//           </div>
//           <div>
//             <Field name="profile_picture" type="text" placeholder="Profile Picture URL" />
//           </div>
//           <button type="submit">Update Profile</button>
//         </Form>
//       </Formik>
//     </div>
//   );
// };

// export default Profile;

import { useEffect, useState } from "react";
import "bootstrap/dist/css/bootstrap.min.css";

const Profile = ({ userId }) => {
  const [profile, setProfile] = useState({
    username: "",
    email: "",
    bio: "",
    profile_picture: "",
  });

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [editMode, setEditMode] = useState(false);
  const [newProfile, setNewProfile] = useState({ bio: "", profile_picture: "" });

  // Fetch user profile
  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const response = await fetch(`http://localhost:5555/profile/${userId}`);
        if (!response.ok) {
          throw new Error("Profile not found");
        }
        const data = await response.json();
        setProfile(data);
        setNewProfile({ bio: data.bio || "", profile_picture: data.profile_picture || "" });
      } catch (error) {
        setError(error.message);
      } finally {
        setLoading(false);
      }
    };
    fetchProfile();
  }, [userId]);

  // Handle input changes
  const handleChange = (e) => {
    setNewProfile({ ...newProfile, [e.target.name]: e.target.value });
  };

  // Update Profile
  const handleUpdate = async () => {
    try {
      const response = await fetch(`http://localhost:5555/profile/${userId}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(newProfile),
      });

      if (!response.ok) {
        throw new Error("Failed to update profile");
      }

      const updatedProfile = { ...profile, ...newProfile };
      setProfile(updatedProfile);
      setEditMode(false);
    } catch (error) {
      console.error("Error updating profile:", error);
    }
  };

  if (loading) return <p>Loading profile...</p>;
  if (error) return <p className="text-danger">{error}</p>;

  return (
    <div className="container mt-4">
      <div className="card shadow-lg">
        <div className="card-body text-center">
          <h2 className="card-title">Profile</h2>
          {profile.profile_picture ? (
            <img
              src={profile.profile_picture}
              alt="Profile"
              className="rounded-circle img-fluid mb-3"
              style={{ width: "150px", height: "150px", objectFit: "cover" }}
            />
          ) : (
            <div
              className="rounded-circle bg-secondary d-inline-block mb-3"
              style={{ width: "150px", height: "150px" }}
            ></div>
          )}
          <h4>@{profile.username}</h4>
          <p className="text-muted">{profile.email}</p>

          {!editMode ? (
            <>
              <p className="lead">{profile.bio || "No bio available"}</p>
              <button className="btn btn-primary" onClick={() => setEditMode(true)}>
                Edit Profile
              </button>
            </>
          ) : (
            <div className="mt-3">
              <input
                type="text"
                name="bio"
                className="form-control mb-2"
                placeholder="Update bio"
                value={newProfile.bio}
                onChange={handleChange}
              />
              <input
                type="text"
                name="profile_picture"
                className="form-control mb-2"
                placeholder="Profile picture URL"
                value={newProfile.profile_picture}
                onChange={handleChange}
              />
              <button className="btn btn-success me-2" onClick={handleUpdate}>
                Save
              </button>
              <button className="btn btn-secondary" onClick={() => setEditMode(false)}>
                Cancel
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Profile;
