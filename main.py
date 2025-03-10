import os
import json
from multiprocessing import Pool

from crawl.crawl_cvpr import crawl_cvpr
from search.search import Paper, Search
from tqdm import tqdm
from format.format_result import generate_markdown_table
from analysis.extract_github_url import extract_github_url


def search_paper(paper):
    paper = Paper(title=paper["paper_name"], authors=paper["author_names"])
    search = Search(paper)
    return search.search()


if __name__ == "__main__":
    cvpr_2025_url = "https://cvpr.thecvf.com/Conferences/2025/AcceptedPapers"

    ## collect all papers from CVPR 2025 website
    os.makedirs("output", exist_ok=True)
    save_path = "output/cvpr_2025_papers.json"
    if os.path.exists(save_path):
        with open(save_path, "r") as f:
            papers = json.load(f)
    else:
        papers = crawl_cvpr(cvpr_2025_url, save_path)

    ## search for each paper
    save_path = "output/cvpr_2025_search_results.json"
    valid_search_results_save_path = "output/cvpr_2025_valid_search_results.json"
    # papers = papers[:20]
    if os.path.exists(save_path):
        with open(save_path, "r") as f:
            search_results = json.load(f)
    else:
        # with Pool(2) as p:
        #     search_results = p.map(search_paper, papers)

        search_results = []
        json_save_dir = "output/cvpr_2025_search_results"
        os.makedirs(json_save_dir, exist_ok=True)
        for paper in tqdm(papers, total=len(papers)):
            save_paper_search_result_path = os.path.join(
                json_save_dir, f"{paper['paper_name'].replace('/', ' ')}.json"
            )
            if os.path.exists(save_paper_search_result_path):
                search_result = json.load(open(save_paper_search_result_path, "r"))
                search_results.append(search_result)
                continue
            else:
                search = Search(
                    Paper(title=paper["paper_name"], authors=paper["author_names"])
                )
                search_result = search.search()
                search_results.append(search_result)
                json.dump(
                    search_result, open(save_paper_search_result_path, "w"), indent=4
                )

        with open(save_path, "w") as f:
            json.dump(search_results, f, indent=4)

    # collect all valid search results
    if os.path.exists(valid_search_results_save_path):
        with open(valid_search_results_save_path, "r") as f:
            valid_search_results = json.load(f)
    else:
        valid_search_results = [result for result in search_results if result["valid"]]
    print(f"Total valid search results: {len(valid_search_results)}")

    if "github_links" not in valid_search_results[0]:
        save_pdf_dir = "output/pdf"
        os.makedirs(save_pdf_dir, exist_ok=True)
        with Pool(10) as p:
            github_links = p.map(extract_github_url, valid_search_results)
        for i, github_link in enumerate(github_links):
            valid_search_results[i]["github_links"] = github_link
        json.dump(
            valid_search_results, open(valid_search_results_save_path, "w"), indent=4
        )

    ## generate markdown table
    generate_markdown_table(valid_search_results)

