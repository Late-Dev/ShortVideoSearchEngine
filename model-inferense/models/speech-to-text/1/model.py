import os
import gc
import sys
import json
from typing import Dict, List
import itertools
import random

import numpy as np

try:
    # noinspection PyUnresolvedReferences
    import triton_python_backend_utils as pb_utils
except ImportError:
    pass  # triton_python_backend_utils exists only inside Triton Python backend.
import nemo.collections.asr as nemo_asr


class TritonPythonModel:

    model: nemo_asr

    def initialize(self, args: Dict[str, str]) -> None:
        """
        Initialize the tokenization process
        :param args: arguments from Triton config file
        """
        self.logger = pb_utils.Logger

        model_config = json.loads(args["model_config"])
        gpu_id = model_config["instance_group"][0]["gpus"][0]
        output_config = pb_utils.get_output_config_by_name(
            model_config, "GENERATED_OUTPUT"
        )
        # Convert Triton types to numpy types
        self.output_dtype = pb_utils.triton_string_to_numpy(output_config["data_type"])

        # Set weights paths
        path: str = args["model_repository"]
        self.model_version = "1"
        self.weights_path = os.path.join(path, self.model_version, "weights/stt_ru_conformer_transducer_large.nemo")

        self.load_in_8bit = True

        self.model = self._get_model()

    def _get_model(self):
        model = nemo_asr.models.EncDecRNNTBPEModel.restore_from(self.weights_path)
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
                import pdb; pdb.set_trace()
                raw_audio = pb_utils.get_input_tensor_by_name(request, "raw_audio").as_numpy()

                self.logger.log_info(f"request #{request.request_id()} processed")
                responses.append(inference_response)

        return responses

    def _decode_batch_text_input(self, byte_string_batch: List[bytes]) -> List[str]:
        encoded_batch = [ b_str.decode("utf-8") for b_str in byte_string_batch ]
        return encoded_batch

