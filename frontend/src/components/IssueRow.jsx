import { useNavigate } from "react-router-dom";

import Badge from "./Badge";
import {
  PRIORITY_COLORS,
  PRIORITY_LABELS,
  STATUS_COLORS,
  STATUS_LABELS,
} from "../utils/enums";

export default function IssueRow({ issue }) {
  const navigate = useNavigate();

  return (
    <tr className="issue-row" onClick={() => navigate(`/issues/${issue.id}`)}>
      <td className="issue-title">{issue.title}</td>
      <td>
        <Badge label={STATUS_LABELS[issue.status]} color={STATUS_COLORS[issue.status]} />
      </td>
      <td>
        <Badge
          label={PRIORITY_LABELS[issue.priority]}
          color={PRIORITY_COLORS[issue.priority]}
        />
      </td>
      <td>{issue.assignee ? issue.assignee.name : "—"}</td>
      <td>{issue.reporter.name}</td>
    </tr>
  );
}
