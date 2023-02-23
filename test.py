import src as src
from src import Formats

video = src.input_option("tests/test.mp4")

dash = video.dash(Formats.hevc())
dash.auto_generate_representations([720, 480])
dash.output("./output/test/dash.mpd")
