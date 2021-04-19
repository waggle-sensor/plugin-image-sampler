#!/usr/bin/env python3
# ANL:waggle-license
#  This file is part of the Waggle Platform.  Please see the file
#  LICENSE.waggle.txt for the legal details of the copyright and software
#  license.  For more details on the Waggle project, visit:
#           http://www.wa8.gl
# ANL:waggle-license
from datetime import datetime, timezone
import time
import os
import argparse

import cv2

import waggle.plugin as plugin
from waggle.data import open_data_source

plugin.init()


def run(args):
    print(f"starting image sampler. will sample every {args.interval}s", flush=True)

    if args.out_dir != "":
        os.makedirs(args.out_dir, exist_ok=True)

    with open_data_source(id=args.stream) as cam:
        while True:
            time.sleep(args.interval)

            print("getting image", flush=True)
            try:
                ts_ns, image = cam.get(timeout=5)
            except TimeoutError:
                print("get image timed out", flush=True)
                continue

            if args.out_dir != "":
                # NOTE(YK) We lose nano seconds precision here
                dt = datetime.fromtimestamp(ts_ns / 1e9)
                path = os.path.join(args.out_dir,
                                    dt.astimezone(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S%z.jpg'))
            else:
                path = "sample.jpg"

            print("writing image", flush=True)
            cv2.imwrite(path, image)
            
            print("uploading image", flush=True)
            plugin.upload_file(path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-stream', dest='stream',
        action='store', default="camera",
        help='ID or name of a stream, e.g. sample')
    parser.add_argument(
        '-out-dir', dest='out_dir',
        action='store', default="",
        help='Path to save images locally in %Y-%m-%dT%H:%M:%S%z.jpg format')
    parser.add_argument(
        '-interval', dest='interval',
        action='store', default=300, type=int,
        help='Inference interval in seconds')
    run(parser.parse_args())
