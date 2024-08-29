import io
import json
import asyncio
from ast import literal_eval
import streamlit as st
from dotenv import load_dotenv

from utils.document_handling import get_input_file, fill_in_front_page, write_document
from utils.web_search import get_search_results
from utils.chat_functions import create_search_query, write_document_section, create_outline_json, create_outline_string, outline_split, create_title


async def _get_text(prompt, outline):
    # search_check = str(await kernel.invoke(function_dict["search_check"]input=prompt)) zegt toch altijd True
    #search_check = "False"
    
    if st.session_state["search_status"] == "True":
        query = await create_search_query(prompt, outline)
        search_results = await get_search_results(query)
    else:
        search_results = ""
    
    #if len(str(search_results)) > 16000: # 16000 is de limiet van de gpt-35 api
    #    search_results = str(search_results[:16000])
    
    text = await write_document_section(input=prompt, search_results=search_results, language=st.session_state["language"])
    
    return text


### Process each chapter
async def _fill_in_outline(section, outline): # recursieve functie die doorheen prompts gaat en telkens de prompts naar tekst omzet
    title = section["title"]
    
    content=[]
    for prompt in section["prompts"]:
        content.append(await _get_text(prompt, outline))
    
    sections=[]
    for subsection in section["sections"]:
        sections.append(await _fill_in_outline(subsection, outline))
    
    return {"title":title, "content":content, "sections":sections}


def _doc_to_bytes(doc):
    doc_bytes = io.BytesIO()  
    doc.save(doc_bytes)  
    doc_bytes.seek(0)
    
    return doc_bytes


async def _generate_document_bytes(title, outline_json: dict):
    load_dotenv()
    # initiatie template document bovenhalen
    doc = get_input_file("./data/input_file.docx")
    
    print("Generating text for the document")

    # prompts naar gpt gegenereerde tekst omzetten
    content_json = {"sections":[]}
    # Create tasks for filling in each section outline
    fill_section_tasks = [asyncio.create_task(_fill_in_outline(section, outline_json))
                          for section in outline_json["sections"]]
    
    # Await all tasks to complete and maintain order of sections
    filled_sections = await asyncio.gather(*fill_section_tasks)
    content_json["sections"].extend(filled_sections)
    
    # maak voorpagina voor document
    doc = fill_in_front_page(doc, title)
    # tekst in het document steken
    for section in content_json["sections"]:
        doc = write_document(doc, section)
    
    print("Document has been written successfully")
    
    # bytes object voor download
    doc_bytes = _doc_to_bytes(doc)
    
    return doc_bytes


async def _create_section_json(outline_section_string):
    # Create tasks for asynchronously processing each outline section to create JSON
    outline_section_json_string = await create_outline_json(outline_section_string)
    
    try:
        # Attempt to load the JSON structure from the response
        outline_section_json = json.loads(outline_section_json_string)
    except json.JSONDecodeError:
        # Log any JSON decode errors
        #print("Error decoding JSON:")
        #print(outline_section_json_string)
        outline_section_json = json.loads(outline_section_json_string[7:-3])
    
    return outline_section_json


async def _create_outline_json(history):
    print("Define outline")
    # Retrieve the definitive outline string
    outline_string = await create_outline_string(history=history, language=st.session_state["language"])
    
    # Convert outline string to a list of outline strings
    outline_list_string = await outline_split(outline=outline_string)
    
    try:
        # Try to evaluate the outline list to a Python list object
        outline_list = literal_eval(outline_list_string)
    except SyntaxError:
        # Handle potential issues with string literals
        outline_list = outline_list_string.replace("\"", "\"\"\"")
        outline_list = literal_eval(outline_list_string[7:-3])
    
    # Prepare a list of tasks
    tasks = [_create_section_json(outline_section_string) for outline_section_string in outline_list]
    
    # Run tasks concurrently and wait for all to complete
    sections = await asyncio.gather(*tasks)
    
    # Collect results into outline_json
    outline_json = {"sections": sections}
    
    print("json outline created")
    
    # maak titel
    title = await create_title(outline=outline_string, language=st.session_state["language"])
    
    print("Created title")
    
    return title, outline_json


async def generate_document(history):
    print("Start outline json creation")
    title, outline_json = await _create_outline_json(history)
    doc_bytes = await _generate_document_bytes(title, outline_json)
    return title, doc_bytes
