import os
import uuid
import shutil
import subprocess
from io import BytesIO
import sys
import json
from typing import Dict, List
import itertools

import numpy as np
import requests

try:
    # noinspection PyUnresolvedReferences
    import triton_python_backend_utils as pb_utils
except ImportError:
    pass  # triton_python_backend_utils exists only inside Triton Python backend.


class TritonPythonModel:

    def initialize(self, args: Dict[str, str]) -> None:
        """
        Initialize the tokenization process
        :param args: arguments from Triton config file
        """
        self.logger = pb_utils.Logger

        model_config = json.loads(args["model_config"])
        output0_config = pb_utils.get_output_config_by_name(
            model_config, "EMBEDDING"
        )
        # Convert Triton types to numpy types
        self.text_output_dtype = pb_utils.triton_string_to_numpy(output0_config["data_type"])

        self.tmp_dir_name = f"/src/tmp/{str(uuid.uuid4())}/"
        os.makedirs(self.tmp_dir_name, exist_ok=True)

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

                # send requests to other models
                xclip_input = pb_utils.Tensor("video_path", np.asarray([video_path], dtype=object))
                embedding = self._call_neighboor_model("xclip-custom", ["EMBEDDING"], [xclip_input])

                output_1 = pb_utils.Tensor("EMBEDDING", embedding[0].astype(self.text_output_dtype))
                inference_response = pb_utils.InferenceResponse(output_tensors=[output_1])
                responses.append(inference_response)

        return responses

    def _decode_batch_text_input(self, byte_string_batch: List[bytes]) -> List[str]:
        encoded_batch = [ b_str.decode("utf-8") for b_str in byte_string_batch ]
        return encoded_batch

    def _download_video(self, video_url: str):
        video_path = os.path.join(self.tmp_dir_name, "video.mp4")
        response = requests.get(video_url, stream=True)
        response.raise_for_status()
        video_bytes = response.content

        self.logger.log_info(f"Downloaded video {video_url}")
        self._write_bytes_to_disk(video_path, video_bytes)
        return video_path

    def _write_bytes_to_disk(self, file_path, file_bytes):
        with open(file_path, 'wb') as f:
            f.write(file_bytes)

    def _call_neighboor_model(self, model_name: str, output_names: List[str], input_tensors: List):
        responses = []
        # Create inference request object
        infer_request = pb_utils.InferenceRequest(
            model_name=model_name,
            requested_output_names=output_names,
            inputs=input_tensors,
        )

        # Perform synchronous blocking inference request
        infer_response = infer_request.exec()

        # Make sure that the inference response doesn't have an error. If
        # it has an error and you can't proceed with your model execution
        # you can raise an exception.
        if infer_response.has_error():
            raise pb_utils.TritonModelException(infer_response.error().message())

        for output_name in output_names:
            out = pb_utils.get_output_tensor_by_name(infer_response, output_name).as_numpy()
            responses.append(out)
        return responses

    def finalize(self):
        """finalize` is called only once when the model is being unloaded.
        Implementing `finalize` function is OPTIONAL. This function allows
        the model to perform any necessary clean ups before exit.
        """
        print("Cleaning up...")
        shutil.rmtree(self.tmp_dir_name)
