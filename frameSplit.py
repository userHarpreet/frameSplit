import argparse
import os
import cv2


def extract_frames(video_path, output_dir, start_time=None, end_time=None, fps=24, image_type='jpg'):
    """
    Extracts frames from a video file and saves them as images.

    Args:
        video_path (str): Path to the input video file.
        output_dir (str): Path to the output directory for saving frames.
        start_time (str, optional): Start time in HH:MM:SS format. Defaults to None.
        end_time (str, optional): End time in HH:MM:SS format. Defaults to None.
        fps (float, optional): Frames per second to extract. Defaults to None (original video fps).
        image_type (str, optional): Image file extension (e.g. 'jpg', 'png'). Defaults to 'jpg'.
    """
    os.makedirs(output_dir, exist_ok=True)

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print(f"Error opening video file: {video_path}")
        return

    if start_time:
        start_seconds = sum(x * int(t) for x, t in zip([3600, 60, 1], start_time.split(":")))
        cap.set(cv2.CAP_PROP_POS_MSEC, start_seconds * 1000)

    if end_time:
        end_seconds = sum(x * int(t) for x, t in zip([3600, 60, 1], end_time.split(":")))

    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if end_time and cap.get(cv2.CAP_PROP_POS_MSEC) / 1000 >= end_seconds:
            break

        filename = os.path.join(output_dir, f"frame_{frame_count:04d}.{image_type}")
        cv2.imwrite(filename, frame)
        frame_count += 1

        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract frames from a video file.")
    parser.add_argument("video_path", help="Path to the input video file")
    parser.add_argument("output_dir", help="Path to the output directory for saving frames")
    parser.add_argument("--start-time", help="Start time in HH:MM:SS format")
    parser.add_argument("--end-time", help="End time in HH:MM:SS format")
    parser.add_argument("--fps", type=float, help="Frames per second to extract")
    parser.add_argument("--image-type", default="jpg", choices=["jpg", "png", "bmp"], help="Image file extension")

    args = parser.parse_args()

    extract_frames(args.video_path, args.output_dir, args.start_time, args.end_time, args.fps, args.image_type)