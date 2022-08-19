FROM python:3.9

COPY requirements.txt /tmp/
RUN pip install --no-cache-dir --user -r /tmp/requirements.txt

EXPOSE 5000
ENV PYTHONUNBUFFERED 1

ENV PYTHONPATH "${PYTHONPATH}:/usr/src/app/src"
ENV PATH="/root/.local/bin:${PATH}"

WORKDIR /usr/src/app
COPY . /usr/src/app

CMD [ "gunicorn", "--bind", "PRIVATE:PRIVATE", "--access-logfile", "-", "--error-logfile", "-", \
      "--threads", "10", "PRIVATE:app" ]
