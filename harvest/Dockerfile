FROM python:3

RUN pip install --no-cache-dir --user boto3==1.16.56 requests

WORKDIR /usr/src/app

CMD [ "python3", "-m" "tools.collect_no_sale_images.py", "PRIVATE_PARAMS" ]
