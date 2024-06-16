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
  faces: Status;
  indexed_faces: Status;
  duration_frames: number;
  duration_speech: number;
  duration_indexed: number;
  duration_indexed_face: number;
  duration_face_analysis: number;
};
