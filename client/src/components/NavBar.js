// src/components/NavBar.js
// import  Link  from 'react-router-dom';
import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';

const NavBar = () => {
    return (
        <>
          <Navbar bg="dark" data-bs-theme="dark">
            <Container>
              <Navbar.Brand href="#home">NavBar</Navbar.Brand>
              <Nav className="me-auto">
                <Nav.Link to="/signup">Sign Up</Nav.Link>
                <Nav.Link to="/login">Login</Nav.Link>
                <Nav.Link to="/feed">Feed</Nav.Link>
                <Nav.Link to="/profile">Profile</Nav.Link>
              </Nav>
            </Container>
          </Navbar>
        </>
  );
};

export default NavBar;



