"""
ffs.ffprobe
~~~~~~~~~~~~
"""

import json
import logging
import subprocess

from .metadata import Size, Bitrate
from .streams import Streams


class FFProbe:
    def __init__(self, filename, cmd="ffprobe"):
        """
        @TODO: add documentation
        """
        commands = [cmd, "-show_format", "-show_streams", "-of", "json", filename]
        logging.info("ffprobe running command: {}".format(" ".join(commands)))
        process = subprocess.Popen(
            commands, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
        )
        self.out, err = process.communicate()
        if process.returncode != 0:
            logging.error(str(self.out) + str(err))
            raise RuntimeError("ffprobe", self.out, err)
        logging.info("ffprobe executed command successfully!")

    def streams(self):
        """
        @TODO: add documentation
        """
        return Streams(json.loads(self.out.decode("utf-8"))["streams"])

    def format(self):
        """
        @TODO: add documentation
        """
        return json.loads(self.out.decode("utf-8"))["format"]

    def all(self):
        """
        @TODO: add documentation
        """
        return json.loads(self.out.decode("utf-8"))

    def save_as_json(self, path):
        """
        @TODO: add documentation
        """
        with open(path, "w", encoding="utf-8") as probe:
            probe.write(self.out.decode("utf-8"))

    @property
    def video_size(self) -> Size:
        """
        @TODO: add documentation
        """
        width = int(self.streams().video().get("width", 0))
        height = int(self.streams().video().get("height", 0))

        if width == 0 or height == 0:
            raise RuntimeError("It could not determine the value of width/height")

        return Size(width, height)

    @property
    def bitrate(self, _type: str = "k") -> Bitrate:
        """
        @TODO: add documentation
        """
        overall = int(self.format().get("bit_rate", 0))
        video = int(self.streams().video().get("bit_rate", 0))
        audio = int(self.streams().audio().get("bit_rate", 0))

        if overall == 0:
            raise RuntimeError("It could not determine the value of bitrate")

        return Bitrate(video, audio, overall, type=_type)


__all__ = ["FFProbe"]
