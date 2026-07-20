import argparse
import time
from collections import deque
from pathlib import Path

import cv2
import numpy as np


WINDOW_NAME = "Week 2 - Color Detection"
MIN_AREA = 500

# 기본값은 빨간색 물체 인식용 HSV 범위입니다.
RED_LOWER_1 = np.array([0, 120, 70])
RED_UPPER_1 = np.array([10, 255, 255])
RED_LOWER_2 = np.array([170, 120, 70])
RED_UPPER_2 = np.array([180, 255, 255])


def create_mask(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    mask1 = cv2.inRange(hsv, RED_LOWER_1, RED_UPPER_1)
    mask2 = cv2.inRange(hsv, RED_LOWER_2, RED_UPPER_2)
    mask = cv2.bitwise_or(mask1, mask2)

    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    return mask


def find_objects(mask):
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    objects = []
    for contour in contours:
        area = cv2.contourArea(contour)
        if area < MIN_AREA:
            continue

        x, y, w, h = cv2.boundingRect(contour)
        cx = x + w // 2
        cy = y + h // 2
        objects.append((cx, cy, area, (x, y, w, h)))

    objects.sort(key=lambda item: item[2], reverse=True)
    return objects


def draw_detection(frame, objects):
    output = frame.copy()

    for cx, cy, area, box in objects:
        x, y, w, h = box
        cv2.rectangle(output, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.circle(output, (cx, cy), 5, (0, 0, 255), -1)
        cv2.putText(
            output,
            f"({cx}, {cy})",
            (x, max(20, y - 10)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2,
        )

    return output


def detect(frame):
    mask = create_mask(frame)
    objects = find_objects(mask)
    result = draw_detection(frame, objects)

    for cx, cy, area, _ in objects:
        print(f"중심: ({cx}, {cy}) | 면적: {area:.0f}px²")

    return result, mask, objects


def calc_fps(times):
    if len(times) == 0:
        return 0
    avg = sum(times) / len(times)
    return 1 / avg if avg > 0 else 0


def draw_fps(frame, fps):
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


def combine_frames(frame, mask):
    mask_view = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    return np.hstack([frame, mask_view])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", help="video file path. empty value uses webcam")
    parser.add_argument("--camera-index", type=int, default=0)
    parser.add_argument("--result-path", default="result_week2.png")
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

        detected_frame, mask, _ = detect(frame)
        fps_times.append(time.perf_counter() - start)
        fps = calc_fps(fps_times)

        detected_frame = draw_fps(detected_frame, fps)
        combined = combine_frames(detected_frame, mask)
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
