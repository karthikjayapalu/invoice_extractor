import torch
import json, cv2, pytesseract
from my_data import VOCAB, color_print
from my_model import MyModel0
from my_utils import pred_to_dict, preprocess
import requests
import os

pytesseract.pytesseract.tesseract_cmd = r'E:\Programfiles\Tesseract-OCR\tesseract.exe'

def inference(text):
    text[0] = preprocess(text[0])
    device = torch.device("cpu")
    hidden_size=256
    model = MyModel0(len(VOCAB), 16, hidden_size).to(device)
    model.load_state_dict(torch.load("model.pth", map_location=torch.device('cpu')))

    #text = ["shubham bisht, something happens"]
    text_tensor = torch.zeros(len(text[0]), 1, dtype=torch.long)
    text_tensor[:, 0] = torch.LongTensor([VOCAB.find(c) for c in text[0].upper()])
    # print(text_tensor)
    inp = text_tensor.to(device)

    oupt = model(inp)
    prob = torch.nn.functional.softmax(oupt, dim=2)
    prob, pred = torch.max(prob, dim=2)

    color_print(text[0], pred)
    json = pred_to_dict(text[0], pred, prob)
    print("\n###########################")
    print(json)
    return json

def tesseract_img(imgcv):
    text = pytesseract.image_to_string(imgcv,config="--psm 1") #default 3
    #1    Automatic page segmentation with OSD.
    #3    Fully automatic page segmentation, but no OSD. (Default)
    return inference([text])

def main(path_to_image):
    # return {'Company':'McD', 'Address':'badlapur', 'Date':'05/6/2020', 'Items':'burgers, drinks, etc.', 'Amount':'550'}
    imgcv = cv2.imread(path_to_image)
    json = tesseract_img(imgcv)
    return json

def load_images_from_folder(folder):
    # list files in img directory
    files = os.listdir(folder)

    for file in files:
        # make sure file is an image
        if file.endswith(('.jpg', '.png', 'jpeg')):
            img_path = folder + file
            images.append(img_path)
    # print("image list:", images)
    return images
if __name__ == "__main__":
    dirname = os.getcwd()
    input_folder = dirname+"\\input_images\\"
    output_folder = dirname+"\\output_jsons\\"
    # https://stackoverflow.com/questions/57451177/python3-create-list-of-image-in-a-folder
    images = []
    # print("=== Python Receipt OCR ===")
    # loading images from folder
    load_images_from_folder(input_folder)
    for imageFile in images:

        json_fl = main(imageFile)
        # print(json_fl)  # result in JSON
        fl_name = os.path.basename(imageFile)
        # print(fl_name)
        outFile = output_folder + "".join(fl_name.split('.')[:-1]) + '.json'
        # print(outFile)
        # outFile = "".join(imageFile.split('.')[:-1]) + '.json'
        with open(outFile, 'w', encoding='utf-8') as f:
            # json.dump(data.text, f, ensure_ascii=False, indent=4)
            json.dump(json_fl,f)

