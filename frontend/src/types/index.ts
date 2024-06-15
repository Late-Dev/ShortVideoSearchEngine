export type Videos = {
  link: string;
  description: string;
};

export type Status = "uploaded" | "processing" | "ready" | "error";

export type VideoWithStatus = {
  link: string;
  description: string;
  id: string;
  frames: Status;
  speech: Status;
  indexed: Status;
};
