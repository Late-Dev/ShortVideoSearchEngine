import os
import gc
import sys
import json
from typing import Dict, List
import itertools
import random

import av
import numpy as np

try:
    # noinspection PyUnresolvedReferences
    import triton_python_backend_utils as pb_utils
except ImportError:
    pass  # triton_python_backend_utils exists only inside Triton Python backend.

import torch
from transformers import AutoProcessor, AutoModel


class TritonPythonModel:

    model: AutoModel

    def initialize(self, args: Dict[str, str]) -> None:
        """
        Initialize the tokenization process
        :param args: arguments from Triton config file
        """
        self.logger = pb_utils.Logger

        model_config = json.loads(args["model_config"])
        try:
            gpu_id = model_config["instance_group"][0]["gpus"][0]
        except Exception as err:
            gpu_id = None
        self.device_map = f"cuda:{gpu_id}" if gpu_id != None else "cpu"

        output_config = pb_utils.get_output_config_by_name(
            model_config, "EMBEDDING"
        )
        # Convert Triton types to numpy types
        self.output_dtype = pb_utils.triton_string_to_numpy(output_config["data_type"])

        # Set weights paths
        path: str = args["model_repository"]
        self.model_version = "1"
        self.weights_path = os.path.join(path, self.model_version, "weights/")

        self.processor = AutoProcessor.from_pretrained(self.weights_path)
        self.model = self._get_model()

    def _get_model(self):
        model = AutoModel.from_pretrained(self.weights_path, device_map=self.device_map)
        self.projector = torch.nn.Linear(512, 1024, bias=False)
        self.projector.load_state_dict(torch.load(os.path.join(self.weights_path, 'projector.pth')))
        self.projector.to(self.device_map)
        model.eval()
        self.projector.eval()
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
            if request.is_cancelled():
                responses.append(pb_utils.InferenceResponse(
                    error=pb_utils.TritonError(f"Request {request.request_id} cancelled", pb_utils.TritonError.CANCELLED)))
            else:
                # binary data typed back to string
                b_video_path = pb_utils.get_input_tensor_by_name(request, "video_path").as_numpy()
                video_path = self._decode_batch_text_input(b_video_path)[0]

                video_emb = self.get_vidio_features(video_path)

                outputs = np.array(video_emb)
                outputs = pb_utils.Tensor("EMBEDDING", outputs.astype(self.output_dtype))

                inference_response = pb_utils.InferenceResponse(output_tensors=[outputs])
                responses.append(inference_response)

        return responses

    def _decode_batch_text_input(self, byte_string_batch: List[bytes]) -> List[str]:
        encoded_batch = [ b_str.decode("utf-8") for b_str in byte_string_batch ]
        return encoded_batch

    def read_video_pyav(self, container, indices):
        '''
        Decode the video with PyAV decoder.
        Args:
            container (`av.container.input.InputContainer`): PyAV container.
            indices (`List[int]`): List of frame indices to decode.
        Returns:
            result (np.ndarray): np array of decoded frames of shape (num_frames, height, width, 3).
        '''
        frames = []
        container.seek(0)
        start_index = indices[0]
        end_index = indices[-1]
        for i, frame in enumerate(container.decode(video=0)):
            if i > end_index:
                break
            if i >= start_index and i in indices:
                frames.append(frame)
        return np.stack([x.to_ndarray(format="rgb24") for x in frames])

    def sample_frame_indices(self, clip_len, frame_sample_rate, seg_len):
        '''
        Sample a given number of frame indices from the video.
        Args:
            clip_len (`int`): Total number of frames to sample.
            frame_sample_rate (`int`): Sample every n-th frame.
            seg_len (`int`): Maximum allowed index of sample's last frame.
        Returns:
            indices (`List[int]`): List of sampled frame indices
        '''
        converted_len = int(clip_len * frame_sample_rate)
        end_idx = np.random.randint(converted_len, seg_len)
        start_idx = end_idx - converted_len
        indices = np.linspace(start_idx, end_idx, num=clip_len)
        indices = np.clip(indices, start_idx, end_idx - 1).astype(np.int64)
        return indices

    def get_vidio_features(self, video_path):
        # answer = ''
        answers = []
        container = av.open(video_path)

        # sample uniformly 8 frames from the video
        total_frames = container.streams.video[0].frames
        indices = np.arange(0, total_frames, total_frames / 8).astype(int)
        clip = self.read_video_pyav(container, indices)

        inputs = self.processor(text='', videos=list(clip), return_tensors="pt")
        for i in inputs:
            inputs[i] = inputs[i].to(self.device_map)
        video_features = self.projector(self.model(**inputs).video_embeds)[0].tolist()
        return video_features

