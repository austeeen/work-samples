#!/bin/python3

import os
import sys
import json
import redis
import tqdm
import argparse
import logging


ENVS = {
    "HOST": os.getenv("REDIS_SERVER"),
    "PORT": int(os.getenv("REDIS_PORT")),
    "REDIS_RESULTS": os.getenv('REDIS_RESULT_KEY'),
    "REDIS_KEY": os.getenv('REDIS_KEY'),
    "WRITE_BATCH_SIZE": 200,
    "PULL_TIMEOUT": 60,
    "START_FLAG": os.getenv("START_FLAG"),
    "STOP_FLAG": os.getenv("STOP_FLAG"),
    "INIT_FLAG": os.getenv("INIT_FLAG"),
    "RESULT_FLAG": os.getenv("RESULT_FLAG"),
    "DATA_ROOT": "customer_images",
    "MSG_LOG": "customer_images/monitor.log",
    "ERR_LOG": "customer_images/monitor.error.log",
}

if any([not v for v in ENVS.values()]):
    print("ERROR: missing environment values")
    print(json.dumps(ENVS, indent=2))
    exit(0)


if not os.path.exists(ENVS['DATA_ROOT']):
    print("WARNING: critical data root directory {} does not exist. creating this for you.".format(
          ENVS['DATA_ROOT']))
    os.makedirs(ENVS['DATA_ROOT'])


def create_logger(log_fp: str, log_level="debug", append=False, to_console=False):
    new_logger = logging.getLogger(os.path.basename(log_fp))
    formatter = logging.Formatter(fmt="[%(asctime)s][%(levelname)s]:(%(funcName)s) %(message)s",
                                  datefmt='%m/%d/%Y %I:%M:%S%p')

    numeric_level = getattr(logging, log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % log_level)
    new_logger.setLevel(numeric_level)

    f_handler = logging.FileHandler(log_fp, mode='a' if append else 'w')
    f_handler.setFormatter(formatter)
    f_handler.setLevel(new_logger.getEffectiveLevel())
    new_logger.addHandler(f_handler)

    if to_console:
        s_handler = logging.StreamHandler()
        s_handler.setFormatter(formatter)
        new_logger.addHandler(s_handler)
    new_logger.propagate = False

    return new_logger


msg_log = create_logger(ENVS['MSG_LOG'])
err_log = create_logger(ENVS['ERR_LOG'])


class RedisService:
    rd = redis.Redis(ENVS['HOST'], ENVS['PORT'])

    def __init__(self):
        self._running = False
        self.send_queue = ENVS['REDIS_KEY']
        self.result_queue = ENVS['REDIS_RESULTS']

    def __str__(self):
        return "[" + self.__class__.__name__ + "] "

    def log(self, msg: str):
        msg_log.info(str(self) + " " + msg)

    def get_queue_sizes(self):
        return self.llen(self.send_queue) + self.llen(self.result_queue)

    def llen(self, list_name: str) -> int:
        return int(self.rd.llen(list_name))

    def pop_msg(self) -> list:
        key = self.rd.blpop(self.result_queue)
        if not key:
            msg_log.warning(str(self) + "blpop returned nothing!")
            return []
        msg = key[1].decode('utf8')
        return msg.split(maxsplit=1)

    def push_msg(self, msg: str):
        self.rd.lpush(self.send_queue, msg)

    def pop(self) -> (str, str):
        try:
            msg: list = self.pop_msg()
            msg_log.info("received: {}".format(msg))
            if len(msg) == 1:
                return msg[0], ""
            if len(msg) == 2:
                return msg[0], msg[1]
            msg_log.warning("{} bad msg: {}".format(str(self), msg))
        except Exception as e:
            err_log.error(str(e))

        return "", ""


redis_service = RedisService()


def pull_results(img_count: int, out_fn: str):
    with open(out_fn, 'w') as f:
        json.dump({"results": []}, f)

    print("monitor start: {} results expected. dumping results to {}.".format(img_count, out_fn))
    print("further messages/errors will now be logged at {}".format(ENVS['DATA_ROOT']))

    progress_bar = tqdm.tqdm(total=img_count)
    batch = []
    running = True

    def dump_batch():
        file_data = json.load(open(out_fn, 'r'))
        file_data['results'].extend(batch)
        json.dump(file_data, open(out_fn, 'w'))
        msg_log.info(" << dumped: {} results to {}".format(len(batch), out_fn))

    def process_result(res_data: str):
        if not res_data:
            err_log.error("expected data from flag: {}, no data given.".format(flag))
            return
        try:
            res_data = json.loads(res_data.replace("'", '"'))
        except json.JSONDecodeError as e:
            err_log.error(str(e))
            return

        batch.append(res_data)
        progress_bar.update(1)
        if len(batch) == ENVS['WRITE_BATCH_SIZE']:
            dump_batch()
            batch.clear()

    while running:
        flag, data = redis_service.pop()

        if flag == ENVS['STOP_FLAG']:
            msg_log.info("stop received")
            dump_batch()
            running = False
        elif flag == ENVS['RESULT_FLAG']:
            process_result(data)
        else:
            err_log.error("bad msg: {} : {}".format(flag, data))
            dump_batch()
            running = False

    while redis_service.llen(ENVS["REDIS_RESULTS"]) > 0:
        msg_log.info("result queue not empty")
        flag, data = redis_service.pop()

        if flag == ENVS['RESULT_FLAG']:
            process_result(data)

    progress_bar.close()


def start_up(target_dir: str) -> int:
    if redis_service.get_queue_sizes() > 0:
        print("warning: redis queues not empty!")

    num_images = 0
    print("sending '{} {}' to decoder service".format(ENVS['START_FLAG'], target_dir))
    redis_service.push_msg("{} {}".format(ENVS['START_FLAG'], target_dir))

    print("waiting for {} flag from decoder service".format(ENVS['INIT_FLAG']))
    running = True
    while running:
        flag, num_images = redis_service.pop()
        if flag == ENVS['INIT_FLAG']:
            print("init received, processing {} image files.".format(num_images))
            running = False
        else:
            print("bad msg: flag: {}, msg: {}".format(flag, num_images))
            running = False
    return int(num_images)


def get_args(argv):
    parser = argparse.ArgumentParser("monitor barcode finder service")
    parser.add_argument("--target_dir", required=True)
    parser.add_argument("--skip-startup", action="store_true", default=False)
    parser.add_argument("-o", "--out-fn", dest="out_fn", default="results.json")

    args = parser.parse_args(argv)
    return args


def main(argv):
    args = get_args(argv)

    out_fn = os.path.join(ENVS['DATA_ROOT'], args.out_fn)

    if args.skip_startup:
        print("skipping start up")
        num_images = redis_service.get_queue_sizes()
    else:
        num_images = start_up(args.target_dir)

    if not num_images:
        print("ERROR: no images, quiting.")
        exit(0)

    pull_results(num_images, out_fn)

    print("\ndone.")


if __name__ == "__main__":
    main(sys.argv[1:])
