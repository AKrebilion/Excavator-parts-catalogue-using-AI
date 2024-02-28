from ultralytics import YOLO
import cv2
import json
import torch
import numpy as np

class YoloV8Detection:
    def __init__(self, model_file):
        self.device = 0 if torch.cuda.is_available() else "cpu"
        if self.device == "cpu":
            print("inferencing with CPU capabilities")
        else:
            print("inferencing with GPU capabilities")
        self.model = YOLO(model_file)

    def Excavator_Detection(self, image, th=0.6, debug=False):
        results = self.model.predict(source=image, show=False, save=False, conf=th, device=self.device)
        prediction_dect = results[0].tojson()
        prediction_dect = json.loads(prediction_dect)
        res_plotted = results[0].plot(conf=True, line_width=10, font_size=12.0, font="Arial", labels=True, boxes=True, masks=True, probs=True)

        

        pre_dect = {}
        if prediction_dect != 0:
            for i in prediction_dect:
                current_label = i["name"]
                                   
                confidence = i["confidence"] * 100
                x = i["segments"]['x']
                x = [int(z) for z in x]
                y = i["segments"]['y']
                y = [int(z) for z in y]
                Main_area_poly = [[xval, yval] for xval, yval in zip(x, y)]
                # Main_area_poly_array = np.array(Main_area_poly)
                if current_label in pre_dect:
                    pre_dect[current_label]["polygon"].append(Main_area_poly)
                    pre_dect[current_label]["confidence"].append(confidence)
                else:
                    pre_dect[current_label] = {"polygon": [Main_area_poly], "confidence": [confidence]}
        
        return pre_dect,res_plotted

        



# obj = YoloV8OjectDetection(r"model\best.pt")
# # file_path=r"D:\samp teest crosstrek"
# # for imag_path in paths.list_images(file_path):
# imag_path = cv2.imread(r"destination\TrainingData\test\images\images (21).jpeg")
# prediction_dect=obj.Excavator_Detection(imag_path)
