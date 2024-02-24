from ultralytics import YOLO
import supervision as sv

class_list = ['Can', 'HDPE', 'PET_BOTTLE', 'Plastic_wrapper', 'Tetrapak']
START = sv.Point(160,0)
END = sv.Point(160,640)

model = YOLO('detect-model\\best.pt')
line_Zone = []
for i in range(5):
    line_Zone.append(sv.LineZone(start=START, end=END))
    
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

def classCount(line_zone,det,id):
    line_zone.trigger(detections = det)
    print(f"Count of {class_list[id]}: {line_zone.out_count}")
    return line_zone.out_count

def coord(detections):
    for xyxy, _, class_id, tracker_id in detections:
        print(f"{class_list[class_id]} {tracker_id} {xyxy}")

def video_tracking(path):
    cls = [0,0,0,0,0,0]
    for result in model.track(source=path, show=False, stream=True, persist=True, agnostic_nms=True, tracker="botsort.yaml"):
        frame = result.orig_img
        detections = sv.Detections.from_yolov8(result)
        if result.boxes.id is not None:
            detections.tracker_id = result.boxes.id.cpu().numpy().astype(int)
        labels=[
                f"{tracker_id} {result.names[class_id]} {confidence:0.2f}"
                for _, confidence, class_id, tracker_id
                in detections
        ]

        det0 = detections[detections.class_id == 0]
        det1 = detections[detections.class_id == 1]
        det2 = detections[detections.class_id == 2]
        det3 = detections[detections.class_id == 3]
        det4 = detections[detections.class_id == 4]
        
        cls[0] = classCount(line_Zone[0],det0,0)
        cls[1] = classCount(line_Zone[1],det1,1)
        cls[2] = classCount(line_Zone[2],det2,2)
        cls[3] = classCount(line_Zone[3],det3,3)
        cls[4] = classCount(line_Zone[4],det4,4)

        coord(detections)

        frame = box_annotator.annotate(scene=frame, detections=detections, labels=labels)
        #To make line visible (Only be able to see the count of CAN Class)
        #line_zone_annotator.annotate(frame,line_Zone[0])
        yield frame, cls
