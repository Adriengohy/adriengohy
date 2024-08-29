from re import search
from asyncio import sleep
from openai import AsyncAzureOpenAI


def _initialize_client(model):
    KEY = "f12a097f613c42308843a87a4bb23f5c"
    ENDPOINT = "https://lucasaiswedenservices.openai.azure.com/"
    DEPLOYMENT = model
    
    base_url = f"{ENDPOINT}/openai/deployments/{DEPLOYMENT}"
    
    client = AsyncAzureOpenAI(
            api_key=KEY,
            api_version="2023-12-01-preview",
            base_url=base_url,
        )
    
    return client


def _make_prompt(system_message, user_message, assistant_message):
    prompt = [
        {
            "role": "system",
            "content": system_message
        },
        {
            "role": "user",
            "content": user_message
        }
    ]
    if assistant_message:
        prompt.append(
            {
                "role": "assistant",
                "content": assistant_message
            }
        )
    
    return prompt


async def _call_api_with_rate_limit_handling(client, model, prompt):
    def _extract_retry_seconds(error_message):
        print(error_message)
        match = search(r'Please retry after (\d+) seconds', error_message)
        if match:
            return int(match.group(1))
        return None

    try:
        # Attempt to call the API
        print("Calling API")
        completion = await client.chat.completions.create(
        model=model,
        messages=prompt,
        temperature=0,
        top_p=1,
        max_tokens=800,
        stop=None,
        stream=False
        )
    
        return completion.choices[0].message.content
    
    except Exception as e:
        wait_time = _extract_retry_seconds(str(e)) or 8  # Defaults to 8 seconds if extraction fails
        if wait_time is not None:
            print(e)
            print(wait_time)
            print(f"Rate limit exceeded, waiting for {wait_time} seconds...")
            await sleep(wait_time)
            return await _call_api_with_rate_limit_handling(client, model, prompt)
        else:
            raise e


async def fetch_response(system_message, user_message, assistant_message=None, model="gpt-4o-mini"):
    client = _initialize_client(model)
    prompt = _make_prompt(system_message, user_message, assistant_message)
    response = await _call_api_with_rate_limit_handling(client, model, prompt)
    return response
