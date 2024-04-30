# Video Frame Splitter

This Python project allows you to split a video file into individual image frames.

## Installation

1. Clone the repository:

```bash
git clone https://github.com/userHarpreet/frameSplit.git
```

2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

To split an video file into frames, run the following command:

```bash
python frameSplit.py [--start-time START_TIME] [--end-time END_TIME] [--fps FPS] [--image-type {jpg,png,bmp}] video_path output_dir
```

This will extract all frames from the `video` file and save them as PNG images in the specified output directory.

## Options 

### positional arguments:
  - `video_path`            Path to the input video file
  - `output_dir`            Path to the output directory for saving frames

### optional arguments:
  - `--start-time START_TIME`           Start time in HH:MM:SS format
  - `--end-time END_TIME`               End time in HH:MM:SS format
  - `--fps FPS`                         Specify the frames per second to extract (default: 24)
  - `--image-type {jpg,png,bmp}`        Set the image type for output frames (e.g. jpg, png, bmp)

## Example

```bash
python frameSplit.py ./movie.mkv ./frames --start-time 00:15:00 --end-time 00:20:00 --fps 30 --image-type jpg
```

This will extract frames from 15 minutes to 20 minutes in the `movie.mkv` file at 30 fps, saving them as JPG images in the `./frames` directory.

## Dependencies

- python >=3.6
- opencv-python

## Contributing

Pull requests are welcome! Please open an issue first to discuss any major changes.

## License

[MIT License](LICENSE)
