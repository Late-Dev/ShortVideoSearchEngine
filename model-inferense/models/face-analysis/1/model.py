import os
import uuid
import shutil
import subprocess
from io import BytesIO
import sys
import json
from typing import Dict, List
import itertools
import tempfile

import cv2
import numpy as np
import requests

try:
    # noinspection PyUnresolvedReferences
    import triton_python_backend_utils as pb_utils
except ImportError:
    pass  # triton_python_backend_utils exists only inside Triton Python backend.
from insightface.app import FaceAnalysis
from sklearn.cluster import DBSCAN


class TritonPythonModel:

    def initialize(self, args: Dict[str, str]) -> None:
        """
        Initialize the tokenization process
        :param args: arguments from Triton config file
        """
        self.logger = pb_utils.Logger

        model_config = json.loads(args["model_config"])
        output0_config = pb_utils.get_output_config_by_name(
            model_config, "EMBEDDINGS"
        )
        # Convert Triton types to numpy types
        self.output_dtype = pb_utils.triton_string_to_numpy(output0_config["data_type"])

        self.providers: List[str] = ["CUDAExecutionProvider"]
        self.allowed_modules: List[str] = ["detection", "landmark_3d_68", "landmark_2d_106", "recognition"]
        self.frame_size: List[int] = [640, 640]
        self.model_version = "1"
        self.models_name = "buffalo_l"
        self.model = self._get_model()

    def _get_model(self):
        model = FaceAnalysis(name=self.models_name, providers=self.providers, allowed_modules=self.allowed_modules)
        model.prepare(ctx_id=0, det_size=self.frame_size)
        return model

    def execute(self, requests) -> "List[List[pb_utils.Tensor]]":
        """
        Parse and tokenize each request
        :param requests: 1 or more requests received by Triton server.
        :return: text as input tensors
        """

        responses = []
        # for loop for batch requests (disabled in our case)
        for request in requests:
            self.logger.log_info(f"processing request #{request.request_id()}")

            if request.is_cancelled():
                responses.append(pb_utils.InferenceResponse(
                    error=pb_utils.TritonError(f"Request {request.request_id} cancelled", pb_utils.TritonError.CANCELLED)))
            else:
                # binary data typed back to string
                b_video_urls = pb_utils.get_input_tensor_by_name(request, "video_url").as_numpy()
                video_url = self._decode_batch_text_input(b_video_urls)[0]
                video_path = self._download_video(video_url)
                all_embeddings = []

                for frame in self._get_video_frames(video_path):
                    faces = self.model.get(frame)
                    all_embeddings.extend([face.embedding for face in faces])

                unique_embeddings = self._get_unique_embeddings_dbscan(all_embeddings) # List[np.ndarray]
                outputs = np.array(unique_embeddings)
                outputs = pb_utils.Tensor("EMBEDDINGS", outputs.astype(self.output_dtype))

                inference_response = pb_utils.InferenceResponse(output_tensors=[outputs])
                responses.append(inference_response)

            return responses

    def _decode_batch_text_input(self, byte_string_batch: List[bytes]) -> List[str]:
        encoded_batch = [ b_str.decode("utf-8") for b_str in byte_string_batch ]
        return encoded_batch

    def _download_video(self, video_url: str):
        try:
            response = requests.get(video_url, stream=True)
            response.raise_for_status()
            temp_video_file = tempfile.NamedTemporaryFile(delete=False)
            with temp_video_file as f:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
            return temp_video_file.name
        except requests.exceptions.RequestException as e:
            print(f"Error downloading video: {e}")
            return None

    def _get_video_frames(self, video_path: str):
        cap = cv2.VideoCapture(video_path)
        frame_count = 0
        frame_interval = 30
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            if frame_count % frame_interval == 0:
                yield frame
            frame_count += 1
        cap.release()

    def _get_unique_embeddings_dbscan(self, embeddings: List[np.ndarray]) -> List[np.ndarray]:
        if not embeddings:
            return []

        clustering = DBSCAN(eps=0.5, min_samples=1, metric='cosine').fit(embeddings)
        labels = clustering.labels_
        unique_labels = set(labels) - {-1}

        unique_embeddings = []
        for label in unique_labels:
            cluster_indices = np.where(labels == label)[0]
            cluster_embeddings = [embeddings[idx] for idx in cluster_indices]
            mean_embedding = np.mean(cluster_embeddings, axis=0)
            unique_embeddings.append(mean_embedding)

        return unique_embeddings

