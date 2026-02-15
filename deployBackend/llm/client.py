import os
import replicate

client = replicate.Client(
    api_token=os.getenv("REPLICATE_API_TOKEN")
)

def generate_response(prompt: str):
    output = client.run(
        "meta/meta-llama-3-8b-instruct",
        input={
            "prompt": prompt,
            "max_tokens": 500,
            "temperature": 0.7
        }
    )

    return "".join(output)
