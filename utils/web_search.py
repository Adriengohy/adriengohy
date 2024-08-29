import aiohttp
from bs4 import BeautifulSoup


async def _get_tavily_response(search_term, max_results):
    # The API endpoint URL
    url = 'https://api.tavily.com/search'

    # The body of the POST request
    payload = {
        "api_key": "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",
        "query": search_term,
        "search_depth": "basic",
        "include_answer": True,
        "include_images": False,
        "include_raw_content": False,
        "max_results": max_results,
        "include_domains": [],
        "exclude_domains": []
    }
    # Headers to specify that the payload is in JSON format
    headers = {'Content-Type': 'application/json'}
    
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload, headers=headers) as response:
            response_data = await response.json()

            search_results = {
                "first_result": {
                    "title": response_data["results"][0]["title"],
                    "url": response_data["results"][0]["url"],
                    "content": response_data["results"][0]["content"]
                },
                "second_result": {
                    "title": response_data["results"][1]["title"],
                    "url": response_data["results"][1]["url"],
                    "content": response_data["results"][1]["content"]
                },
                "third_result": {
                    "title": response_data["results"][2]["title"],
                    "url": response_data["results"][2]["url"],
                    "content": response_data["results"][2]["content"]
                },
            }

            return search_results

async def _get_url_raw(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status_code == 200:
                return await response.read()
            else:
                return f"Error: Unable to get content from {url}, status code: {response.status_code}"


def _extract_readable_info(raw_content):
    soup = BeautifulSoup(raw_content, 'html.parser')
    content_tags = ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li', 'article', 'section']
    text_content = []
    
    for tag in content_tags:
        for element in soup.find_all(tag):
            text_content.append(element.get_text())

    readable_text = ' '.join(text_content)
    
    return readable_text


def _clean_text(input_string):
    # Remove all newline characters
    no_newlines = input_string.replace('\n', ' ')
    # Remove everything between curly braces (including the braces)
    #cleaned_string = re.sub(r'\{.*?\}', '', no_newlines)
    return no_newlines


async def get_search_results(search_term, max_results=3):
    tavily_response = await _get_tavily_response(search_term, max_results)
    zoekresultaten = []
    for key, resultaat in tavily_response.items():
        raw_content = await _get_url_raw(resultaat["url"])
        readable_content = _extract_readable_info(raw_content)
        clean_content = _clean_text(readable_content)
        
        zoekresultaten.append(key+":\n"+clean_content+"\n")
    
    return zoekresultaten
