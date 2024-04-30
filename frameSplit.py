import argparse
import os
import cv2
from collections import deque

SUPPORTED_FORMATS = ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv']  # Add more formats as needed

def extract_frames(video_path, output_dir, start_time=None, end_time=None, fps=24, image_type='jpg'):
    """
    Extracts frames from a video file and saves them as images.

    Args:
        video_path (str): Path to the input video file.
        output_dir (str): Path to the output directory for saving frames.
        start_time (str, optional): Start time in HH:MM:SS format. Defaults to None.
        end_time (str, optional): End time in HH:MM:SS format. Defaults to None.
        fps (float, optional): Frames per second to extract. Defaults to 24.
        image_type (str, optional): Image file extension (e.g. 'jpg', 'png'). Defaults to 'jpg'.
    """
    # Check if the video format is supported
    _, ext = os.path.splitext(video_path)
    if ext.lower() not in SUPPORTED_FORMATS:
        print(f"Error: Unsupported video format '{ext}'. Supported formats: {', '.join(SUPPORTED_FORMATS)}")
        return

    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Open the video file
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error opening video file: {video_path}")
        return

    # Get the original FPS of the video
    video_fps = cap.get(cv2.CAP_PROP_FPS)
    if fps <= 0:
        print("Error: FPS must be a positive value.")
        return

    # Calculate the start and end frame numbers based on the provided start and end times
    start_frame = 0
    end_frame = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    if start_time:
        start_seconds = sum(x * int(t) for x, t in zip([3600, 60, 1], start_time.split(":")))
        start_frame = int(start_seconds * video_fps)

    if end_time:
        end_seconds = sum(x * int(t) for x, t in zip([3600, 60, 1], end_time.split(":")))
        end_frame = int(end_seconds * video_fps)

    # Calculate the frame step based on the desired FPS and the video's FPS
    frame_step_map = {
        (fps == video_fps): 1,  # Process every frame if desired FPS matches video FPS
        (fps > video_fps): max(int(video_fps / fps), 1),  # Round down, but ensure frame_step is at least 1
        (fps < video_fps): int(video_fps / fps) + 1  # Round up to avoid skipping frames
    }
    frame_step = frame_step_map[True]
    frame_out = 0

    # Buffer frames in a deque
    frame_queue = deque()
    for frame_count in range(start_frame, end_frame, frame_step):
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_count)
        ret, frame = cap.read()
        if not ret:
            break
        frame_queue.append((frame_count, frame))

    # Write frames to disk
    for frame_count, frame in frame_queue:
        filename = os.path.join(output_dir, f"frame_{frame_count // frame_step:04d}.{image_type}")
        cv2.imwrite(filename, frame)
        frame_out += 1

    print(f"Total frame output: {frame_out}")

    # Release resources
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description="Extract frames from a video file.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("video_path", help="Path to the input video file")
    parser.add_argument("output_dir", help="Path to the output directory for saving frames")
    parser.add_argument("--start-time", help="Start time in HH:MM:SS format")
    parser.add_argument("--end-time", help="End time in HH:MM:SS format")
    parser.add_argument("--fps", type=float, default=24, help="Frames per second to extract")
    parser.add_argument(
        "--image-type",
        default="jpg",
        choices=["jpg", "png", "bmp"],
        help="Image file extension",
    )

    args = parser.parse_args()

    # Call the extract_frames function with the parsed arguments
    extract_frames(args.video_path, args.output_dir, args.start_time, args.end_time, args.fps, args.image_type)