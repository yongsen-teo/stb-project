import json
import google.generativeai as genai  # type: ignore
import typing_extensions as typing
from app.config import settings

genai.configure(api_key=settings.GEMINI_API_KEY)


def convert_offerings_to_dict(xml_text):
    # Split into lines and clean whitespace
    lines = [line.strip() for line in xml_text.splitlines() if line.strip()]

    offerings = {}
    current_name = None

    for line in lines:
        if "<name>" in line:
            current_name = line.replace("<name>", "").replace("</name>", "").strip()
        elif "<price_range>" in line and current_name:
            price = (
                line.replace("<price_range>", "").replace("</price_range>", "").strip()
            )
            offerings[current_name] = f"SGD {price}"
            current_name = None

    return offerings


generation_config = {
    "temperature": 0.4,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-exp",
    generation_config=generation_config,
    system_instruction="Given a location name and its price level information, generate the top offerings and estimated prices for the location.\nUse the Grouding tool whenever necessary to find updated offerings and their prices.\nThe locations are based in Singapore.\n\nYou should provide top 5 offerings for the place in JSON with the offering name as the key and an estimated numerical price range (SGD) as its value. \nExample output: \n- give in XML tags \n- you should give an estimated price range for each offering\n",
)


def generate_top_offerings(
    location_name: str,
) -> typing.Dict[str, str]:
    """
    Generate the top offerings and estimated prices for a given location.
    Used XML tags to format the response for reliable parsing.
    """
    chat_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [
                    'Location Name: LAVO MBS Singapore \nPrice level: "PRICE_LEVEL_VERY_EXPENSIVE"',
                ],
            },
            {
                "role": "model",
                "parts": [
                    'Okay, here are the top 5 offerings at LAVO MBS Singapore, with estimated price ranges in SGD, based on the provided information. Given the "PRICE_LEVEL_VERY_EXPENSIVE" tag, the prices reflect the higher end of the spectrum.\n\n```xml\n<offerings>\n  <offering>\n    <name>The Meatball</name>\n    <price_range>38 - 45</price_range>\n  </offering>\n  <offering>\n    <name>Seafood Plateau Piccolo</name>\n    <price_range>170 - 180</price_range>\n  </offering>\n   <offering>\n    <name>Lamb Chops</name>\n    <price_range>80 - 90</price_range>\n  </offering>\n  <offering>\n    <name>New York Strip</name>\n    <price_range>100 - 120</price_range>\n  </offering>\n   <offering>\n    <name>20 Layer Chocolate Cake</name>\n    <price_range>30 - 40</price_range>\n  </offering>\n</offerings>\n```',
                ],
            },
            {
                "role": "user",
                "parts": [
                    "Location name: ah chew dessert in bugis\nPrice level: cheap",
                ],
            },
            {
                "role": "model",
                "parts": [
                    "```xml\n<offerings>\n  <offering>\n    <name>Mango Sago</name>\n    <price_range>4 - 5</price_range>\n  </offering>\n  <offering>\n    <name>Durian Sago</name>\n    <price_range>6 - 7</price_range>\n  </offering>\n  <offering>\n    <name>Sesame Paste</name>\n    <price_range>3.5 - 4.5</price_range>\n  </offering>\n  <offering>\n    <name>Almond Paste</name>\n    <price_range>3.5 - 4.5</price_range>\n  </offering>\n    <offering>\n    <name>Water Chestnut Cake</name>\n    <price_range>3 - 4</price_range>\n  </offering>\n</offerings>\n```",
                ],
            },
            {
                "role": "user",
                "parts": [
                    "mcdonalds lot one ",
                ],
            },
            {
                "role": "model",
                "parts": [
                    "Okay, here are the top 5 offerings at McDonald's Lot One, with estimated price ranges in SGD. Please note that prices can vary slightly based on promotions and specific meal options.\n\n```xml\n<offerings>\n  <offering>\n    <name>Big Mac</name>\n    <price_range>7 - 9</price_range>\n  </offering>\n  <offering>\n    <name>McSpicy Meal</name>\n    <price_range>9.75 - 11</price_range>\n  </offering>\n  <offering>\n    <name>Filet-O-Fish Meal</name>\n    <price_range>7.45 - 9</price_range>\n  </offering>\n    <offering>\n    <name>Chicken McNuggets (6pc) Meal</name>\n     <price_range>7 - 8.5</price_range>\n  </offering>\n  <offering>\n    <name>Double Cheeseburger Meal</name>\n    <price_range>8.30 - 9.5</price_range>\n  </offering>\n</offerings>\n```",
                ],
            },
            # {
            #     "role": "user",
            #     "parts": [location_name, price_level],
            # },
        ]
    )
    response = chat_session.send_message(location_name)
    print(f"Response: {response}")
    print(f"Response usage metadata: {response.usage_metadata}")
    top_offerings = convert_offerings_to_dict(response.text)
    print(f"Top offerings for {location_name}: {top_offerings}")
    return top_offerings
