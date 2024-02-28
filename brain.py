import base64
from yolov8_inferencecode import *

Exc_model = YoloV8Detection(r"best.pt")


def video_to_frames(video, frames_per_second=1):
    frame_list=[]
    cap = cv2.VideoCapture(video)

    # Check if the video opened successfully
    if not cap.isOpened():
        print("Error: Couldn't open the video file.")
        return []

    # Get video properties
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Calculate frame skip based on desired frames per second
    frame_skip = int(fps // frames_per_second)
    # Read and save frames with the calculated frame skip
    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame_count += 1
        # Skip frames based on the calculated interval
        if frame_count % frame_skip != 0:
            continue
        frame_list.append(frame)
    cap.release()

    return frame_list



def Excavator_processing(detection_det,org_im):
    
    ROI_Extraction={}
    for current_label in detection_det:
        polygon=detection_det[current_label]["polygon"][0]
        confidence=detection_det[current_label]["confidence"][0]

        mask = np.zeros_like(org_im)
        points = np.array(polygon, dtype=np.int32)
        points = points.reshape((-1, 1, 2))
        cv2.fillPoly(mask, [points], (255, 255, 255))
        result = cv2.bitwise_and(org_im, mask)
        ROI_Extraction[current_label]={"image":result,"accuracy":confidence}
    return ROI_Extraction

def ProcessRequest(video):
    frames_list=video_to_frames(video)
    
    final_result={"Message":"Parts Detected","status":200,"org_video":"","Result":""}

    if len(frames_list) != 0:
        result={}
        i=1
        for each_frame in frames_list:
            each_frame_result={"detected_object_count":0,"org_img":"","detection_result":"","plotted_image":""}
            pre_dect,res_plotted = Exc_model.Excavator_Detection(each_frame)
            if len(pre_dect) !=0:
                each_frame_result["detected_object_count"]=len(pre_dect)
                each_frame_result["detection_result"]=pre_dect


                _, each_encoded_image = cv2.imencode('.jpg', each_frame)  # You can change the format if needed
                each_frame_base64 = base64.b64encode(each_encoded_image.tobytes()).decode('utf-8')
                each_frame_result["org_img"]=[each_frame_base64]

                _, res_plotted_encoded_image = cv2.imencode('.jpg', res_plotted)  # You can change the format if needed
                res_plotted_base64 = base64.b64encode(res_plotted_encoded_image.tobytes()).decode('utf-8')
                each_frame_result["plotted_image"]=[res_plotted_base64]

            result[i]=each_frame_result
            i+=1
        final_result["Result"]=result
        
        with open(video, 'rb') as video_file:
            # Read the binary data
            binary_data = video_file.read()

        # Encode the binary data to Base64
        base64_data = base64.b64encode(binary_data).decode('utf-8')

        final_result["org_video"]=[base64_data]
    else:
        final_result["Message"]="No video found"
        final_result["status"]=202

    
    return final_result
