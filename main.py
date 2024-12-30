import streamlit as st
from scrape import (
    scrape_website,
    extract_body_content,
    clean_body_content,
)
from parse import parse_with_ollama

# Streamlit UI
st.title("SMART WEB SCRAPING TOOL")
url = st.text_input("Enter Website URL")

# Step 1: Scrape the Website
if st.button("Scrape Website"):
    if url:
        st.write("Scraping the website...")

        # Scrape the website
        dom_content = scrape_website(url)
        if dom_content:  # Ensure dom_content is not None
            body_content = extract_body_content(dom_content)
            cleaned_content = clean_body_content(body_content)

            # Store the DOM content in Streamlit session state
            st.session_state.dom_content = cleaned_content

            # Display the DOM content in an expandable text box
            with st.expander("View DOM Content"):
                st.text_area("DOM Content", cleaned_content, height=300)
        else:
            st.write("Error: Unable to scrape the website. Please check the WebDriver configuration.")

# Step 2: Ask Questions About the DOM Content
if "dom_content" in st.session_state:
    parse_description = st.text_area("Describe what you want to parse")

    if st.button("Parse Content"):
        if parse_description:
            st.write("Parsing the content...")

            # Call the updated parse_with_ollama function directly
            parsed_result = parse_with_ollama(st.session_state.dom_content, parse_description)
            st.write(parsed_result)