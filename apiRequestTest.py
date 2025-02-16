import requests
import os

# URL of the FastAPI endpoint
url = "https://polio-image-classification-api.vercel.app/polio_classification"

# Define the input image file path
image_path = "/home/gashu/Desktop/Polio project/polio_afp_image/polio_emamu/photo_100_2025-01-06_14-10-18.jpg"

# Define the epidemiological number
epid_number = "EPtest"

# Check if the file exists
if not os.path.isfile(image_path):
    print(f"Error: The file '{image_path}' does not exist.")
else:
    # Prepare the files payload
    files = {
        'input_image': (os.path.basename(image_path), open(image_path, 'rb'), 'image/jpeg')
    }

    # Set headers
    headers = {
        'accept': 'application/json'
    }

    try:
        # Make a POST request with the query parameter in the URL
        response = requests.post(f"{url}?epid_number={epid_number}", headers=headers, files=files)

        # Raise an error for bad responses
        response.raise_for_status()

        # Parse JSON response
        output = response.json()
        print("Output:", output)

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        print("Response content:", response.text)  # Print additional response content for clarity
    except requests.exceptions.RequestException as req_err:
        print(f"Request error occurred: {req_err}")
    except ValueError as json_err:
        print(f"JSON decoding error: {json_err}")
    finally:
        # Ensure the file is closed if it was opened
        if 'input_image' in files:
            files['input_image'][1].close()