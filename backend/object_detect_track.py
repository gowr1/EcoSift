from ultralytics import YOLO
import supervision as sv

class_list = ['Can', 'HDPE', 'PET_BOTTLE', 'Plastic_wrapper', 'Tetrapak']
START = sv.Point(560,0)
END = sv.Point(560,1200)

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

def video_tracking(path,cls_select):
    cls = [0,0,0,0,0]
    cls_selectIndex=[]
    cls_notSelectIndex = [0,1,2,3,4]
    det=[0,0,0,0,0]
    for i in cls_select:
        cls_selectIndex.append(class_list.index(i))
        cls_notSelectIndex.remove(class_list.index(i))

    for result in model.track(source=path, show=False, stream=True, persist=True, agnostic_nms=True, tracker="bytetrack.yaml", conf=0.5):
        frame = result.orig_img
        detections = sv.Detections.from_yolov8(result)
        if result.boxes.id is not None:
            detections.tracker_id = result.boxes.id.cpu().numpy().astype(int)
        for index in cls_notSelectIndex:
            detections = detections[detections.class_id != index]
        labels=[
                f"{tracker_id} {result.names[class_id]} {confidence:0.2f}"
                for _, confidence, class_id, tracker_id
                in detections
        ]

        for index in cls_selectIndex:
            det[index] = detections[detections.class_id == index]
            cls[index] = classCount(line_Zone[index],det[index],index)

        coord(detections)

        frame = box_annotator.annotate(scene=frame, detections=detections, labels=labels)
        #To make line visible (Only be able to see the count of CAN Class)
        line_zone_annotator.annotate(frame,line_Zone[0])
        yield frame, cls
