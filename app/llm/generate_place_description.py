import google.generativeai as genai  # type: ignore
from app.config import settings

genai.configure(api_key=settings.GEMINI_API_KEY)

# Create the model
generation_config = {
    "temperature": 0.4,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 2000,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-exp",
    generation_config=generation_config,
    system_instruction="Given a location name and its information, generate an engaging 350-400 character description of the location. The locations are based in Singapore. \n\nHere are some points to include: \n- what's interesting about the location\n- what is the location main service type (e.g. dining, events, services etc) \n- where is it located (use popular landmarks to reference it)\n- why people should go there. \n\nHere are some tone examples to follow: \n- Step into this speakeasy-style restaurant and bar, where nostalgic charm meets culinary innovation. Named after family-run provision stores once integral to HDB communities in Singapore, Mama Diam offers a unique dining experience to savor local classics reimagined with contemporary twists.\n- Embark on the Singapore River Dining Cruise and be dazzled by the city's bright lights as you cruise along the historic Singapore River. Dig into seafood dishes and take in the local sights!\n\nGuidelines: \n- Your description should feel make the readers imagine a scenario so that they are more interested to explore it. ",
)

HISTORY = [
    {
        "role": "user",
        "parts": [
            "bread street kitchen singapore",
        ],
    },
    {
        "role": "model",
        "parts": [
            "Step into Gordon Ramsay's Bread Street Kitchen, a vibrant dining destination at Marina Bay Sands. Indulge in a menu of British classics and international flavors, all while enjoying the stunning views of the Singapore skyline. Perfect for a memorable meal or a special occasion. Come for the food, stay for the experience!\n",
        ],
    },
    {
        "role": "user",
        "parts": [
            "Featherblade Singapore Tanjong Pagar",
        ],
    },
    {
        "role": "model",
        "parts": [
            "Savor the exquisite flavors of Featherblade, a steakhouse nestled in the heart of Tanjong Pagar. Known for its signature featherblade cut, this spot offers a no-frills, quality dining experience. Enjoy tender, flavorful steaks in a cozy, intimate setting. It's a must-visit for meat lovers seeking a satisfying meal.\n",
        ],
    },
    {
        "role": "user",
        "parts": [
            "Lau Pa sat food market ",
        ],
    },
    {
        "role": "model",
        "parts": [
            "Immerse yourself in the vibrant atmosphere of Lau Pa Sat, a historic food market in the heart of the CBD. This iconic Victorian-era structure offers a diverse array of local hawker delights. From satay to char kway teow, savor the authentic flavors of Singapore in this bustling culinary hub. A must-visit for foodies!\n",
        ],
    },
    {
        "role": "user",
        "parts": [
            "tiong bahru yong tau foo first branch",
        ],
    },
    {
        "role": "model",
        "parts": [
            "Experience the original Tiong Bahru Yong Tau Foo, a beloved local eatery. Located near Tiong Bahru Market, this humble spot serves up authentic Hakka-style yong tau foo with a variety of fresh ingredients. Customize your bowl and savor the comforting flavors that have made it a neighborhood favorite. A taste of tradition awaits!\n",
        ],
    },
]


def generate_place_description(location_name: str) -> str:
    """Generate an engaging description for a given location name"""

    # use few-shot prompts
    chat_session = model.start_chat(history=HISTORY)
    response = chat_session.send_message(location_name)
    print(response.usage_metadata)
    return response.text
