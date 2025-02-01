// src/pages/Signup.js
import React, { useEffect, useState } from "react";
import { useFormik } from "formik";
import * as yup from "yup";
import { useHistory } from "react-router-dom";  
import 'bootstrap/dist/css/bootstrap.min.css';

const Signup = () => {
  const history = useHistory();  
  const [error, setError] = useState(""); 

  
  useEffect(() => {
    
  }, []);

  const formik = useFormik({
    initialValues: {
      username: "",
      email: "",
      password: "",
    },
    validationSchema: yup.object({
      username: yup
        .string()
        .required("Username is required")
        .min(3, "Username must be at least 3 characters"),
      email: yup
        .string()
        .email("Invalid email address")
        .required("Email is required"),
      password: yup
        .string()
        .required("Password is required")
        .min(6, "Password must be at least 6 characters"),
    }),
    onSubmit: async (values) => {
      try {
        const response = await fetch("http://localhost:5555/users", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(values),
        });

        if (!response.ok) {
          throw new Error("Error signing up");
        }

        const data = await response.json();
        alert(data.message);
        history.push("/login"); 
      } catch (error) {
        setError("Signup failed. Please try again."); 
      }
    },
  });

  return (
    <div className="container mt-5">
      <h2>Sign Up</h2>
      {error && <p className="text-danger">{error}</p>}
      <form onSubmit={formik.handleSubmit}>
        <div className="mb-3">
          <input
            type="text"
            name="username"
            className="form-control"
            placeholder="Username"
            value={formik.values.username}
            onChange={formik.handleChange}
            onBlur={formik.handleBlur}
          />
          {formik.touched.username && formik.errors.username && (
            <div className="text-danger">{formik.errors.username}</div>
          )}
        </div>
        <div className="mb-3">
          <input
            type="email"
            name="email"
            className="form-control"
            placeholder="Email"
            value={formik.values.email}
            onChange={formik.handleChange}
            onBlur={formik.handleBlur}
          />
          {formik.touched.email && formik.errors.email && (
            <div className="text-danger">{formik.errors.email}</div>
          )}
        </div>
        <div className="mb-3">
          <input
            type="password"
            name="password"
            className="form-control"
            placeholder="Password"
            value={formik.values.password}
            onChange={formik.handleChange}
            onBlur={formik.handleBlur}
          />
          {formik.touched.password && formik.errors.password && (
            <div className="text-danger">{formik.errors.password}</div>
          )}
        </div>
        <button type="submit" className="btn btn-primary w-100">Sign Up</button>
      </form>
    </div>
  );
};

export default Signup;
