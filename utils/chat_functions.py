from utils.rag_api_call import fetch_response


async def brainstorm_chat(user_context, language, history=""):
    system_message = """You are an AI assistant that is trying to help the user create an outline for a document that he is trying to create.
        The user may also upload text of his own that serves as additional context, which is provided below if applicable.
        When responding to the user, begin by displaying the outline you have generated up until this point by looking at the chat history.
        Then you may propose new ideas if appropriate.

        ALWAYS USE BULLET LISTS. 
        BE VERY THOROUGH WHEN CREATING YOUR OUTLINE. 
        CREATE EXTRA SUBTITLES FOR THE MAIN OUTLINE SECTIONS.
        CREATE EVEN MORE SUBTITLES FOR THOSE SUBTITLES, UP TO THREE LEVELS DEEP."""
    
    user_message = f"""
        WRITE THE TEXT IN {language}

        User provided text:
        {user_context}

        Conversation history:
        {history}

        Outline as a bullet list:"""
    
    return await fetch_response(system_message, user_message)


async def create_title(outline, language):
    system_message = """You create a title for a document based on the outline.

        You should only generate the title itself, nothing else.
        Following rules apply:
        - Max 30 characters
        - Do not return anything else
        - No " in your output
        - Only use letters from the alphabet and spaces, nothing else

        EXAMPLE
        Outline:
        1. Introduction to the Pharma Industry
           - Definition of the pharmaceutical industry
           - Importance and impact on global health and economy
           - Historical overview of the industry
           - Key challenges and opportunities facing the industry

        2. Trends in the Pharma Industry
           - Shift towards personalized medicine
             - Advancements in genomics and targeted therapies
             - Impact on drug development and patient care
           - Increased focus on biopharmaceuticals
             - Growth of biologics and biosimilars
             - Market trends and investment in biopharma
           - Regulatory changes and their impact
             - Updates in drug approval processes
             - Implications for market access and pricing
           - Global market trends and forecasts
             - Market size and growth projections
             - Regional dynamics and emerging markets

        3. Overview of the 10 Biggest Pharma Companies
           - Company 1: Summary and key highlights
             - Market position and revenue
             - Notable products and therapeutic areas
           - Company 2: Summary and key highlights
             - Market position and revenue
             - Notable products and therapeutic areas
           - ...
           - Company 10: Summary and key highlights
             - Market position and revenue
             - Notable products and therapeutic areas

        4. The Position of China and India in Pharma
           - Overview of the pharmaceutical industry in China
             - Market size and growth
             - Regulatory landscape and market access
           - Key players and market dynamics in India
             - Domestic and international market presence
             - Innovation and manufacturing capabilities
           - Comparison of China and India's roles in global pharma
             - Competitive advantages and challenges
             - Future outlook and implications for the global industry

        5. Mergers and Acquisitions (M&A) Activity in Pharma
           - Recent M&A trends and their impact
             - Drivers of M&A activity in the industry
             - Notable deals and their implications
           - Regulatory challenges and opportunities in M&A
             - Antitrust considerations and regulatory approvals
             - Impact on market competition and innovation

        6. Status of Biopharma
           - Definition and significance of biopharmaceuticals
             - Distinction from traditional small molecule drugs
             - Market growth and investment in biopharma
           - Regulatory landscape for biopharmaceutical products
             - Approval pathways and regulatory requirements
             - Market access and pricing considerations

        7. Biggest Biopharma Players
           - Company 1: Overview and key biopharma products
             - Leading biopharma products and pipeline
             - Market position and competitive landscape
           - Company 2: Overview and key biopharma products
             - Leading biopharma products and pipeline
             - Market position and competitive landscape
           - ...
           - Company n: Overview and key biopharma products
             - Leading biopharma products and pipeline
             - Market position and competitive landscape

        8. Biopharma Clusters in Europe and Globally
           - Overview of major biopharma clusters in Europe
             - Key clusters and their specialization
             - Research and innovation ecosystem
           - Comparison with biopharma clusters in other regions
             - Global biopharma hubs and their strengths
             - Collaborations and partnerships across clusters
           - Factors contributing to the growth of biopharma clusters
             - Government incentives and industry initiatives
             - Talent pool and academic-industry collaborations

        9. Top 10 Universities in Pharma
           - University 1: Research and contributions to the pharma industry
             - Notable research areas and breakthroughs
             - Industry collaborations and technology transfer
           - University 2: Research and contributions to the pharma industry
             - Notable research areas and breakthroughs
             - Industry collaborations and technology transfer
           - ...
           - University 10: Research and contributions to the pharma industry
             - Notable research areas and breakthroughs
             - Industry collaborations and technology transfer

        10. Trends in Clinical Trials
           - Shift towards virtual and decentralized clinical trials
             - Adoption of remote monitoring and digital technologies
             - Impact on patient recruitment and trial efficiency
           - Use of real-world evidence in clinical research
             - Integration of RWE in regulatory decision-making
             - Applications in post-market surveillance and outcomes research
           - Emerging technologies and their impact on clinical trials
             - AI, machine learning, and predictive analytics
             - Wearable devices and digital endpoints

        11. Impact of AI on Pharma
           - Applications of artificial intelligence in drug discovery
             - AI-driven target identification and lead optimization
             - Drug repurposing and virtual screening
           - AI in clinical trial design and patient recruitment
             - Predictive analytics for patient selection and stratification
             - Optimization of trial protocols and endpoints
           - Regulatory considerations and challenges in AI adoption
             - Validation and transparency in AI algorithms
             - Ethical and privacy concerns in AI-driven healthcare

        12. Conclusion
           - Recap of key insights and findings
           - Future outlook for the pharmaceutical industry

        Title:
        Pharma Industry Insights

        END EXAMPLE"""
    
    user_message = f"""Outline:
        {outline}

        WRITE THE TITLE IN {language}

        Title:"""
    
    return await fetch_response(system_message, user_message)


async def create_outline_string(history, language):
    system_message = """You are an AI assistant that helps with creating the outline of a document of text that the user is asking about.

        You will be given the transcript of a conversation. Use this transcript to figure out the best and most detailed version of the outline that you can possibly make that is coherent with user requests.
        """
    
    user_message = f"""The content of outline must contain titles, subtitles, subsubtitles and so on as much as possible.

        TRANSCRIPT OF THE CONVERSATION:
        {history}

        WRITE THE TEXT IN {language}

        Outline:"""
    
    return await fetch_response(system_message, user_message)


async def create_outline_json(outline):
    system_message = """You are an AI assistant that is tasked with turning the outline of a document into a JSON structure.

        This outline is structured as a list of sections.
        Each section is itself written as a json in the following way:
        1. A "title" element that contains a string that is the title of this section.
        2. A "prompts" element that contains a list of strings, these strings are prompts for future text generation using GPT. Keep only one string element in this list.
        3. A "sections" element that contains a list of sections, there should be subsections added if a certain title of the outline has subtitles. If this is not the case, make this an empty list.


        EXAMPLE
        Outline:
        II. History of the Pharmaceutical Industry  
           # Early developments in pharmaceuticals
            ## Origins of Herbal Medicines
            ## The Birth of Modern Pharmacy
             ### Influence of the Renaissance on Medicine
             ### Pioneering Figures in Early Pharmacy
            ## The Impact of the Scientific Revolution
           # Milestones in the pharmaceutical industry

        JSON:
        {
          "title": "History of the Pharmaceutical Industry",
          "prompts": [
            "Explore the historical development of the pharmaceutical industry, noting key milestones and innovations."
          ],
          "sections": [
            {
          "title": "Early Developments in Pharmaceuticals",
          "prompts": [
            "Describe the early developments in pharmaceuticals, focusing on the origins and initial discoveries that shaped the industry."
          ],
          "sections": [
            {
              "title": "Origins of Herbal Medicines",
              "prompts": [
                "Trace the history of pharmaceuticals back to the use of herbal medicines and natural compounds in ancient civilizations."
              ],
              "sections": []
            },
            {
          "title": "The Birth of Modern Pharmacy",
          "prompts": [
            "Explain the emergence of modern pharmacy in the Renaissance period, highlighting key figures and their contributions."
          ],
          "sections": [
            {
              "title": "Influence of the Renaissance on Medicine",
              "prompts": [
                "Discuss how the Renaissance period influenced medical knowledge and practices, setting the stage for modern pharmacy."
              ],
              "sections": []
            },
            {
              "title": "Pioneering Figures in Early Pharmacy",
              "prompts": [
                "Profile pioneering figures in early pharmacy, such as Paracelsus, who challenged traditional methods and promoted the use of chemicals in medicine."
              ],
              "sections": []
            }
          ]
        },
            {
              "title": "The Impact of the Scientific Revolution",
              "prompts": [
                "Detail how the Scientific Revolution propelled the pharmaceutical industry forward through advancements in chemistry and biology."
              ],
              "sections": []
            }
          ]
        },
            {
              "title": "Milestones in the Pharmaceutical Industry",
              "prompts": [
                "Outline the major milestones in the history of the pharmaceutical industry, including breakthrough drugs and regulatory changes."
              ],
              "sections": []
            }
          ]
        }"""
    
    user_message = f"""Outline:
        {outline}

        JSON:"""
    
    return await fetch_response(system_message, user_message)


async def outline_split(outline):
    system_message = """You split up an outline into its major parts.
        Create a list object, with each element being one part of the outline.
        Respect the language of the outline.

        EXAMPLE
        Outline:
        - Introduction to the Pharmaceutical Industry
          - Definition and Overview
            - What is the pharmaceutical industry?
            - Importance of pharmaceuticals in healthcare
            - Impact on Healthcare
              - Role in disease treatment and prevention
              - Economic and social impact
          - History of the Pharmaceutical Industry
            - Early Beginnings
              - Origins of pharmaceutical practices
              - Evolution of medicine and drug development
            - Milestones and Innovations
              - Discovery of key drugs
              - Development of pharmaceutical regulations
            - Regulatory Changes and Impact
              - Introduction of FDA and other regulatory bodies
              - Impact of regulations on drug development and safety
          - Key Players in the Pharmaceutical Industry
            - Major Companies
              - Overview of leading pharmaceutical companies
              - Global reach and market share
            - Research and Development Institutions
              - Role of research institutions in drug discovery
              - Collaboration with pharmaceutical companies
            - Regulatory Agencies
              - FDA and its role in drug approval
              - International regulatory bodies and their influence

        List:
        ["- Introduction to the Pharmaceutical Industry\
          - Definition and Overview\
            - What is the pharmaceutical industry?\
            - Importance of pharmaceuticals in healthcare\
            - Impact on Healthcare\
              - Role in disease treatment and prevention\
              - Economic and social impact",
        "  - History of the Pharmaceutical Industry\
            - Early Beginnings\
              - Origins of pharmaceutical practices\
              - Evolution of medicine and drug development\
            - Milestones and Innovations\
              - Discovery of key drugs\
              - Development of pharmaceutical regulations\
            - Regulatory Changes and Impact\
              - Introduction of FDA and other regulatory bodies\
              - Impact of regulations on drug development and safety",
        "  - Key Players in the Pharmaceutical Industry\
            - Major Companies\
              - Overview of leading pharmaceutical companies\
              - Global reach and market share\
            - Research and Development Institutions\
              - Role of research institutions in drug discovery\
              - Collaboration with pharmaceutical companies\
            - Regulatory Agencies\
              - FDA and its role in drug approval\
              - International regulatory bodies and their influence"]"""
    
    user_message = f"""Outline:
        {outline}

        List:"""
    
    return await fetch_response(system_message, user_message)


async def write_document_section(language, search_results, input):
    system_message = f"""Write a section of a document based on the search results from the web. Make it a nicely readable text. WRITE THE TEXT IN {language}"""

    assisstant_message = f"""
    [CONTEXT]

    ADDITIONAL INFORMATION FROM THE WEB:
    {search_results}

    [END CONTEXT]"""
    
    user_message = f"""Section Prompt:
        {input}"""
    
    return await fetch_response(system_message, user_message, assisstant_message)


async def create_search_query(outline, input):
    system_message = f"""You are an AI assistant that creates a query for a public search query. 
        The goal of this query is to get the most relevant possible information from a public web search for a text document.
        You should base this public search query on the outline of the document and the user prompt that you are given. 

        YOU CAN ONLY CREATE A SEARCH QUERY
        THE QUERY CAN NOT BE LONGER THAN 10 WORDS"""

    assisstant_message = f"""
        Outline of the document(for reference only):
        {outline}"""
    
    user_message = f"""Prompt:
        {input}

        Query:"""
    
    return await fetch_response(system_message, user_message, assisstant_message)


async def is_search_necessary(input): ### does not work; always returns True for some reason
    system_message = f"""You are something that can only output a boolean.
        Only return "True" or "False". 
        NO OTHER RESPONSE ALLOWED. ONLY "True" OR "False".

        A section of a professional document is being written based on a prompt.
        Using the prompt, it is up to you to decide whether or not this section would benefit from a public search to gather the most recent information.
        If it is unlikely that up-to-date information will improve the content significantly, no public search should be done.

        Return "True" if you believe a public search is helpful, given the prompt.
        If you believe public search will not significantly improve the content that is being written, return "False"."""

    assisstant_message = f"""
        EXAMPLE
        Prompt:
        Comparison of biopharma clusters in the US, Asia, and other regions
        Output:
        True

        Prompt:
        Definition and significance of biopharmaceuticals
        Output:
        False

        Prompt:
        Adoption of real-world evidence and decentralized trials
        Output:
        False

        Prompt:
        Recap of key insights and findings
        Output:
        False

        Prompt:
        Profiles of leading biopharmaceutical companies
        Output:
        True

        Prompt:
        Pharmaceutical market in India
        Output:
        True
        END EXAMPLE"""
    
    user_message = f"""Prompt:
        {input}

        Output:"""
    
    return await fetch_response(system_message, user_message, assisstant_message)
