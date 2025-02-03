// import React from "react";
// import 'bootstrap/dist/css/bootstrap.min.css';

// const Comment = ({ comment }) => {
//   return (
//     <div className="comment d-flex align-items-start mb-2">
//       <div className="rounded-circle bg-secondary text-white d-flex align-items-center justify-content-center me-2" 
//            style={{ width: '24px', height: '24px', fontSize: '12px' }}>
//         {comment.username ? comment.username.charAt(0).toUpperCase() : '?'}
//       </div>
//       <div className="comment-content bg-light rounded p-2" style={{ flex: 1 }}>
//         <div className="d-flex justify-content-between align-items-center mb-1">
//           <small className="fw-bold text-secondary">{comment.username}</small>
//         </div>
//         <p className="mb-0 small">{comment.content}</p>
//       </div>
//     </div>
//   );
// };

// export default Comment;

import { Formik, Form, Field, ErrorMessage } from "formik";
import * as Yup from "yup";

const Comment = ({ postId, userId, onCommentAdded }) => {
  const initialValues = {
    content: "",
  };

  const validationSchema = Yup.object({
    content: Yup.string()
      .trim()
      .min(3, "Comment must be at least 3 characters")
      .max(500, "Comment cannot exceed 500 characters")
      .required("Comment is required"),
  });

  const handleSubmit = async (values, { setSubmitting, resetForm, setStatus }) => {
    try {
      const response = await fetch(`http://localhost:5555/posts/${postId}/comments`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ user_id: userId, content: values.content }),
      });

      const data = await response.json();

      if (response.ok) {
        setStatus({ success: "Comment added successfully!" });
        resetForm(); // Clear the form
        onCommentAdded(); // Optional callback to refresh comments
      } else {
        setStatus({ error: data.message || "Failed to add comment." });
      }
    } catch (error) {
      setStatus({ error: "An error occurred. Please try again." });
    }

    setSubmitting(false);
  };

  return (
    <div className="p-4 border rounded-lg shadow-md bg-white">
      <h3 className="text-lg font-semibold mb-2">Add a Comment</h3>

      <Formik
        initialValues={initialValues}
        validationSchema={validationSchema}
        onSubmit={handleSubmit}
      >
        {({ isSubmitting, status }) => (
          <Form className="flex flex-col gap-2">
            {status?.error && <p className="text-red-500">{status.error}</p>}
            {status?.success && <p className="text-green-500">{status.success}</p>}

            <Field
              as="textarea"
              name="content"
              className="border rounded p-2 w-full"
              rows="3"
              placeholder="Write your comment..."
            />
            <ErrorMessage name="content" component="p" className="text-red-500 text-sm" />

            <button
              type="submit"
              className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
              disabled={isSubmitting}
            >
              {isSubmitting ? "Posting..." : "Post Comment"}
            </button>
          </Form>
        )}
      </Formik>
    </div>
  );
};

export default Comment;
