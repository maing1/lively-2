import React, { useEffect } from 'react';
import { useHistory } from 'react-router-dom';

const Logout = () => {
    const history = useHistory();

    useEffect(() => {
        // Clear the authentication token
        localStorage.removeItem('token');
        
        // Redirect to login page
        history.push('/login');
    }, [history]);

    return null; // This component doesn't render anything
};

export default Logout; 