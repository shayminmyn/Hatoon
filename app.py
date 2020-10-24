from flask import Flask,  render_template , redirect, make_response, request, send_file
from PIL import Image
import numpy as np
import cv2
import io
import uuid
from model.WhiteBoxModel import WB_Cartoonize
import os
from dropboxAPI import DropBoxAPI

app = Flask(__name__)

app.config.from_object('config.Config')

UPLOAD_DIR = app.config['UPLOAD_DIR']
CARTOON_DIR = app.config['CARTOON_DIR']
DROPBOX_TOKEN = app.config['DROPBOX_TOKEN']

def convert_bytes_to_image(img_bytes):
    
    pil_image = Image.open(io.BytesIO(img_bytes))
    if pil_image.mode=="RGBA":
        image = Image.new("RGB", pil_image.size, (255,255,255))
        image.paste(pil_image, mask=pil_image.split()[3])
    else:
        image = pil_image.convert('RGB')
    
    image = np.array(image)
    
    return image


MODEL = WB_Cartoonize(os.path.abspath(app.config['SAVED_MODEL_PATH']), app.config['GPU'])
DRB = DropBoxAPI(DROPBOX_TOKEN)
@app.route('/',methods=['GET', 'POST'])
@app.route('/cartoonize',methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return render_template('index.html')
    if request.method == 'POST':
        if request.files.get('image'):
            img = request.files.get('image').read()
            image = convert_bytes_to_image(img) 
            img_name = str(uuid.uuid4())
            link = UPLOAD_DIR+img_name+ '.jpg'
            cv2.imwrite(link,cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
            cartoon_image = MODEL.infer(image)
            cartoon_name = img_name + '_cartoon.jpg'
            cartoon_link = CARTOON_DIR + cartoon_name
            cv2.imwrite(cartoon_link,cv2.cvtColor(cartoon_image, cv2.COLOR_RGB2BGR))
            result = DRB.upload(cartoon_link)
        return render_template('index.html',link = link,cartoon_link = result)





if __name__ == '__main__':
    app.run(host=app.config['MAIN_IP'], port=8000, debug=True)