// import React, { useEffect, useState } from "react";
// import { Switch, Route } from "react-router-dom";

// function App() {
//   return <h1>Project Client</h1>;
// }

// export default App;

// src/App.js
// src/App.js

import React from "react";
import { BrowserRouter as Router, Switch, Route } from "react-router-dom"; // Using v5 syntax
import NavBar from "./components/NavBar";
import Signup from "./pages/Signup";
import Login from "./pages/Login";
import Feed from "./pages/Feed";
import Profile from "./pages/Profile";

const App = () => {
  return (
    <Router>
      <NavBar />
      <Switch>
        <Route path="/signup" component={Signup} />
        <Route path="/login" component={Login} />
        <Route path="/feed" component={Feed} />
        <Route path="/profile" component={Profile} />
      </Switch>
    </Router>
  );
};

export default App;