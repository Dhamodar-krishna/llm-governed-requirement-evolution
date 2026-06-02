import os

from dotenv import load_dotenv

from anthropic import AnthropicBedrock

# =================================================
# LOAD ENV VARIABLES
# =================================================

load_dotenv()

# =================================================
# BEDROCK CLIENT
# =================================================

client = AnthropicBedrock(

    aws_access_key=os.getenv(
        "AWS_ACCESS_KEY_ID"
    ),

    aws_secret_key=os.getenv(
        "AWS_SECRET_ACCESS_KEY"
    ),

    aws_region=os.getenv(
        "AWS_DEFAULT_REGION"
    )
)

# =================================================
# LLM CALL
# =================================================

import time


def call_llm(prompt):

    for attempt in range(3):

        try:

            response = client.messages.create(

                model="anthropic.claude-sonnet-4-6",

                max_tokens=4000,

                temperature=0.1,

                messages=[

                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            return response.content[0].text

        except Exception as e:

            if attempt < 2:

                time.sleep(3)

            else:

                raise Exception(
                    "The LLM service is temporarily unavailable. "
                    "Please wait a moment and run the framework again."
                )