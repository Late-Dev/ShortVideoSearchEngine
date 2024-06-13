from typing import Any, Dict, List
from dataclasses import dataclass

import numpy as np
import tritonclient.grpc

from infrastructure.base_model import BaseModelPredictionData, BaseTritonModel


class SpeechPredictionData(BaseModelPredictionData):
    audio_text: str


@dataclass
class SpeechModelInputs:
    video_url: str


class SpeechTritonModel(BaseTritonModel):

    def __init__(
            self,
            triton_url: str,
            triton_model_name: str,
            model_version: str,
            ):
        super().__init__(triton_url, triton_model_name, model_version)
        self.model_output_name = "AUDIO_TEXT"
        self.batch_size = 1

    def _set_inputs(
            self,
            model_inputs: SpeechModelInputs
            ) -> List:

        inputs = [
                tritonclient.grpc.InferInput(name="video_url", shape=(self.batch_size,), datatype="BYTES"),
                ]

        inputs[0].set_data_from_numpy(np.asarray([[model_inputs.video_url]], dtype=object))
        return inputs

    def _set_outputs(self) -> List:
        outputs = [
                tritonclient.grpc.InferRequestedOutput(name=self.model_output_name)
                ]
        return outputs

    def __call__(
            self,
            model_inputs: SpeechModelInputs
            ) -> SpeechPredictionData:

        inputs = self._set_inputs(model_inputs)
        outputs = self._set_outputs()

        response = self._request_model(inputs, outputs)
        res = response.get_output(self.model_output_name)["data"][0]
        return SpeechPredictionData(audio_text=res)

