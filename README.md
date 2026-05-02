# DASH

A Python tool for generating MPEG-DASH (Dynamic Adaptive Streaming over HTTP) streams from video files. Creates adaptive bitrate streams with multiple resolutions for optimal playback across different network conditions.

## Features

- Generate DASH manifests (`.mpd`) from video files
- Auto-generate multiple resolution representations (e.g., 720p, 480p)
- HLS streaming support
- Real-time transcoding progress monitoring
- Web player integration with Video.js
- Supports H.264 encoding

## Requirements

- Python 3.8+
- FFmpeg (installed and available in PATH)

## Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd DASH
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Ensure FFmpeg is installed:

- **Windows**: Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH
- **macOS**: `brew install ffmpeg`
- **Ubuntu/Debian**: `sudo apt install ffmpeg`

## Usage

### Basic Usage

Transcode a video file to DASH format with auto-generated representations:

```bash
python main.py -i path/to/video.mp4
```

### Options

| Flag | Description | Required | Default |
|------|-------------|----------|---------|
| `-i`, `--input` | Path to the input video file | Yes | - |
| `-o`, `--output` | Output directory for generated files | No | `./out/<video_name>/<video_name>` |

### Example

```bash
python main.py -i ./videos/myvideo.mp4 -o ./output/myvideo
```

This generates:
- DASH manifest (`.mpd`)
- Multiple resolution segments (720p, 480p by default)
- All necessary media chunks for adaptive streaming

### Programmatic Usage

```python
import src
from src import Formats

# Load input video
video = src.input_option("path/to/video.mp4")

# Create DASH stream with H.264 encoding
dash = video.dash(Formats.h264())

# Auto-generate representations at specified resolutions
dash.auto_generate_representations([1080, 720, 480])

# Output with progress monitoring
dash.output("./output/stream", monitor=monitor)
```

## Project Structure

```
DASH/
├── main.py              # Entry point CLI script
├── cron.py              # Scheduled task runner (WIP)
├── requirements.txt     # Python dependencies
├── src/                 # Core library
│   ├── __init__.py      # Module exports
│   ├── input.py         # Video input handling
│   ├── format.py        # Encoding format definitions
│   ├── reperesentation.py  # Stream representation configs
│   ├── streaming.py     # Streaming logic
│   ├── streams.py       # Stream management
│   ├── media.py         # Media processing
│   ├── metadata.py      # Video metadata extraction
│   ├── ffprobe.py       # FFprobe integration
│   ├── process.py       # Process management
│   ├── save.py          # Output file handling
│   ├── build_args.py    # FFmpeg argument builder
│   ├── config/          # Configuration
│   └── utils/           # Utility functions (HLS, general)
├── templates/           # HTML templates
├── out/                 # Generated output directory
├── css/                 # Player stylesheets
├── js/                  # Player scripts
└── index.html           # Test player page
```

## Monitoring

The `monitor` callback provides real-time transcoding progress:

- `per` - Percentage complete (0-100)
- `duration` - Total video duration
- `time_` - Current transcoded time
- `time_left` - Estimated time remaining
- `process` - Subprocess object for control

The default monitor displays a terminal progress bar. Customize it for logging, email notifications, or WebSocket progress broadcasting.

## CI/CD

GitHub Actions runs Pylint on push for Python 3.8, 3.9, and 3.10.

## License

TBD
