FROM nvcr.io/nvidia/tensorrt:19.10-py3

# Tensor GPU and OpenCV dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libsm6 libxrender1 libxext6 libglib2.0-0

# Curl/zip
RUN apt install -y --no-install-recommends curl zip unzip libcurl4-openssl-dev
RUN mkdir /usr/src/deps

# python and requirements
RUN curl https://bootstrap.pypa.io/pip/3.6/get-pip.py -o get-pip.py
RUN python get-pip.py

RUN python -m pip install --upgrade pip

COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

COPY . /usr/src/app
WORKDIR /usr/src/app

ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/lib/x86_64-linux-gnu:/usr/local/cuda/lib64
RUN ldconfig

CMD [ "./src/connecter.py" ]