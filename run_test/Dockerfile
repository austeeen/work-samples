FROM python:3

RUN pip install --no-cache-dir --user pytest pytest-cov

ENV SNAP="/path/to/snap/"
ENV SNAP_COMMON="/path/to/snap/common/"
ENV PYTHONPATH="PRIVATE"

WORKDIR /usr/src/app

CMD [ "python", "-m", "pytest" ]
