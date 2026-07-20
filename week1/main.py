import argparse
import time
from collections import deque
from pathlib import Path

import cv2
import numpy as np


WINDOW_NAME = "Week 1 - Camera Preprocessing"


def preprocess(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blur, 100, 200)
    return gray, blur, edges


def calc_fps(times):
    if len(times) == 0:
        return 0
    avg = sum(times) / len(times)
    return 1 / avg if avg > 0 else 0


def put_fps(frame, fps):
    cv2.putText(
        frame,
        f"FPS: {fps:.1f}",
        (15, 35),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2,
    )
    return frame


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", help="video file path. empty value uses webcam")
    parser.add_argument("--camera-index", type=int, default=0)
    parser.add_argument("--result-path", default="result.png")
    args = parser.parse_args()

    source = args.source if args.source else args.camera_index
    cap = cv2.VideoCapture(source)

    if not cap.isOpened():
        print("카메라 또는 영상 파일을 열 수 없습니다.")
        return

    fps_times = deque(maxlen=30)
    result_path = Path(args.result_path)

    while True:
        start = time.perf_counter()
        ret, frame = cap.read()

        if not ret:
            print("더 이상 읽을 프레임이 없습니다.")
            break

        _, _, edges = preprocess(frame)
        fps_times.append(time.perf_counter() - start)
        fps = calc_fps(fps_times)

        edge_view = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        original = put_fps(frame.copy(), fps)
        combined = np.hstack([original, edge_view])

        cv2.imshow(WINDOW_NAME, combined)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("s"):
            cv2.imwrite(str(result_path), combined)
            print(f"저장 완료: {result_path}")
        elif key == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
