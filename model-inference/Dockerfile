FROM nvcr.io/nvidia/tritonserver:24.05-py3
ARG DEBIAN_FRONTEND=noninteractive

WORKDIR /src
COPY ./requirements.txt $WORKDIR

RUN apt-get update && apt-get clean && apt-get install ffmpeg libsm6 libxext6 libopencc-dev  -y
RUN pip install -U pip && \
	pip install cython

RUN pip install h5py==3.8.0
RUN pip install -r requirements.txt

RUN export LC_ALL=C.UTF-8

ENTRYPOINT [ "tritonserver" , "--model-repository=/models"]
