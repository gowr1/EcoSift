# install dependencies
# pip install -r requirements.txt

from ultralytics import YOLO
import supervision as sv
import cv2
import numpy as np


START = sv.Point(200,0)
END = sv.Point(200,640)

model=YOLO('best.pt')
line_Zone = []
for i in range(6):
    line_Zone.append(sv.LineZone(start=START, end=END))
print(type(line_Zone))
line_zone_annotator = sv.LineZoneAnnotator(
    thickness=2,
    text_thickness=1,
    text_scale=0.5
)

box_annotator = sv.BoxAnnotator(
    thickness=2,
    text_thickness=1,
    text_scale=0.5
)
cls = [0,0,0,0,0,0]

out=cv2.VideoWriter('output.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 20, (640,640))

def classCount(line_zone,det):
    line_zone.trigger(detections = det)
    return line_zone.out_count

def coord(detections):
    for xyxy, _, _, tracker_id in detections:
        print(f"{tracker_id} {xyxy}")

def main():
    for result in model.track(source='tracker.mp4', show=False, stream=True, persist=True, agnostic_nms=True, tracker="botsort.yaml"):
        frame = result.orig_img
        detections = sv.Detections.from_yolov8(result)
        # print(result.boxes.id)
        if result.boxes.id is not None:
            detections.tracker_id = result.boxes.id.cpu().numpy().astype(int)
        labels=[
                f"{tracker_id} {result.names[class_id]} {confidence:0.2f}"
                for _, confidence, class_id, tracker_id
                in detections
        ]

        coord(detections)

        det0 = detections[detections.class_id == 0]
        det1 = detections[detections.class_id == 1]
        det2 = detections[detections.class_id == 2]
        det3 = detections[detections.class_id == 3]
        det4 = detections[detections.class_id == 4]
        det5 = detections[detections.class_id == 5]
        
        cls[0] = classCount(line_Zone[0],det0)
        cls[1] = classCount(line_Zone[1],det1)
        cls[2] = classCount(line_Zone[2],det2)
        cls[3] = classCount(line_Zone[3],det3)
        cls[4] = classCount(line_Zone[4],det4)
        cls[5] = classCount(line_Zone[5],det5)

        frame = box_annotator.annotate(scene=frame, detections=detections, labels=labels)
        out.write(frame)
        cv2.imshow('track',frame)
        if(cv2.waitKey(30) == 27):
            break
    print("Final count of each class = ",cls)
    out.release()
    cv2.destroyAllWindows()
    

if __name__ == "__main__":
    main()