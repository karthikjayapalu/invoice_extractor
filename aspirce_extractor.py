
#http://asprise.com/receipt-ocr/blog-github-python-receipt-ocr-api-library-free-example-code-open-source
# View complete code at: https://github.com/Asprise/receipt-ocr/tree/main/python-receipt-ocr
import requests
import json
import os

input_folder="E:\\karthik\\Python_Projects\\invoice_extractor\\input_images\\"
output_folder="E:\\karthik\\Python_Projects\\invoice_extractor\\output_images\\"
print(input_folder)
print(output_folder)
#https://stackoverflow.com/questions/57451177/python3-create-list-of-image-in-a-folder
images = []
def load_images_from_folder(folder):
    # list files in img directory
    files = os.listdir(folder)

    for file in files:
      # make sure file is an image
      if file.endswith(('.jpg', '.png', 'jpeg')):
        img_path = folder + file
        images.append(img_path)
    print("image list:",images)
    return images

print("=== Python Receipt OCR ===")
#loading images from folder
load_images_from_folder(input_folder)
receiptOcrEndpoint = 'https://ocr.asprise.com/api/v1/receipt' # Receipt OCR API endpoint
for imageFile in images:
  # "T3_samp3.png" # // Modify it to use your own file
  data = requests.post(receiptOcrEndpoint, data = { \
    'client_id': 'TEST',        # Use 'TEST' for testing purpose \
    'recognizer': 'auto',       # can be 'US', 'CA', 'JP', 'SG' or 'auto' \
    'ref_no': 'ocr_python_123', # optional caller provided ref code \
    }, \
    files = {"file": open(imageFile, "rb")})

  print(data.text) # result in JSON
  fl_name= os.path.basename(imageFile)
  print(fl_name)
  outFile=output_folder+"".join(fl_name.split('.')[:-1]) + '.json'
  print(outFile)
  # outFile = "".join(imageFile.split('.')[:-1]) + '.json'
  with open(outFile, 'w', encoding='utf-8') as f:
    # json.dump(data.text, f, ensure_ascii=False, indent=4)
    f.write(data.text)
