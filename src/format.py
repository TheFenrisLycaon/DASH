"""
ffs.media
~~~~~~~~~~~~

Video and audio formats
"""
import abc
from .config.config import *


def verify_codecs(codec, codecs):
    if codec is None:
        return
    elif codec not in codecs:
        ValueError("The codec is not available!")
    else:
        return str(codec)


class Format(abc.ABC):
    """
    Format class that classifies videos into different formats with different default values.
    """

    def __init__(self, video: str, audio: str, **codec_options):
        self.video = video
        self.audio = audio
        self.codec_options = codec_options

    @property
    def all(self) -> dict:
        args = {
            "c:v": self.video,
            "c:a": self.audio,
        }
        args.update(self.get_codec_options())

        return args

    @abc.abstractmethod
    def multiply(self) -> int:
        pass

    @abc.abstractmethod
    def get_codec_options(self) -> dict:
        pass


class H264(Format):
    def __init__(self, video: str = "libx264", audio: str = "aac", **codec_options):
        """
        h.264 format class.
        """
        videos = ["libx264", "h264", "h264_afm", "h264_nvenc"]
        audios = ["copy", "aac", "libvo_aacenc", "libfaac", "libmp3lame", "libfdk_aac"]

        super(H264, self).__init__(
            verify_codecs(video, videos), verify_codecs(audio, audios), **codec_options
        )

    def multiply(self) -> int:
        return MULTIPLY_BY_TWO

    def get_codec_options(self) -> dict:
        """
        set the default value of h264 codec options and update the value with the specified value by user
        see https://ffmpeg.org/ffmpeg-codecs.html#Options-28 for more information about options
        :return: dict
        """
        h264_codec_options = {"bf": 1, "keyint_min": 25, "g": 250, "sc_threshold": 40}

        h264_codec_options.update(self.codec_options)

        return h264_codec_options


class HEVC(Format):
    """
    hevc (h.265) format class.
    """

    def __init__(self, video: str = "libx265", audio: str = "aac", **codec_options):
        videos = ["libx265", "h265"]
        audios = ["copy", "aac", "libvo_aacenc", "libfaac", "libmp3lame", "libfdk_aac"]

        super(HEVC, self).__init__(
            verify_codecs(video, videos), verify_codecs(audio, audios), **codec_options
        )

    def multiply(self) -> int:
        return MULTIPLY_BY_TWO

    def get_codec_options(self) -> dict:
        """
        set the default value of hevc(h265) codec options and update the value with the specified value by user
        see https://ffmpeg.org/ffmpeg-codecs.html#Options-29 for more information about options
        :return: dict
        """
        h265_codec_options = {"keyint_min": 25, "g": 250, "sc_threshold": 40}
        h265_codec_options.update(self.codec_options)
        return h265_codec_options


class Formats:
    @staticmethod
    def h264(video: str = "libx264", audio: str = "aac", **codec_options) -> Format:
        """
        Returns h264 videos from H264 class.
        """
        return H264(video, audio, **codec_options)

    @staticmethod
    def hevc(video: str = "libx265", audio: str = "aac", **codec_options) -> Format:
        """
        Returns h265 videos from HEVC class.
        """
        return HEVC(video, audio, **codec_options)


__all__ = ["Format", "Formats"]
