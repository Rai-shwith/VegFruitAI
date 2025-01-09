from fastapi import FastAPI, UploadFile, Response
from fastapi.middleware.cors import CORSMiddleware
from keras._tf_keras.keras.utils import load_img, img_to_array
import tensorflow as tf
import os
import numpy as np
from fastapi.staticfiles import StaticFiles
# Paths to datasets and image
DATA_TRAIN_PATH = os.path.join(current_dir,"Fruits_Vegetables","train")

image_width = 180
image_height = 180

items = os.listdir(DATA_TRAIN_PATH)
data_cat = [item for item in items if os.path.isdir(os.path.join(DATA_TRAIN_PATH, item))]

# Load the model from the specified path
model_path = "fruits_vegetables_model.keras"  
model = tf.keras.models.load_model(model_path)



def predict_image(image_path):
    try:
        image= load_img(image_path,target_size=(image_width,image_height)) 
        img_arr = img_to_array(image)
        img_batch = tf.expand_dims(img_arr,0)
        predict = model.predict(img_batch)
        DataScore = tf.nn.softmax(predict)
        score = np.max(DataScore)*100
        prediction = data_cat[np.argmax(DataScore)]
        print(f"{prediction} [{score}]")
        return (prediction,float(score))
    except Exception as e:
        print(f"Error making prediction: {e}")
        return None, None
    
    
def delete_file(file_path):
    try:
        os.remove(file_path)
        print(f"File {file_path} deleted successfully.")
    except FileNotFoundError:
        print(f"File {file_path} not found.")
    except PermissionError:
        print(f"Permission denied to delete file {file_path}.")



app = FastAPI()



# # Configure CORS
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Allow all origins. Replace with specific origins for more security.
#     allow_credentials=True,
#     allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
#     allow_headers=["*"],  # Allow all headers
# )

# Mount the static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def read_root():
    return Response(content="index.html", media_type="text/html", status_code=302, headers={"Location": "/static/index.html"})

@app.post("/predict/")
async def predict(file: UploadFile):
    image_path = f"temp_{file.filename}"
    
    with open(image_path, "wb") as f:
        f.write(await file.read())

    (prediction,score) = predict_image(image_path)
    delete_file(image_path)
    return {"prediction": prediction,"score":score}

