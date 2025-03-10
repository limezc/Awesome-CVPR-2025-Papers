import requests
from bs4 import BeautifulSoup
import json


def main(url):
    response = requests.get(url)
    papers = []
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        rows = soup.select('tr[style="background-color: #f3f3f3"]')
        for row in rows:
            try:
                first_td = row.find('td')
                if first_td:
                    strong_tag = first_td.find('strong')
                    a_tag = first_td.find('a')
                    if a_tag:
                        paper_name = a_tag.get_text(strip=True)
                        paper_url = a_tag['href']
                    elif strong_tag:
                        paper_name = strong_tag.get_text(strip=True)
                        paper_url = None
                    author_names = first_td.find('div').find('i').get_text(strip=True)
                    author_names = [name.strip() for name in author_names.split('·')]
                    papers.append({"paper_name": paper_name, "paper_url": paper_url, "author_names": author_names})
            except:
                print("Error while parsing the row")
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
    with open("cvpr_2025_papers.json", "w") as f:
        json.dump(papers, f, indent=4)
    
    print("Data saved to cvpr_2025_papers.json. Total papers found: ", len(papers))


if __name__ == "__main__":
    cvpr_2025_url = "https://cvpr.thecvf.com/Conferences/2025/AcceptedPapers"
    main(cvpr_2025_url)

