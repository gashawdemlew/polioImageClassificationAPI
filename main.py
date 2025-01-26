from fastapi import FastAPI, Form, Depends
import uvicorn
import os
import tempfile
import requests
from pydantic import BaseModel,ValidationError
# from PIL import Image

from fastapi import File, UploadFile, HTTPException
from gradio_client import Client, file, handle_file

app = FastAPI(
    title="Polio image classification",
    version="1.0.0",
)

# Allowed image extensions
ALLOWED_EXTENSIONS = {".jpg", ".jpeg"}

class iPayload(BaseModel):
    epid_number: str

def is_file_extension_allowed(filename: str) -> bool:
    return filename.lower().endswith(tuple(ALLOWED_EXTENSIONS))

# async def save_uploaded_image(uploaded_image: UploadFile) -> str:
#     """Saves the image to the specified path and returns the save path."""
#     try:
#         contents = await uploaded_image.read()
#         filename = f"{uploaded_image.filename}"
#         save_path = os.path.join(os.getcwd(), filename)
        
#         with open(save_path, "wb") as f:
#             f.write(contents) 

#         return save_path

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error saving image: {e}")

async def save_uploaded_image(uploaded_image: UploadFile) -> str:
    """Saves the image to a temporary path and returns the save path."""
    try:
        contents = await uploaded_image.read()
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
            temp_file.write(contents)
            return temp_file.name  # Returns the path of the temporary file
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving image: {e}")

def hugging_face_api_call(image_path):    
    client = Client("gashudemman/polioImageClassification")
    result = client.predict(
        #img=file(image_path),
        image=handle_file(image_path),
        api_name="/predict"
    )
    
    return result

@app.get("/")
async def start_root():
    msg = {"Message": "Polio image classification"}
    return msg

@app.post("/polio_classification")
async def predict_polio(
    inputData: iPayload = Depends(),
    input_image: UploadFile = File(...)):
    try:
        if not is_file_extension_allowed(input_image.filename):
            return {"response": "Only .jpg images are supported"}
        
        # Save the uploaded image
        save_path = await save_uploaded_image(input_image)
        
        print(save_path)
        
        # Call the Hugging Face API
        predicted_value = hugging_face_api_call(save_path)
        
        print(predicted_value)
        
        polio_suspected = "not-suspected"
        message = ""
        confidence = 0.0
        if int(predicted_value[0]["label"]) == 0:
            polio_suspected = "suspected"
            confidence = float(predicted_value[1]) * 100
            message = f"The case is polio suspected with a confidence of {confidence}"
        else:
            polio_suspected = "not-suspected"
            confidence = float(predicted_value[1]) * 100
            message = f"The case is not polio suspected with a confidence of {confidence}"
        
        # Request the api (nodeJS) to save the predicted result to database
        api_url = "https://testgithub.polioantenna.org/ModelRoute/data"
        
        request_json = {
            "message": message,
            "epid_number": inputData.epid_number,
            "suspected": polio_suspected,
            "confidence_interval": confidence
        }
        
        # Make a POST request
        response = requests.post(api_url, json=request_json)
        
        if response.status_code == 200 or response.status_code == 201:
            output = response.json()
            print("Output:", output)
            return {"prediction": polio_suspected, "confidence_interval": confidence, "message": message}
        else:
            print("Error:",response.json())
            return { "error": "Internal Server Error"}

    except Exception as e:
        return {"error": str(e)}
    
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)