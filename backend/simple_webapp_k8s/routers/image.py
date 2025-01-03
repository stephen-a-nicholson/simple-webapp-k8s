""" Contains endpoint to generate image from text prompt """
from fastapi import APIRouter, HTTPException, Depends
from huggingface_hub import InferenceClient
import base64
from ..auth_utils import get_current_user
import os
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

router = APIRouter()

client = InferenceClient(token=os.getenv("HUGGINGFACE_API_TOKEN"))


class ImagePrompt(BaseModel):
    prompt: str


@router.post("/generate")
async def generate_image(
    prompt_data: ImagePrompt, current_user: dict = Depends(get_current_user)
):
    """
    Generate an image from a text prompt using Stable Diffusion XL
    """
    try:
        image_blob = client.post(
            json={"inputs": prompt_data.prompt},
            model="stabilityai/stable-diffusion-xl-base-1.0",
        )

        base64_image = base64.b64encode(image_blob).decode()

        return {
            "success": True,
            "image": f"data:image/png;base64,{base64_image}",
            "prompt": prompt_data.prompt,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
