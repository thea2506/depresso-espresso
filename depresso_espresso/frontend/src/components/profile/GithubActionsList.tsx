import { useState, useEffect } from "react";
import axios from "axios";

// components
import { UserInfo } from "../UserInfo";

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
    ref_type?: string;
  };
}

const GitHubActionsList = () => {
  const username = "thea2506";
  const githubUrl = `https://api.github.com/users/${username}/events`;
  const [events, setEvents] = useState<GitHubEvent[]>([]);

  //#region useEffect
  useEffect(() => {
    const getGitHubEvents = async (): Promise<void> => {
      const response = await axios(githubUrl);
      const data: GitHubEvent[] = response.data;

      // Transform the data to only include the fields we need and filtered out the necessary events
      const filteredData = data
        .map((event: GitHubEvent) => ({
          type: event.type,
          created_at: event.created_at,
          actor: {
            display_login: event.actor.display_login,
            avatar_url: event.actor.avatar_url,
          },
          repo: {
            name: event.repo.name,
            url: event.repo.url,
          },
          payload: {
            size: event.payload.size,
            action: event.payload.action,
            ref_type: event.payload.ref_type,
            issue: {
              title: event.payload.issue?.title,
            },
          },
        }))
        .filter((event: GitHubEvent) => {
          return [
            "CreateEvent",
            "ForkEvent",
            "PushEvent",
            "PullRequestEvent",
            "WatchEvent",
          ].includes(event.type);
        });

      setEvents(filteredData);
    };

    getGitHubEvents().catch((error) => {
      console.error(`Failed fetching data from GitHub: ${error}`);
    });
  }, [githubUrl]);
  //#endregion

  //#region functions
  const displayAction = (event: GitHubEvent) => {
    const actor = event.actor.display_login;
    switch (event.type) {
      case "CreateEvent":
        return event.payload.ref_type === "repository" ? (
          <p>
            {actor} <b>created</b> a {event.payload.ref_type}{" "}
            <b>{event.repo.name}</b>
          </p>
        ) : (
          <p>
            {actor} <b>created</b> a {event.payload.ref_type} at{" "}
            <b>{event.repo.name}</b>
          </p>
        );
      case "ForkEvent":
        return (
          <p>
            {actor} <b>forked</b> a repository <b>{event.repo.name}</b>{" "}
          </p>
        );
      case "PushEvent":
        return (
          <p>
            {actor} <b>pushed</b> {event.payload.size}{" "}
            {event.payload.size && event.payload.size > 1
              ? "commits"
              : "commit"}{" "}
            to <b>{event.repo.name}</b>
          </p>
        );
      case "PullRequestEvent":
        return (
          <p>
            {actor} <b>{event.payload.action}</b> a pull request at{" "}
            <b>{event.repo.name}</b>{" "}
          </p>
        );
      case "WatchEvent":
        return (
          <p>
            {actor} <b>{event.payload.action}</b> a repository{" "}
            <b>{event.repo.name}</b>
          </p>
        );
    }
  };
  //#endregion

  return (
    <div className="flex flex-col gap-y-4">
      {events.map((event) => {
        return (
          <div className="flex flex-col items-start px-6 py-6 gap-y-4 rounded-2xl bg-accent-3">
            <UserInfo
              username="Thea Nguyen"
              avatarURL={event.actor.avatar_url}
              time={event.created_at}
            />
            {displayAction(event)}
          </div>
        );
      })}
    </div>
  );
};

export { GitHubActionsList };
