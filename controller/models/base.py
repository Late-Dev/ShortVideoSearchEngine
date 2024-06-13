import time
import uuid
from typing import Any, List, Union
from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict

import tritonclient.grpc
import tritonclient.utils
from socket import error as socket_error

@dataclass
class BaseModelPredictionData(ABC):
    model_prediction: Any

    @property
    def as_dict(self):
        return asdict(self)


class BaseTritonModel:

    def __init__(
            self,
            triton_url: str,
            triton_model_name: str,
            model_version: str,
            ):

        self.triton_url = triton_url
        self.triton_model_name = triton_model_name
        self.model_version = model_version

        self.n_connection_retries = 5
        self.connection_wait_time = 10

        self.triton_client = self._init_client(self.triton_url)

    def _init_client(self, triton_url: str):

        for conn_try in range(self.n_connection_retries):
            print("Trying to connect to TritonServer")
            triton_client = tritonclient.grpc.InferenceServerClient(
                    url=triton_url,
                    verbose=False,
                    )
            try:
                if triton_client.is_server_ready():
                    print("Inited Connection to TritonServer")
                    return triton_client
            except Exception:
                print(f"wait for reconnect to TritonServer {self.connection_wait_time}s")
                time.sleep(self.connection_wait_time)
        raise Exception("Triton Server Connection Error")

    def _get_model_status(self) -> bool:
        model_status = False
        try:
            model_status = self.triton_client.is_model_ready(
                    model_name=self.triton_model_name,
                    model_version=self.model_version
                    )
        except tritonclient.utils.InferenceServerException as err:
            print(f"Check Model {self.triton_model_name} Status Error: {err}")
        return model_status

    def _set_inputs(self) -> List:
        raise NotImplementedError("Implement this method")

    def _set_outputs(self) -> List:
        raise NotImplementedError("Implement this method")

    def __call__(self, *Args, **Kwargs) -> BaseModelPredictionData:
        raise NotImplementedError("Implement this method")

    def _request_model(self, inputs: List, outputs: List):
        request_id = uuid.uuid4()
        print(f"Processing request id: {request_id}, model: {self.triton_model_name}")

        response = self.triton_client.infer(
                model_name=self.triton_model_name,
                model_version=self.model_version,
                inputs=inputs,
                outputs=outputs,
                request_id=str(request_id)
                )
        return response

