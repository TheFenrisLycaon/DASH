"""
ffs.Streams
~~~~~~~~~~~
"""


class Streams:
    def __init__(self, streams):
        self.streams = streams

    def video(self, ignore_error=True):
        """
        Returns video stream
        """
        return self.get_stream("video", ignore_error)

    def audio(self, ignore_error=True):
        """
        Returns audio stream
        """
        return self.get_stream("audio", ignore_error)

    def first_stream(self):
        """
        Returns default stream
        """
        return self.streams[0]

    def all(self):
        """
        Returns all streams
        """
        return self.streams

    def videos(self):
        """
        Returns all video streams
        """
        return self._get_streams("video")

    def audios(self):
        """
        Returns all audio streams
        """
        return self._get_streams("audio")

    def get_stream(self, media, ignore_error):
        """
        Returns the given queried stream
        """
        media_attr = next(
            (stream for stream in self.streams if stream["codec_type"] == media), None
        )
        if media_attr is None and not ignore_error:
            raise ValueError("No {} stream found".format(str(media)))
        return media_attr if media_attr is not None else {}

    def get_streams(self, media):
        """
        Returns all streams
        """
        for stream in self.streams:
            if stream["codec_type"] == media:
                yield stream


__all__ = ["Streams"]
