from typing import Any, Dict, List
from dataclasses import dataclass

import numpy as np
import tritonclient.grpc

from models.base import BaseTritonModel


@dataclass
class XclipPredictionData:
    embedding: str


@dataclass
class XclipModelInputs:
    video_url: str


class XclipTritonModel(BaseTritonModel):

    def __init__(
            self,
            triton_url: str,
            triton_model_name: str,
            model_version: str,
            ):
        super().__init__(triton_url, triton_model_name, model_version)
        self.model_output_name = "EMBEDDING"
        self.batch_size = 1

    def _set_inputs(
            self,
            model_inputs: XclipModelInputs
            ) -> List:

        inputs = [
                tritonclient.grpc.InferInput(name="video_url", shape=(self.batch_size,), datatype="BYTES"),
                ]

        inputs[0].set_data_from_numpy(np.asarray([model_inputs.video_url]*self.batch_size, dtype=object))
        return inputs

    def _set_outputs(self) -> List:
        outputs = [
                tritonclient.grpc.InferRequestedOutput(name=self.model_output_name)
                ]
        return outputs

    def __call__(
            self,
            model_inputs: XclipModelInputs
            ) -> XclipPredictionData:

        inputs = self._set_inputs(model_inputs)
        outputs = self._set_outputs()

        response = self._request_model(inputs, outputs)
        res = response.as_numpy(self.model_output_name).tolist()
        return XclipPredictionData(embedding=res)

