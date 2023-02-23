"""
ffs.build_args
~~~~~~~~~~~~

Build a command for the FFmpeg
"""
import sys

from .utils.utils import cnv_options_to_args, get_path_info, clean_args
from .config.config import *


def stream_to_file(stream_to_file):
    """
    Streams the incoming encoded video stream to a file
    """
    args = stream_to_file.format.all
    args.update({"c": "copy"})
    args.update(stream_to_file.options)

    return cnv_options_to_args(args) + [stream_to_file.output_]


def get_audio_bitrate(rep, index: int = None):
    """
    Fetches audio bitrate from video
    """
    if rep.bitrate.audio_ is not None and rep.bitrate.audio_ != 0:
        opt = "b:a" if index is None else f"b:a:{index}"
        return {opt: rep.bitrate.audio}

    return {}


def getdash_stream(key, rep):
    """
    Fetches DASH stream
    """
    args = {
        "map": 0,
        f"s:v:{str(key)}": rep.size,
        f"b:v:{str(key)}": rep.bitrate.calc_video(),
    }

    args.update(get_audio_bitrate(rep, key))
    args.update(rep.options)

    return cnv_options_to_args(args)


def dash(dash):
    """
    Main DASH function.
    """
    dirname, name = get_path_info(dash.output)
    args = dash.format.all
    args.update(
        {
            "use_timeline": USE_TIMELINE,
            "use_template": USE_TEMPLATE,
            "init_seg_name": "{}_init_$RepresentationID$.$ext$".format(name),
            "media_seg_name": "{}_chunk_$RepresentationID$_$Number%05d$.$ext$".format(
                name
            ),
            "f": "dash",
        }
    )
    args.update(dash.options)
    args = cnv_options_to_args(args)

    for key, rep in enumerate(dash.reps):
        args += getdash_stream(key, rep)

    return args + ["-strict", "-2", "{}/{}.mpd".format(dirname, name)]


def hls_seg_ext(hls):
    """
    Fetches HLS segment extention
    """
    return "m4s" if hls.options.get("hls_segment_type", "") == "fmp4" else "ts"


def gethls_stream(hls, rep, dirname, name):
    """
    Fetches HLS stream.
    """
    args = hls.format.all
    args.update(
        {
            "hls_list_size": HLS_LIST_SIZE,
            "hls_time": HLS_TIME,
            "hls_allow_cache": HLS_ALLOW_CACHE,
            "hls_segment_filename": "{}/{}_{}p_%04d.{}".format(
                dirname, name, rep.size.height, hls_seg_ext(hls)
            ),
            "hls_fmp4_init_filename": "{}_{}p_init.mp4".format(name, rep.size.height),
            "s:v": rep.size,
            "b:v": rep.bitrate.calc_video(),
        }
    )
    args.update(get_audio_bitrate(rep))
    args.update(rep.options)
    args.update({"strict": "-2"})
    args.update(hls.options)

    return cnv_options_to_args(args) + [
        "{}/{}_{}p.m3u8".format(dirname, name, str(rep.size.height))
    ]


def hls(hls):
    """
    Main HLS function
    """
    dirname, name = get_path_info(hls.output)
    streams = []
    for key, rep in enumerate(hls.reps):
        if key > 0:
            streams += input_args(hls)
        streams += gethls_stream(hls, rep, dirname, name)

    return streams


def stream_args(media):
    """
    Arguments to control stream
    """
    return getattr(sys.modules[__name__], "_%s" % type(media).__name__.lower())(media)


def input_args(media):
    inputs = []
    for key, input in enumerate(media.media.inputs.inputs):
        input = dict(input)
        input.pop("is_tmp", None)
        if key > 0:
            input.pop("y", None)
        inputs += cnv_options_to_args(input)

    return inputs


def command_builder(ffmpeg_bin: str, media):
    """
    Builds the command.
    """
    return " ".join(clean_args([ffmpeg_bin] + input_args(media) + stream_args(media)))
