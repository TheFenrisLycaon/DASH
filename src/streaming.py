import abc

from .build_args import command_builder
from .format import Format
from .reperesentation import Representation, AutoRep
from .save import Save


class Streaming(Save, abc.ABC):
    def __init__(self, media, _format: Format, **options):
        """
        @TODO: add documentation
        """
        self.reps = list
        super(Streaming, self).__init__(media, _format, **options)

    def representations(self, *reps: Representation):
        self.reps = list(reps)

    def auto_generate_representations(
        self,
        heights=None,
        bitrate=None,
        ffprobe_bin="ffprobe",
        include_original=True,
        ascending_sort=False,
    ):
        """
        @TODO: add documentation
        """
        probe = self.probe(ffprobe_bin)
        self.reps = AutoRep(
            probe.video_size,
            probe.bitrate,
            self.format,
            heights,
            bitrate,
            include_original,
        )

        if ascending_sort:
            self.reps = sorted(self.reps, key=lambda rep: rep.bitrate.overall_)

    def add_filter(self, *_filter: str):
        """
        @TODO: add documentation
        """
        _filters = self.options.pop("filter_complex", None)
        _filters = (
            f"{_filters}," + ",".join(list(_filter))
            if _filters is not None
            else ",".join(list(_filter))
        )

        self.options.update({"filter_complex": _filters})

    def watermarking(self, path, _filter="overlay=10:10"):
        """
        @TODO: add documentation
        """
        self.media.inputs.input(path)
        self.add_filter(_filter)
