import cv2

def video_to_frames(video_path, frames_per_second=2):
    frame_list=[]
    cap = cv2.VideoCapture(video_path)

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

video_path = r"c:\Users\Jsn - Laptop SSD\Downloads\final\DJI_20231019_120716_021_video.mp4"
video_to_frames(video_path)
