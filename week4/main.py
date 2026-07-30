import argparse
import time
from collections import deque
from pathlib import Path

import cv2
import matplotlib.pyplot as plt
import numpy as np

from transform import rotation_matrix_2d, scale_matrix_2d, translate_2d


WINDOW_NAME = "Week 4 - Integrated Pipeline"
MIN_AREA = 500
PLOT_UPDATE_INTERVAL = 3

RED_LOWER_1 = np.array([0, 120, 70])
RED_UPPER_1 = np.array([10, 255, 255])
RED_LOWER_2 = np.array([170, 120, 70])
RED_UPPER_2 = np.array([180, 255, 255])


def preprocess(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    return cv2.Canny(blur, 100, 200)


def create_mask(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    mask1 = cv2.inRange(hsv, RED_LOWER_1, RED_UPPER_1)
    mask2 = cv2.inRange(hsv, RED_LOWER_2, RED_UPPER_2)
    mask = cv2.bitwise_or(mask1, mask2)

    kernel = np.ones((5, 5), np.uint8)
    return cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)


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

    for cx, cy, _, box in objects:
        x, y, w, h = box
        cv2.rectangle(output, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.circle(output, (cx, cy), 5, (0, 0, 255), -1)

    return output


def detect(frame):
    mask = create_mask(frame)
    objects = find_objects(mask)
    return draw_detection(frame, objects), mask, objects


def pixel_to_world(point, image_size, scale=0.01, angle_deg=0.0):
    width, height = image_size
    centered = translate_2d(point, -width / 2, -height / 2)
    scaled = scale_matrix_2d(scale, scale) @ centered
    return rotation_matrix_2d(angle_deg) @ scaled


def calc_fps(times):
    if len(times) == 0:
        return 0
    avg = sum(times) / len(times)
    return 1 / avg if avg > 0 else 0


def draw_status(frame, fps, pixel_point, world_point, angle, scale):
    lines = [
        f"FPS: {fps:.1f}",
        f"angle: {angle:.0f} deg | scale: {scale:.4f}",
    ]

    if pixel_point is not None:
        lines.append(f"pixel: ({pixel_point[0]}, {pixel_point[1]})")
        lines.append(f"world: ({world_point[0]:.2f}, {world_point[1]:.2f})")

    for index, text in enumerate(lines):
        cv2.putText(
            frame,
            text,
            (15, 35 + index * 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2,
        )

    return frame


def combine_frames(frame, edges, mask):
    edge_view = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    mask_view = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    return np.hstack([frame, edge_view, mask_view])


def setup_plot():
    plt.ion()
    figure, axes = plt.subplots(1, 2, figsize=(10, 4))
    figure.canvas.manager.set_window_title("Week 4 - Coordinate History")
    figure.tight_layout()
    plt.show(block=False)
    return figure, axes


def update_plot(figure, axes, pixel_history, world_history, image_size):
    pixel_axis, world_axis = axes
    pixel_axis.clear()
    world_axis.clear()

    if pixel_history:
        pixel_points = np.array(pixel_history)
        pixel_axis.scatter(pixel_points[:, 0], pixel_points[:, 1], c="blue", s=18)

    if world_history:
        world_points = np.array(world_history)
        world_axis.scatter(world_points[:, 0], world_points[:, 1], c="red", s=18)

    width, height = image_size
    pixel_axis.set(
        title="Pixel coordinates",
        xlim=(0, width),
        ylim=(height, 0),
        xlabel="x (px)",
        ylabel="y (px)",
    )
    world_axis.set(title="World coordinates", xlabel="x", ylabel="y")
    world_axis.axhline(0, color="gray", linewidth=0.7)
    world_axis.axvline(0, color="gray", linewidth=0.7)
    world_axis.grid(alpha=0.3)
    world_axis.axis("equal")

    figure.canvas.draw_idle()
    figure.canvas.flush_events()
    plt.pause(0.001)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", help="video file path. empty value uses webcam")
    parser.add_argument("--camera-index", type=int, default=0)
    parser.add_argument("--result-path", default="result_week4.png")
    args = parser.parse_args()

    source = args.source if args.source else args.camera_index
    cap = cv2.VideoCapture(source)

    if not cap.isOpened():
        print("카메라 또는 영상 파일을 열 수 없습니다.")
        return

    print("웹캠 연결 성공")

    fps_times = deque(maxlen=30)
    pixel_history = deque(maxlen=100)
    world_history = deque(maxlen=100)
    result_path = Path(args.result_path)
    angle = 0.0
    scale = 0.01
    fps = 0.0
    frame_count = 0
    figure, axes = setup_plot()

    try:
        while True:
            frame_start = time.time()

            sense_start = time.time()
            ret, frame = cap.read()
            sense_ms = (time.time() - sense_start) * 1000

            if not ret:
                print("더 이상 읽을 프레임이 없습니다.")
                break

            compute_start = time.time()
            height, width = frame.shape[:2]
            edges = preprocess(frame)
            detected_frame, mask, objects = detect(frame)
            pixel_point = None
            world_point = None

            if objects:
                cx, cy, _, _ = objects[0]
                pixel_point = (cx, cy)
                world_point = pixel_to_world(
                    pixel_point,
                    (width, height),
                    scale=scale,
                    angle_deg=angle,
                )
                pixel_history.append(pixel_point)
                world_history.append(world_point)

            compute_ms = (time.time() - compute_start) * 1000

            act_start = time.time()
            detected_frame = draw_status(
                detected_frame,
                fps,
                pixel_point,
                world_point,
                angle,
                scale,
            )
            combined = combine_frames(detected_frame, edges, mask)
            cv2.imshow(WINDOW_NAME, combined)

            if frame_count % PLOT_UPDATE_INTERVAL == 0:
                update_plot(
                    figure,
                    axes,
                    pixel_history,
                    world_history,
                    (width, height),
                )
            frame_count += 1

            key = cv2.waitKey(1) & 0xFF
            act_ms = (time.time() - act_start) * 1000

            fps_times.append(time.time() - frame_start)
            fps = calc_fps(fps_times)
            print(
                f"sense: {sense_ms:.1f}ms | "
                f"compute: {compute_ms:.1f}ms | "
                f"act: {act_ms:.1f}ms | FPS: {fps:.1f}"
            )

            if key == ord("a"):
                angle -= 5
            elif key == ord("d"):
                angle += 5
            elif key in (ord("+"), ord("=")):
                scale *= 1.1
            elif key == ord("-"):
                scale *= 0.9
            elif key == ord("s"):
                cv2.imwrite(str(result_path), combined)
                print(f"저장 완료: {result_path}")
            elif key == ord("q"):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()
        plt.close(figure)


if __name__ == "__main__":
    main()
