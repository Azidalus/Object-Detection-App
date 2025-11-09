import supervision as sv
from ultralytics import YOLO
import numpy as np
import subprocess
import os
import cv2

detector = YOLO('yolo11n.pt')
tracker = sv.ByteTrack()
box_annotator = sv.BoxAnnotator()
label_annotator = sv.LabelAnnotator()

def callback(frame: np.ndarray, _: int) -> np.ndarray:
    results = detector(frame)[0]
    detections = sv.Detections.from_ultralytics(results)
    detections = tracker.update_with_detections(detections)

    labels = [
        f"#{tracker_id} {results.names[class_id]}"
        for class_id, tracker_id
        in zip(detections.class_id, detections.tracker_id)
    ]

    annotated_frame = box_annotator.annotate(frame.copy(), 
                                             detections=detections)
    return label_annotator.annotate(annotated_frame, 
                                    detections=detections, 
                                    labels=labels)

def track_video(src_path, trgt_path):
    sv.process_video(
        source_path=src_path,
        target_path=trgt_path,
        callback=callback
    )

def prepare_video_for_streamlit(path: str) -> bytes:
    """
    Re-encodes the video to H.264 (browser-friendly) and returns raw bytes
    that can be passed directly to st.video().
    """
    path_reencoded = path.removesuffix(".mp4") + "_reencoded.mp4"

    # Конвертируем видео в H.264
    subprocess.run(
        ["ffmpeg", "-y", "-i", path, "-vcodec", "libx264", "-pix_fmt", "yuv420p", path_reencoded],
        check=True
    )

    # Переводим видео в байты, т.к. стримлитовский ридер принимает именно их 
    with open(path_reencoded, "rb") as video:
        video_bytes = video.read()

    # Очищаем временный файл
    os.remove(path_reencoded)

    return video_bytes


def prep_video(src_path: str, trgt_path: str):
    cap = cv2.VideoCapture(src_path)
    if not cap.isOpened():
        raise RuntimeError(f"Could not open {src_path}")

    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # 'mp4v' codec is widely browser-compatible
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(trgt_path, fourcc, fps, (width, height))

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        processed = callback(frame)
        writer.write(processed)

    cap.release()
    writer.release()
    cv2.destroyAllWindows()

    return trgt_path