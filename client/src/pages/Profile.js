// src/pages/Profile.js
import { useState, useEffect } from 'react';
import { Formik, Field, Form } from 'formik';

const Profile = () => {
  const [profile, setProfile] = useState(null);

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const response = await fetch('http://localhost:5555/profile/username'); // Replace with actual username
        const data = await response.json();
        setProfile(data);
      } catch (error) {
        console.error('Error fetching profile:', error);
      }
    };

    fetchProfile();
  }, []);

  const handleProfileUpdate = async (values) => {
    try {
      const response = await fetch('http://localhost:5555/profile/username/update', { // Replace with actual username
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(values),
      });

      if (!response.ok) {
        throw new Error('Error updating profile');
      }

      alert('Profile updated successfully');
    } catch (error) {
      console.error('Profile update error:', error);
    }
  };

  if (!profile) return <div>Loading...</div>;

  return (
    <div>
      <h2>Profile</h2>
      <Formik
        initialValues={{
          bio: profile.bio,
          profile_picture: profile.profile_picture,
        }}
        onSubmit={handleProfileUpdate}
      >
        <Form>
          <div>
            <Field name="bio" as="textarea" placeholder="Bio" />
          </div>
          <div>
            <Field name="profile_picture" type="text" placeholder="Profile Picture URL" />
          </div>
          <button type="submit">Update Profile</button>
        </Form>
      </Formik>
    </div>
  );
};

export default Profile;
