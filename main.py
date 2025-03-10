import os
import json
from multiprocessing import Pool

from crawl.crawl_cvpr import crawl_cvpr
from search.search import Paper, Search
from tqdm import tqdm

def search_paper(paper):
    paper = Paper(title=paper["paper_name"], authors=paper["author_names"])
    search = Search(paper)
    return search.search()

if __name__ == "__main__":
    cvpr_2025_url = "https://cvpr.thecvf.com/Conferences/2025/AcceptedPapers"

    ## collect all papers from CVPR 2025 website
    save_path = "output/cvpr_2025_papers.json"
    if os.path.exists(save_path):
        with open(save_path, "r") as f:
            papers = json.load(f)
    else:
        papers = crawl_cvpr(cvpr_2025_url, save_path)


    ## search for each paper
    save_path = "output/cvpr_2025_search_results.json"
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
            search = Search(Paper(title=paper["paper_name"], authors=paper["author_names"]))
            search_result = search.search()
            search_results.append(search_result)
            json.dump(search_result, open(os.path.join(json_save_dir, f"{paper['paper_name']}.json"), "w"), indent=4)

        with open(save_path, "w") as f:
            json.dump(search_results, f, indent=4)
    
    # collect all valid search results
    valid_search_results = [result for result in search_results if result["valid"]]
    print(f"Total valid search results: {len(valid_search_results)}")
    ss = 1

    



