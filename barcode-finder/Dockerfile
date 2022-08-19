FROM ubuntu:18.04

RUN apt-get update && \
    apt-get -y install \
        build-essential \
        cmake \
        libhiredis-dev \
        libevent-dev \
        pkg-config \
        libjpeg-dev \
        redis-tools \
        python3 \
        python3-pip

RUN pip3 install redis boto3 tqdm

COPY src/SD/libid_FlexRelease_linux_x64.so /usr/lib/x86_64-linux-gnu

RUN mkdir -p /usr/src/deps
RUN ln -s /usr/lib/x86_64-linux-gnu/cmake/Hiredis/HiredisConfig.cmake /usr/src/deps/hiredis-config.cmake
ENV CMAKE_PREFIX_PATH=/usr/src/deps

RUN ldconfig

COPY . /usr/src/app/
WORKDIR /usr/src/app/

RUN mkdir build && cd build && cmake ../src/ && make

CMD ["./build/Analyzer"]
