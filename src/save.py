import abc
import os
import shutil
import atexit
import asyncio

from .build_args import command_builder
from .format import Format
from .process import Process
from .utils.utils import mkdir, rm
from .ffprobe import FFProbe

class Save(abc.ABC):
    def __init__(self, media, _format: Format, **options):
        """
        @TODO: add documentation
        """
        atexit.register(self.finish_up)

        self.output_ = ""
        self.key = None
        self.media = media
        self.format = _format
        self.options = options
        self.pipe = None
        self.output_temp = False

    def finish_up(self):
        """
        @TODO: add documentation
        """
        if self.media.input_temp:
            rm(self.media.input)
        if self.output_temp:
            if self.output:
                shutil.move(
                    os.path.dirname(self.output_), os.path.dirname(str(self.output))
                )
            else:
                shutil.rmtree(os.path.dirname(str(self.output_)), ignore_errors=True)

    @abc.abstractmethod
    def set_up(self):
        pass

    def __getattr__(self, name):
        def method(*args, **kwargs):
            if name in ["save", "package"]:
                self.output(*args, **kwargs)
            else:
                raise AttributeError("The object has no attribute {}".format(name))

        return method

    def output(
        self,
        output: str = None,
        run_command: bool = True,
        ffmpeg_bin: str = "ffmpeg",
        monitor: callable = None,
        **options,
    ):
        """
        @TODO: add documentation
        """

        mkdir(os.path.dirname(output))
        self.output_ = output

        self.set_up()

        if run_command:
            self.run(ffmpeg_bin, monitor, **options)

    def probe(self, ffprobe_bin="ffprobe") -> FFProbe:
        """
        @TODO: add documentation
        """
        return FFProbe(self.media.input, ffprobe_bin)

    def _run(self, ffmpeg_bin, monitor: callable = None, **options):
        """
        @TODO: add documentation
        """
        with Process(
            self, command_builder(ffmpeg_bin, self), monitor, **options
        ) as process:
            self.pipe, err = process.run()

    async def async_run(self, ffmpeg_bin, monitor: callable = None, **options):
        """
        @TODO: add documentation
        """
        self._run(ffmpeg_bin, monitor, **options)

    def run(self, ffmpeg_bin, monitor: callable = None, **options):
        """
        @TODO: add documentation
        """
        if async_run := options.pop("async_run", True):
            asyncio.run(self.async_run(ffmpeg_bin, monitor, **options))
        else:
            self._run(ffmpeg_bin, monitor, **options)
