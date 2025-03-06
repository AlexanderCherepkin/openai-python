from openai import OpenAI
from dotenv import load_dotenv
from pprint import pprint
import os
import base64
from utils.conversion import object_to_dict

load_dotenv()

client = OpenAI()

prompt = "replace cat with a rabbit"
model = "dall-e-2"
response_format = "b64_json"
size = "1024x1024"

images_folder_name = "images_edits"
input_image_name = "input.png"
mask_name = "mask.png"
output_image_name = "output.png"

module_dir = os.path.dirname(os.path.abspath(__file__))
images_dir = os.path.join(module_dir, images_folder_name)
input_image_file_path = os.path.join(images_dir, input_image_name)
mask_file_path = os.path.join(images_dir, mask_name)
output_image_file_path = os.path.join(images_dir, output_image_name)

try:
    # STEP 1 - Get edited image
    with open(input_image_file_path, "rb") as input_image_file:
        with open(mask_file_path, "rb") as mask_file:
            response = client.images.edit(
                prompt=prompt,
                image=input_image_file,
                mask=mask_file,
                model=model,
                response_format=response_format,
                size=size,
                # n=1,
            )

    # pprint(object_to_dict(response))

    b64_data = response.data[0].b64_json

    if b64_data:
        # STEP 2 - Save image in the file in the images folder in the same directory as module
        with open(output_image_file_path, "wb") as file:
            file.write(base64.b64decode(b64_data))

        print("Successfully saved image:", output_image_name)
    else:
        print("Image data in Base64 format wasn't received from the server")

except Exception as e:
    print("Error during OpenAI API communication occured:", e)
