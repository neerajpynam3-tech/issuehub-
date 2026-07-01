import { useState } from "react";

// Text area + submit button for adding a comment. Clears itself on success.
export default function CommentComposer({ onSubmit }) {
  const [body, setBody] = useState("");
  const [submitting, setSubmitting] = useState(false);

  async function handleSubmit(event) {
    event.preventDefault();
    if (!body.trim()) return;
    setSubmitting(true);
    try {
      await onSubmit(body.trim());
      setBody("");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <form className="comment-composer" onSubmit={handleSubmit}>
      <textarea
        rows={3}
        placeholder="Write a comment..."
        value={body}
        onChange={(e) => setBody(e.target.value)}
      />
      <button type="submit" className="btn btn-primary" disabled={submitting}>
        {submitting ? "Posting..." : "Add Comment"}
      </button>
    </form>
  );
}
