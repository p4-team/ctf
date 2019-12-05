from flask import Flask, request, redirect
from imageai.Prediction import ImagePrediction
import numpy as np
from PIL import Image
import os

app = Flask(__name__)


# Heard that these kind of models are vulnerable to adversarial attacks
prediction = ImagePrediction()
prediction.setModelTypeAsResNet()
prediction.setModelPath("resnet50_weights_tf_dim_ordering_tf_kernels.h5")
prediction.loadModel()

BASE_IMAGE = np.asarray(Image.open("car.jpg"))

def normalize(arr):
    rng = arr.max()-arr.min()
    amin = arr.min()
    return (arr-amin)/rng


def diff(arr1, arr2):
    arr1 = normalize(arr1)
    arr2 = normalize(arr2)
    distance = arr1 - arr2
    return np.max(np.sum(np.square(distance).reshape(arr1.shape[0], -1), axis=1))



@app.route('/task/upload/', methods=['POST',])
def hello_world():
    answer = {
        "status": "fail to recognize image"
    }
    if request.method == 'POST':
        f = request.files['file']
        I = np.asarray(Image.open(f))
        if I.shape != (224,224, 3):
            return redirect(os.getenv("base_url", "http://0.0.0.0:8000") + "/fail.html")
        if diff(I, BASE_IMAGE) > 2:
            return redirect(os.getenv("base_url","http://0.0.0.0:8000" ) + "/fail.html")
        predictions, percentage_probabilities = prediction.predictImage(I, result_count=1, input_type="array")
        answer['classification_result'] = predictions[0]
        if answer['classification_result'] == 'racer':
            return {"flag": os.getenv("FLAG", "tutbudetflag")}
    return redirect(os.getenv("base_url", "http://0.0.0.0:8000" ) + "/sportscar.html")


if __name__ == '__main__':
    app.run("0.0.0.0", 1488)