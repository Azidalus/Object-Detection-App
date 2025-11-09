import supervision as sv
from ultralytics import YOLO
import numpy as np


tracker = sv.ByteTrack()
detector = YOLO("yolo11m.pt")
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
        source_path="Crows.mp4",
        target_path="Crows yolo11 superv.mp4",
        callback=callback
    )