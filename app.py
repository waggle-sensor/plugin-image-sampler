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

import cv2

import waggle.plugin as plugin
from waggle.data import open_data_source

plugin.init()


def run(args):
    print("Image sample starts...")
    os.makedirs(args.out_dir, exist_ok=True)

    with open_data_source(args.stream) as cam:
        while True:
            try:
                ts_ns, image = cam.get(timeout=5)
                if args.out_dir != "":
                    # We lose nano seconds precision here
                    dt = datetime.fromtimestamp(ts_ns / 10e8)
                    filename = dt.astimezone(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S%z')
                    cv2.imwrite(filename, image)
                else:
                    cv2.imwrite('/tmp/sample.jpg', image)
                    plugin.upload_file('/tmp/sample.jpg')
            except TimeoutError:
                pass
            time.sleep(args.interval)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-stream', dest='stream',
        action='store', default="camera"
        help='ID or name of a stream, e.g. sample')
    parser.add_argument(
        '-out-dir', dest='out_dir',
        action='store', default="",
        help='Path to save images locally in %Y-%m-%dT%H:%M:%S%z.jpg format')
    parser.add_argument(
        '-interval', dest='interval',
        action='store', default=60, type=int,
        help='Inference interval in seconds')
    run(parser.parse_args())
