from json import JSONDecodeError

from config import config
from database import engine, post_table
from httpx import AsyncClient, HTTPStatusError
from sqlalchemy import update
from sqlalchemy.orm import Session
from utils.send_email import simple_email_builder


# private function
async def _generate_image_api(prompt: str):
    async with AsyncClient() as client:
        try:
            response = await client.post(
                "https://api.deepai.org/api/cute-creature-generator",
                data={"text": prompt},
                headers={"api-key": config.DEEP_API_KEY},
                timeout=60,
            )

            response.raise_for_status()
            return response.json()
        except HTTPStatusError as e:
            raise e
        except JSONDecodeError as err:
            raise err


async def generate_and_add_to_post(
    email: str,
    post_id: int,
    post_url: str,
    prompt: str = "A blue british shorthair cat with a white belly",
):
    try:
        response = await _generate_image_api(prompt)
    except Exception:
        return await simple_email_builder(
            email,
            "Error generating image",
            f"""
                Hi {email}! I was passing through to let you know that 
                there was an error generating the image for your post {post_url}
            """,
        )

    query = (
        update(post_table)
        .where(post_table.c.id == post_id)
        .values(image_url=response["output_url"])
    )

    with Session(engine) as session:
        try:
            session.execute(query)
            session.commit()
            session.close()
        except Exception as e:
            session.rollback()
            raise e

    await simple_email_builder(
        email,
        "Image generation completed",
        f"""
            Hi {email}! Your image has been generated and added to your post. 
            Please check it out on the following url {post_url}
        """,
    )

    return response
