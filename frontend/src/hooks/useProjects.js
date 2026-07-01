import { useCallback, useEffect, useState } from "react";

import { listProjects } from "../services/projects";
import { getErrorMessage } from "../services/api";

// Loads the current user's projects and exposes a `reload` for after creating one.
export function useProjects() {
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const reload = useCallback(() => {
    setLoading(true);
    listProjects()
      .then(setProjects)
      .catch((err) => setError(getErrorMessage(err)))
      .finally(() => setLoading(false));
  }, []);

  useEffect(() => {
    reload();
  }, [reload]);

  return { projects, loading, error, reload };
}
