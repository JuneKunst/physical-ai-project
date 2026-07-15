"""Week 1 Assignment: Real-time webcam preprocessing pipeline.

Pipeline:
    webcam/video input -> grayscale -> Gaussian blur -> Canny edges
    -> draw average FPS -> combine original + edge view -> display
    -> quit with 'q'

Run:
    python week1/main.py
    python week1/main.py --source sample_video.mp4
    python week1/main.py --camera-index 1

Keys:
    q: quit
    s: save current combined frame to result.png
"""

from __future__ import annotations

import argparse
import time
from collections import deque
from pathlib import Path
from typing import Deque, Tuple, Union

import cv2
import numpy as np

Frame = np.ndarray
VideoSource = Union[int, str]

DEFAULT_WIDTH = 640
DEFAULT_HEIGHT = 480
DEFAULT_CANNY_LOW = 100
DEFAULT_CANNY_HIGH = 200
FPS_HISTORY_SIZE = 30
WINDOW_NAME = "Week 1 - Original + Edges"


def to_grayscale(frame: Frame) -> Frame:
    """Convert a BGR color frame to a 1-channel grayscale image."""
    return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


def apply_blur(gray: Frame, kernel_size: Tuple[int, int] = (5, 5)) -> Frame:
    """Apply Gaussian blur to reduce noise before edge detection."""
    return cv2.GaussianBlur(gray, kernel_size, 0)


def detect_edges(
    blur: Frame,
    low_threshold: int = DEFAULT_CANNY_LOW,
    high_threshold: int = DEFAULT_CANNY_HIGH,
) -> Frame:
    """Detect edges from a blurred grayscale image using Canny."""
    return cv2.Canny(blur, low_threshold, high_threshold)


def preprocess(frame: Frame) -> tuple[Frame, Frame, Frame]:
    """Run the full preprocessing pipeline and return each stage."""
    gray = to_grayscale(frame)
    blur = apply_blur(gray)
    edges = detect_edges(blur)
    return gray, blur, edges


def calculate_fps(frame_durations: Deque[float]) -> float:
    """Calculate average FPS from recent frame durations."""
    if not frame_durations:
        return 0.0

    average_duration = sum(frame_durations) / len(frame_durations)
    if average_duration <= 0:
        return 0.0

    return 1.0 / average_duration


def draw_fps(frame: Frame, fps: float) -> Frame:
    """Draw FPS text at the top-left of a frame and return the frame."""
    output = frame.copy()
    cv2.putText(
        output,
        f"FPS: {fps:.1f}",
        (15, 35),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.0,
        (0, 255, 0),
        2,
        cv2.LINE_AA,
    )
    return output


def combine_frames(frame: Frame, edges: Frame) -> Frame:
    """Combine BGR original frame and 1-channel edge image side by side."""
    edges_colored = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

    if edges_colored.shape[:2] != frame.shape[:2]:
        edges_colored = cv2.resize(edges_colored, (frame.shape[1], frame.shape[0]))

    return np.hstack((frame, edges_colored))


def parse_source(source: str | None, camera_index: int) -> VideoSource:
    """Return a camera index unless a video file path is provided."""
    if source:
        return source
    return camera_index


def open_capture(source: VideoSource, width: int, height: int) -> cv2.VideoCapture:
    """Open webcam or video file and apply requested capture size."""
    cap = cv2.VideoCapture(source)

    if not cap.isOpened():
        raise RuntimeError(f"웹캠/영상 입력을 열 수 없습니다: {source}")

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    print("웹캠 연결 성공" if isinstance(source, int) else f"영상 파일 연결 성공: {source}")
    return cap


def run_pipeline(args: argparse.Namespace) -> None:
    """Run the real-time preprocessing loop."""
    source = parse_source(args.source, args.camera_index)
    cap = open_capture(source, args.width, args.height)
    frame_durations: Deque[float] = deque(maxlen=FPS_HISTORY_SIZE)
    result_path = Path(args.result_path)

    try:
        while True:
            start_time = time.perf_counter()

            ret, frame = cap.read()
            if not ret:
                print("프레임을 읽을 수 없어 종료합니다.")
                break

            if args.flip:
                frame = cv2.flip(frame, 1)

            _, _, edges = preprocess(frame)

            frame_durations.append(time.perf_counter() - start_time)
            fps = calculate_fps(frame_durations)

            frame_with_fps = draw_fps(frame, fps)
            combined = combine_frames(frame_with_fps, edges)

            cv2.imshow(WINDOW_NAME, combined)

            key = cv2.waitKey(args.wait_ms) & 0xFF
            if key == ord("s"):
                cv2.imwrite(str(result_path), combined)
                print(f"결과 화면 저장: {result_path}")
            if key == ord("q"):
                break

            if args.source and args.limit_video_fps:
                time.sleep(max(0.0, (1.0 / args.limit_video_fps) - (time.perf_counter() - start_time)))
    finally:
        cap.release()
        cv2.destroyAllWindows()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Week 1 realtime video preprocessing pipeline")
    parser.add_argument("--source", help="웹캠 대신 사용할 동영상 파일 경로")
    parser.add_argument("--camera-index", type=int, default=0, help="사용할 카메라 번호")
    parser.add_argument("--width", type=int, default=DEFAULT_WIDTH, help="캡처 너비")
    parser.add_argument("--height", type=int, default=DEFAULT_HEIGHT, help="캡처 높이")
    parser.add_argument("--wait-ms", type=int, default=1, help="cv2.waitKey 대기 시간(ms)")
    parser.add_argument("--flip", action="store_true", help="웹캠 화면 좌우 반전")
    parser.add_argument("--limit-video-fps", type=float, help="동영상 파일 입력 시 재생 FPS 제한")
    parser.add_argument("--result-path", default="result.png", help="s 키로 저장할 결과 이미지 경로")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    run_pipeline(args)


if __name__ == "__main__":
    main()
