import requests
import os
import pdfplumber
import re

def download_file(url, save_file_path):
    """
    Download the file from the given URL and save it to the specified path.
    """
    response = requests.get(url)
    if response.status_code == 200:
        with open(save_file_path, 'wb') as f:
            f.write(response.content)
        print(f"File downloaded successfully and saved to {save_file_path}")
    else:
        print(f"Failed to download the file. Status code: {response.status_code}")

def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text

# 检测GitHub和Hugging Face链接
def detect_links(text):
    github_link_pattern = r"https?://github.com/[\w-]+/[\w-]+"
    github_io_link_pattern = r"https?://[\w-]+.github.io/[\w-]+"
    huggingface_link_pattern = r"https?://huggingface.co/[\w-]+/[\w-]+"
    github_links = re.findall(github_link_pattern, text)
    github_io_links = re.findall(github_io_link_pattern, text)
    huggingface_links = re.findall(huggingface_link_pattern, text)
    return github_links + github_io_links + huggingface_links


def extract_urls(valid_search_result):
    """
    Extract the urls from the given url.
    """
    save_pdf_path = os.path.join("output/pdf", f"{valid_search_result["paper_search"]["title"].replace("/", " ")}.pdf")
    if not os.path.exists(save_pdf_path):
        download_file(valid_search_result["paper_search"]["pdf_url"], save_pdf_path)
    text = extract_text_from_pdf(save_pdf_path)
    links = detect_links(text)
    return links

if __name__ == "__main__":
    pdf_path = "output/pdf/2406.10462v2.pdf"
    text = extract_text_from_pdf(pdf_path)
    links = detect_links(text)
    print(links)





    