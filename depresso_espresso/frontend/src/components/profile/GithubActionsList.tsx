import { useState, useEffect } from "react";
import axios from "axios";

export interface GitHubEvent {
  type: string;
  created_at: string;
  actor: {
    display_login: string;
    avatar_url: string;
  };
  repo: {
    name: string;
    url: string;
  };
  payload: {
    size?: number;
    action?: string;
    issue?: {
      title?: string;
    };
  };
}

const GitHubActionsList = () => {
  const username = "thea2506";
  const githubUrl = `https://api.github.com/users/${username}/events`;
  const [events, setEvents] = useState<GitHubEvent[]>([]);

  useEffect(() => {
    const getGitHubEvents = async (): Promise<void> => {
      const response = await axios(githubUrl);
      const data: GitHubEvent[] = response.data;
      setEvents(data);
    };

    getGitHubEvents();
  }, [githubUrl]);

  console.log(events);
  return <div>List</div>;
};

export { GitHubActionsList };
