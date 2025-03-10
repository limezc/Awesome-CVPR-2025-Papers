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

# 检测GitHub链接
def detect_github_links(text):
    github_link_pattern = r"https?://github.com/[\w-]+/[\w-]+"
    return re.findall(github_link_pattern, text)


def extract_github_url(valid_search_result):
    """
    Extract the github url from the given url.
    """
    save_pdf_path = os.path.join("output/pdf", f"{valid_search_result["paper_search"]["title"].replace("/", " ")}.pdf")
    if not os.path.exists(save_pdf_path):
        download_file(valid_search_result["paper_search"]["pdf_url"], save_pdf_path)
    text = extract_text_from_pdf(save_pdf_path)
    github_links = detect_github_links(text)
    return github_links

if __name__ == "__main__":
    pdf_path = "output/pdf/2406.10462v2.pdf"
    text = extract_text_from_pdf(pdf_path)
    github_links = detect_github_links(text)
    print(github_links)





    