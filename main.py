from fastapi import FastAPI, Form
import uvicorn
import os
# from PIL import Image

from fastapi import File, UploadFile, HTTPException
from gradio_client import Client, file, handle_file

app = FastAPI(
    title="Polio image classification",
    version="1.0.0",
)

# Allowed image extensions
ALLOWED_EXTENSIONS = {".jpg", ".jpeg"}

def is_file_extension_allowed(filename: str) -> bool:
    return filename.lower().endswith(tuple(ALLOWED_EXTENSIONS))

async def save_uploaded_image(uploaded_image: UploadFile) -> str:
    """Saves the image to the specified path and returns the save path."""
    try:
        contents = await uploaded_image.read()
        filename = f"{uploaded_image.filename}"
        save_path = os.path.join(os.getcwd(), filename)
        
        with open(save_path, "wb") as f:
            f.write(contents) 

        return save_path

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
async def predict_polio(input_image: UploadFile = File(...)):
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
                    
        return {"prediction": polio_suspected, "confidence_interval": confidence, "message": message}

    except Exception as e:
        return {"error": str(e)}
    
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)