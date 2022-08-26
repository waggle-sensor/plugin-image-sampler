#!/usr/bin/env python3
# ANL:waggle-license
#  This file is part of the Waggle Platform.  Please see the file
#  LICENSE.waggle.txt for the legal details of the copyright and software
#  license.  For more details on the Waggle project, visit:
#           http://www.wa8.gl
# ANL:waggle-license
from datetime import datetime, timezone
import logging
import time
import os
import argparse

from waggle.plugin import Plugin
from waggle.data.vision import Camera
from croniter import croniter

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(message)s',
    datefmt='%Y/%m/%d %H:%M:%S')


def capture(plugin, cam, args):
    sample_file_name = "sample.jpg"
    sample = cam.snapshot()
    if args.out_dir == "":
        sample.save(sample_file_name)
        plugin.upload_file(sample_file_name)
    else:
        dt = datetime.fromtimestamp(sample.timestamp / 1e9)
        base_dir = os.path.join(args.out_dir, dt.astimezone(timezone.utc).strftime('%Y/%m/%d/%H'))
        os.makedirs(base_dir, exist_ok=True)
        sample_path = os.path.join(base_dir, dt.astimezone(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S%z.jpg'))
        sample.save(sample_path)


def run(args):
    logging.info("starting image sampler.")
    if args.cronjob == "":
        logging.info("capturing...")
        with Plugin() as plugin, Camera(args.stream) as cam:
            capture(plugin, cam, args)
        return 0
    
    logging.info("cronjob style sampling triggered")
    if not croniter.is_valid(args.cronjob):
        logging.error(f'cronjob format {args.cronjob} is not valid')
        return 1
    now = datetime.now(timezone.utc)
    cron = croniter(args.cronjob, now)
    with Plugin() as plugin, Camera(args.stream) as cam:
        while True:
            n = cron.get_next(datetime).replace(tzinfo=timezone.utc)
            now = datetime.now(timezone.utc)
            next_in_seconds = (n - now).total_seconds()
            if next_in_seconds > 0:
                logging.info(f'sleeping for {next_in_seconds} seconds')
                time.sleep(next_in_seconds)
            logging.info("capturing...")
            capture(plugin, cam, args)
    return 0


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-stream', dest='stream',
        action='store', default="camera", type=str,
        help='ID or name of a stream, e.g. sample')
    parser.add_argument(
        '-out-dir', dest='out_dir',
        action='store', default="", type=str,
        help='Path to save images locally in %Y-%m-%dT%H:%M:%S%z.jpg format')
    parser.add_argument(
        '-cronjob', dest='cronjob',
        action='store', default="", type=str,
        help='Time interval expressed in cronjob style')

    args = parser.parse_args()
    if args.out_dir != "":
        os.makedirs(args.out_dir, exist_ok=True)
    exit(run(args))
