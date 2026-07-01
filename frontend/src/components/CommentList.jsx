import { formatDateTime } from "../utils/format";

// Renders the comment thread, oldest first (the order the API returns).
export default function CommentList({ comments }) {
  if (comments.length === 0) {
    return <p className="muted">No comments yet. Be the first to comment.</p>;
  }

  return (
    <ul className="comment-list">
      {comments.map((comment) => (
        <li key={comment.id} className="comment">
          <div className="comment-header">
            <strong>{comment.author.name}</strong>
            <span className="muted">{formatDateTime(comment.created_at)}</span>
          </div>
          <p className="comment-body">{comment.body}</p>
        </li>
      ))}
    </ul>
  );
}
