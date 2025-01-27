import re
import base64
import google.generativeai as genai  # type: ignore
from app.config import settings

genai.configure(api_key=settings.GEMINI_API_KEY)

system_prompt = """Given an image and its information, generate 3 types of information for the image. The image locations are based in Singapore. 

The 3 types of information are: 
- Image Caption 
- Short Name for the image
- Appropriate hashtags to associate with the image

The tone for the captions will differ based on the location type. 

# Dining Location Tone Examples ("image name": "image caption"): 
- "Award-Winning Bars": "Bold new flavours and buzzing nightlife come together in an intoxicating blend at these world-class bars."
- "Top Restaurants": "Finesse, flavour and the finest meals you'll ever taste – when it comes to award-winning restaurants, Singapore is an epicurean's paradise." 
- "Unique Dining Experiences": "Take in gorgeous views, have breakfast with furry friends at the zoo and discover a host of unique experiences that turn dining into an adventure!"

# Events Location Tone Examples ("image name": "image caption"): 
- "Bird Paradise": "Roamed with the winged wanderers and enjoy the interactive experience amid lush green habitats."
- "Trifecta": "Experience the ultimate thrill and unleash your adventurous spirit at Trifecta. Hit the snowboard, ride the waves, and feel the excitement of the skate bowl" 
Guidelines: 
- Your description should feel make the readers imagine a scenario so that they are more interested to explore it. 

Guidelines:
- caption must be less than 70 words (follow the above examples in terms of tonality)
- the name must be short and sweet
- include the values for "name", "caption and "hashtags" in your response. Enclose them in XML tags.
- hashtags must be separated by commas and should not contain spaces or quotes.
But make sure to include the # symbol before each hashtag.
"""


def parse_xml_tags(xml_string, tag):
    """Parse the content inside the specified XML tag"""
    # Regex pattern to match the content inside the specified tag
    pattern = f"<{tag}[^>]*>(.*?)</{tag}>"

    # Search for the first match
    match = re.search(pattern, xml_string, re.DOTALL)

    # Return the stripped text if a match is found, otherwise return None
    return match.group(1).strip() if match else None


def generate_image_info(photo_binary):
    """Generate image information using the Gemini API"""

    print("Generating image info for photo binary")
    prompt = """Caption this image in 70 words or less.
    What would you name this image? What hashtags would you associate with this image?"""
    generation_config = {
        "temperature": 0.5,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 2000,
    }

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=system_prompt,
        generation_config=generation_config,
    )

    content_list = []
    content_list.append(
        {
            "mime_type": "image/jpeg",
            "data": base64.b64encode(photo_binary).decode("utf-8"),
        }
    )
    content_list.append(prompt)
    response = model.generate_content(content_list)
    print(f"generate_image_info response: {response}")
    response = response.text
    response_body = {
        "name": parse_xml_tags(response, "name"),
        "caption": parse_xml_tags(response, "caption"),
        "hashtags": parse_xml_tags(response, "hashtags"),
    }
    print(f"Image Info generated --- Response Body: {response_body}")
    return response_body
