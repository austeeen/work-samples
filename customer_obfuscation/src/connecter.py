#!/usr/bin/env python

import redis
import json
import os
import signal
import requests
import logging
import sys
import time
import socket

from PIL import Image, ImageFilter
from io import BytesIO

sys.path.append(os.path.dirname(sys.path[0]))

from pkgs import CaffeFaceDetect
from pkgs import DeepLabModel
from uploader import S3, Gcloud

# Setup Logging
level = os.environ.get("LOGLEVEL", "INFO").upper()
log = logging.getLogger()
log.setLevel(level)
ch = logging.StreamHandler()
fmt = logging.Formatter('%(asctime)s::%(levelname)s - %(message)s')
ch.setFormatter(fmt)
log.addHandler(ch)


def get_input(r, key):
    """Retrieve the json from Redis"""
    redis_retry_count = 0
    blocking_timeout_seconds = 5
    in_data = None
    while not in_data:
        try:
            popped = r.brpop(key, blocking_timeout_seconds)
            if popped:
                in_data = json.loads(popped[1].decode('utf-8'))
        except redis.exceptions.ConnectionError as ce:
            retry_delay_seconds = 5
            log.critical(str(ce), exc_info=True)
            if redis_retry_count < 3:
                redis_retry_count += 1
                log.info("Retrying redis connection in {}".format(retry_delay_seconds))
                time.sleep(retry_delay_seconds)
            else:
                log.critical("Could not connect to redis, shutting down")
                exit(1)
    return in_data


def send_response(r, key, data):
    """Return the results to Redis"""
    r.lpush(key, json.dumps(data))


def get_env_vars():
    """Grab the necessary environment variables"""
    try:
        review_key = os.environ['REDIS_KEY']
        result_key = os.environ['REDIS_RESULT_KEY']
        redis_url = os.environ['REDIS_URL']
        bucket = os.environ['BUCKET']
        platform = os.environ['PLATFORM']
    except Exception as e:
        log.error("Error getting environment variables: {}".format(e))
        return None, None, None, None, None, None

    return review_key, result_key, redis_url, bucket, platform


def get_image(url):
    """Get the image by accessing the url provided from Redis"""
    try:
        response = requests.get(url)
    except Exception as e:
        log.error("An error occurred while trying to get image: {}".format(e), exc_info=True)
        return None

    if not response.ok:
        log.error("Error getting image from " + url)
        return None

    return response.content


def trim_results(in_data):
    """We only care about the bounding box for the face"""
    out_data = []
    for face in in_data:
        out_data.append(face['bndbox'])

    return out_data


def mask_faces(img, faces):
    """
    Mask the faces that were found in the image

    DEPRECATED due to segmentation fault with caffe detections
    """
    image = Image.open(BytesIO(img))

    for face in faces:
        face_location = (face['xmin'], face['ymin'], face['xmax'], face['ymax'])
        cimg = image.crop(face_location)
        bimg = cimg.filter(ImageFilter.GaussianBlur(30))
        # Todo fix segmentation fault after multiple faces in a single image
        image.paste(bimg, face_location)

    return image


def deep_lab_blur(model, uploader, data, res_data):
    for image in data['images']:
        log.info("Processing image: {}".format(image))
        img = get_image(image['url'])

        if img is None:
            log.warning("No image was returned. Skipping!")
            continue

        # Detect faces and then blur them
        blurred_image, _, blur_image = model.blur(Image.open(BytesIO(img)))

        if blur_image:
            ret_obj = uploader.upload(blurred_image.convert('RGB'), res_data['capture_event_id'],
                                      image['camera_label'])
            if ret_obj:
                res_data['images'].append(ret_obj)
        else:
            print("No blur detected, not uploading: " + image['camera_label'])


def deep_lab_blur_benchmark(uploader, data, res_data):
    log.info("Starting Deep Lab Blur Benchmarking service")

    log.info("Initializing with CPU")
    deep_lab_cpu = DeepLabModel(use_gpu=False)
    log.info("Initializing with GPU")
    deep_lab_gpu = DeepLabModel(use_gpu=True)

    if deep_lab_gpu.num_gpus == 0:
        log.warn("No GPUs available, quitting benchmark.")
        return res_data

    def _blur_and_upload(deep_lab_model):
        for image in data['images']:
            log.info("Processing image: {}".format(image))
            img = get_image(image['url'])

            if img is None:
                log.warning("No image was returned. Skipping!")
                continue

            # Detect faces and then blur them
            blurred_image, _ = deep_lab_model.blur(Image.open(BytesIO(img)))
            ret_obj = uploader.upload(blurred_image.convert('RGB'), res_data['capture_event_id'],
                                      image['camera_label'])
            if ret_obj:
                res_data['images'].append(ret_obj)

        return deep_lab_model.get_average_time()

    cpu_time = _blur_and_upload(deep_lab_cpu)
    gpu_time = _blur_and_upload(deep_lab_gpu)

    log.info("DEEP LAB CPU TIME: " + str(cpu_time))
    log.info("DEEP LAB GPU TIME: " + str(gpu_time))


def caffe_face_detect(model, uploader, data, res_data):
    if 'min_confidence' in data:
        log.info("Using confidence level: {}".format(data["min_confidence"]))
        model.min_confidence_threshold = float(data["min_confidence"])

    for image in data['images']:
        log.info("Processing image: {}".format(image))
        img = get_image(image['url'])

        if img is None:
            log.warning("No image was returned. Skipping!")
            continue

        # Detect faces and then blur them
        image_obj, blur_detected = model.blur_face_byte_str(img, write_yaml=False)
        blurred_image = Image.open(BytesIO(image_obj))

        # if there was nothing to blur then don't upload anything
        if blur_detected:
            ret_obj = uploader.upload(blurred_image.convert('RGB'), res_data['capture_event_id'],
                                      image['camera_label'])
            if ret_obj:
                res_data['images'].append(ret_obj)
        else:
            print("No blur detected, not uploading: " + image['camera_label'])

def terminate(signum, frame):
    """Terminate the program when we receive SIGTERM or SIGINT"""
    log.critical("Shutting down")
    exit()


def main():
    # Graceful exits
    signal.signal(signal.SIGINT, terminate)
    signal.signal(signal.SIGTERM, terminate)

    rev_key, res_key, redis_url, bucket, platform = get_env_vars()
    if None in (rev_key, res_key, redis_url, bucket, platform):
        log.critical("Missing environment variable")
        exit(1)

    uploader = None
    if platform == 'aws':
        uploader = S3(bucket, log, os.environ.get('TEST_RUN'))
    elif platform == 'google':
        uploader = Gcloud(bucket, log)
    else:
        log.critical("The specified platform ({}) is not supported! Supported platforms: aws, "
                     "google".format(platform))
        exit(1)

    r = redis.from_url(url=redis_url)
    blur_mode = ""
    model = None

    while True:
        data = get_input(r, rev_key)

        if data['blur_mode'] != blur_mode:
            blur_mode = data['blur_mode']
            try:
                if data['blur_mode'] == "deep_lab":
                    log.info("Starting Deep Lab blur service")
                    model = DeepLabModel()
                elif data['blur_mode'] == "caffe_detect":
                    log.info("Starting Caffe Face Detect blur service")
                    model = CaffeFaceDetect(debug=0, logger=log)
                else:
                    log.critical("Blur mode '{}' not valid. Valid modes are [ deep_lab | "
                                 "caffe_detect ]".format(data['blur_mode']))
            except KeyError:
                log.critical("key [ blur_mode ] not found in redis data.")

        res_data = {'capture_event_id': data['capture_event_id'], 'bucket': bucket, 'images': []}

        if model:
            if data['blur_mode'] == "deep_lab":
                deep_lab_blur(model, uploader, data, res_data)
            else:
                caffe_face_detect(model, uploader, data, res_data)
        else:
            log.critical("error model not instantiated: blur_mode = " + data['blur_mode'])

        send_response(r, res_key, res_data)


if __name__ == '__main__':
    log.info("Starting Blur Service")
    main()
