// import React, { useEffect, useState } from "react";
// import { Switch, Route } from "react-router-dom";

// function App() {
//   return <h1>Project Client</h1>;
// }

// export default App;

// src/App.js
// src/App.js

import React from "react";
import { BrowserRouter as Router, Switch, Route, Redirect } from "react-router-dom";
import NavBar from "./components/NavBar";
import Signup from "./pages/Signup";
import Login from "./pages/Login";
import Logout from "./pages/Logout";
import Feed from "./pages/Feed";
import Profile from "./pages/Profile";

const App = () => {
  // For demo purposes, we'll use a hardcoded userId
  const userId = 1;

  return (
    <Router>
      <div className="app">
        <NavBar />
        <div className="main-content">
          <Switch>
            <Route exact path="/" render={() => <Redirect to="/feed" />} />
            <Route path="/signup" component={Signup} />
            <Route path="/login" component={Login} />
            <Route path="/logout" component={Logout} />
            <Route path="/feed" component={Feed} />
            <Route path="/profile" render={(props) => <Profile {...props} userId={userId} />} />
            <Route path="*" render={() => <Redirect to="/feed" />} />
          </Switch>
        </div>
      </div>
    </Router>
  );
};

export default App;