"""Dash testing script"""

import argparse
import datetime
import sys
import logging

import src
from src import Formats

logging.basicConfig(
    filename="logs/streaming.log",
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s: %(message)s",
)


def monitor(ffmpeg, duration, time_, time_left, process):
    """
    Handling proccess.

    Examples:
    1. Logging or printing ffmpeg command
    logging.info(ffmpeg) or print(ffmpeg)

    2. Handling Process object
    if "something happened":
        process.terminate()

    3. Email someone to inform about the time of finishing process
    if time_left > 3600 and not already_send:
        # if it takes more than one hour and you have not emailed them already
        ready_time = time_left + time.time()
        Email.send(
            email='someone@somedomain.com',
            subject='Your video will be ready by %s' % datetime.timedelta(seconds=ready_time),
            message='Your video takes more than %s hour(s) ...' % round(time_left / 3600)
        )
       already_send = True

    4. Create a socket connection and show a progress bar(or other parameters) to your users
    Socket.broadcast(
        address=127.0.0.1
        port=5050
        data={
            percentage = per,
            time_left = datetime.timedelta(seconds=int(time_left))
        }
    )

    :param ffmpeg: ffmpeg command line
    :param duration: duration of the video
    :param time_: current time of transcoded video
    :param time_left: seconds left to finish the video process
    :param process: subprocess object
    :return: None
    """
    per: int = round(time_ / duration * 100)
    sys.stdout.write(
        "\rTranscoding...(%s%%) [%s%s] %s"
        % (
            per,
            "#" * per,
            "-" * (100 - per),
            datetime.timedelta(seconds=int(time_left)),
        )
    )
    sys.stdout.flush()


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-i", "--input", required=True, help="The path to the video file (required)."
    )

    args = parser.parse_args()
    video_name = args.input.split("/")[-1]

    parser.add_argument(
        "-o",
        "--output",
        default=f"./out/{video_name.split('.')[0]}/{video_name}", # TODO : Add path to VM video source directory.
        help="The output to write files.",
    )

    args = parser.parse_args()

    video = src.input_option(args.input)

    dash = video.dash(Formats.h264())
    dash.auto_generate_representations([720, 480])

    dash.output(args.output, monitor=monitor)


if __name__ == "__main__":
    sys.exit(main())
