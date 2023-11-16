import httpx
from config import config


async def simple_email_builder(to: str, subject: str, body: str):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"https://api.mailgun.net/v3/{config.MAILGUN_DOMAIN}/messages",
                auth=("api", config.MAILGUN_API_KEY),
                data={
                    "from": f"Luis Martinez <mailgun@{config.MAILGUN_DOMAIN}>",
                    "to": [to],
                    "subject": subject,
                    "text": body,
                },
            )

            response.raise_for_status()

            return response
        except httpx.HTTPError as e:
            raise e


async def send_user_registration_email(email: str, confirmation_url: str):
    return await simple_email_builder(
        email,
        "Successfully signed up to Store website",
        (
            f""" 
                Hi {email}! You have successfully registered to our Store website.
                Please confirm your email by clicking on the following link
                {confirmation_url}
            """
        ),
    )
