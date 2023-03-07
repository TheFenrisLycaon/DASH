"""
ffs.media
~~~~~~~~~~~~

Media object to build a stream objects
"""
import tempfile
import copy

from .build_args import command_builder
from .format import Format
from .utils.hls_utils import HLSKeyInfoFile, HLSMasterPlaylist
from .utils.utils import rm
from .streaming import Streaming
from .save import Save


class DASH(Streaming):
    def set_up(self):
        pass

    def generate_hls_playlist(self):
        self.options.update({"hls_playlist": 1})


class HLS(Streaming):
    KEY_INFO_FILE_PATH = None
    PERIODIC_RE_KEY_FLAG = "periodic_rekey"
    MASTER_PLAYLIST_IS_SAVED = False

    def set_up(self):
        """
        @TODO: add documentation
        """
        if not HLS.MASTER_PLAYLIST_IS_SAVED:
            self.save_master_playlist()

    def encryption(
        self,
        path: str,
        url: str,
        key_rotation_period: int = 0,
        needle: str = ".ts' for writing",
        length: int = 16,
    ):
        """
        @TODO: add documentation
        """
        with tempfile.NamedTemporaryFile(
            mode="w", suffix="_py_ff_vi_st.tmp", delete=False
        ) as key_info:
            HLS.KEY_INFO_FILE_PATH = key_info.name

        key_info_file = HLSKeyInfoFile(
            HLS.KEY_INFO_FILE_PATH, path, url, key_rotation_period, needle, length
        )
        self.options.update({"hls_key_info_file": str(key_info_file)})

        if key_rotation_period > 0:
            setattr(self, "key_rotation", key_info_file)
            self.flags(HLS.PERIODIC_RE_KEY_FLAG)

    def fragmented_mp4(self):
        """
        @TODO: add documentation
        """
        self.options.update({"hls_segment_type": "fmp4"})

    def save_master_playlist(self, path=None):
        """
        @TODO: add documentation
        """
        if path is not None:
            HLS.MASTER_PLAYLIST_IS_SAVED = True

        HLSMasterPlaylist.generate(self, path)

    def flags(self, *flags: str):
        """
        @TODO: add documentation
        """
        hls_flags = self.options.pop("hls_flags", None)
        hls_flags = (
            f"{hls_flags}+" + "+".join(list(flags))
            if hls_flags is not None
            else "+".join(list(flags))
        )

        self.options.update({"hls_flags": hls_flags})

    def finish_up(self):
        """
        @TODO: add documentation
        """
        if HLS.KEY_INFO_FILE_PATH is not None:
            rm(HLS.KEY_INFO_FILE_PATH)

        super(HLS, self).finish_up()


class Stream2File(Save):
    """
    @TODO: add documentation
    """

    def set_up(self):
        pass


class Media(object):
    def __init__(self, _inputs):
        """
        @TODO: add documentation
        """
        self.inputs = _inputs

        first_input = dict(copy.copy(_inputs.inputs[0]))
        self.input = first_input.get("i")
        self.input_temp = first_input.get("is_tmp", False)

    def hls(self, _format: Format, **hls_options):
        """
        @TODO: add documentation
        """
        return HLS(self, _format, **hls_options)

    def dash(self, _format: Format, **dash_options):
        """
        @TODO: add documentation
        """
        return DASH(self, _format, **dash_options)

    def stream2file(self, _format: Format, **options):
        """
        @TODO: add documentation
        """
        return Stream2File(self, _format, **options)
