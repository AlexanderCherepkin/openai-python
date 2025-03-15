from openai import OpenAI
from dotenv import load_dotenv
from pprint import pprint
import base64
import os
from utils.conversion import object_to_dict

load_dotenv()

client = OpenAI()


# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


model = "omni-moderation-latest"
module_dir = os.path.dirname(os.path.abspath(__file__))
images_dir = os.path.join(module_dir, "images")
sample_image_file_path = os.path.join(images_dir, "a_dramatic_and_intense_na_v2.png")
base64_sample_image = encode_image(sample_image_file_path)


try:
    # EXAMPLE 1 - Image URL
    response = client.moderations.create(
        model=model,
        input=[
            {"type": "text", "text": "I really hate earth and all people in the world"},
            {
                "type": "image_url",
                "image_url": {
                    "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/80/13_Mile_%2885521817%29.jpeg/1200px-13_Mile_%2885521817%29.jpeg",
                    "detail": "low",
                },
            },
        ],
    )

    pprint(object_to_dict(response))
    
except Exception as e:
    print("Error during OpenAI API communication occured:", e)
    
    
    
#   {'_request_id': 'req_77756eb60d5e831ea83e8809bbb84551',
#  'id': 'modr-77756eb60d5e831ea83e8809bbb84551',
#  'model': 'omni-moderation-latest',
#  'results': [{'categories': {'harassment': False,
#                              'harassment_threatening': False,
#                              'hate': False,
#                              'hate_threatening': False,
#                              'illicit': False,
#                              'illicit_violent': False,
#                              'self_harm': False,
#                              'self_harm_instructions': False,
#                              'self_harm_intent': False,
#                              'sexual': False,
#                              'sexual_minors': False,
#                              'violence': False,
#                              'violence_graphic': False},
#               'category_applied_input_types': {'harassment': ['text'],
#                                                'harassment_threatening': ['text'],
#                                                'hate': ['text'],
#                                                'hate_threatening': ['text'],
#                                                'illicit': ['text'],
#                                                'illicit_violent': ['text'],
#                                                'self_harm': ['text', 'image'],
#                                                'self_harm_instructions': ['text',
#                                                                           'image'],
#                                                'self_harm_intent': ['text',
#                                                                     'image'],
#                                                'sexual': ['text', 'image'],
#                                                'sexual_minors': ['text'],
#                                                'violence': ['text', 'image'],
#                                                'violence_graphic': ['text',
#                                                                     'image']},
#               'category_scores': {'harassment': 0.34232758880668784,
#                                   'harassment_threatening': 0.0008208990838843598,
#                                   'hate': 0.020614598407216186,
#                                   'hate_threatening': 2.4156629828672456e-05,
#                                   'illicit': 1.0071400221737608e-05,
#                                   'illicit_violent': 2.710880136557205e-06,
#                                   'self_harm': 0.00045765168153699784,
#                                   'self_harm_instructions': 1.3846004563753396e-06,
#                                   'self_harm_intent': 5.829126566113866e-06,
#                                   'sexual': 1.0229985472581487e-05,
#                                   'sexual_minors': 4.936988949458183e-07,
#                                   'violence': 0.0005584771959849744,
#                                   'violence_graphic': 6.814872211615988e-06},
#               'flagged': False}]}
