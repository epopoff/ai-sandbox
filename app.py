import io
import json

from torchvision import models
import torchvision.transforms as transforms
import torch
from PIL import Image
from flask import Flask, jsonify, request

import ssl
ssl._create_default_https_context = ssl._create_unverified_context


app = Flask(__name__)
imagenet_class_index = json.load(open('imagenet_class_index.json'))
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
model = models.resnet50(pretrained=True)
model.eval()



def transform_image(image_bytes):
    trfms = transforms.Compose([transforms.Resize(255),
                                        transforms.CenterCrop(224),
                                        transforms.ToTensor(),
                                        transforms.Normalize(
                                            [0.485, 0.456, 0.406],
                                            [0.229, 0.224, 0.225])])
    image = Image.open(io.BytesIO(image_bytes))
    return trfms(image).unsqueeze(0)


def get_prediction(image_bytes):
    image_bytes
    tensor = transform_image(image_bytes=image_bytes)
    outputs = model.forward(tensor)
    # print(outputs)
    _, y_hat = outputs.max(1)
    import torch.nn.functional as nnf
    prob, _ = nnf.softmax(outputs, dim=1).max(1)
    predicted_idx = str(y_hat.item())

    class_id, class_name = imagenet_class_index[predicted_idx]
    return class_name, prob.item()


@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        file = request.files['file']
        img_bytes = file.read()
        class_name, prob = get_prediction(image_bytes=img_bytes)
        return jsonify({'class_name': class_name, 'probability': prob})


if __name__ == '__main__':
    app.run(host='0.0.0.0')
