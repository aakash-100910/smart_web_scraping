from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
import concurrent.futures
from functools import lru_cache

from scrape import split_dom_content

# Define a simplified prompt for faster processing
template = (
    "Extract information matching: {parse_description} "
    "from the following content: {dom_content}. "
    "Return only the relevant data."
)

model = OllamaLLM(model="phi3.5")

# Cache results for faster repeated access
@lru_cache(maxsize=128)
def process_chunk(chunk, parse_description):
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model
    response = chain.invoke({"dom_content": chunk, "parse_description": parse_description})
    return response

def parse_with_ollama(dom_content, parse_description):
    # Larger chunk size to reduce processing overhead
    chunks = split_dom_content(dom_content, max_length=10000)  # Increased chunk size for speed
    results = []

    # Use ThreadPoolExecutor for efficient parallel processing
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        future_to_chunk = {executor.submit(process_chunk, chunk, parse_description): chunk for chunk in chunks}
        for future in concurrent.futures.as_completed(future_to_chunk):
            results.append(future.result())

    # Combine results into a single string
    return "\n".join(results)
