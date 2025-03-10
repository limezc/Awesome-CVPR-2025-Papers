import os
import json


def generate_markdown_table(papers_search_results):
    title_project = "# CVPR 2025 Papers"
    table_header = "| Title | Authors | Abstract | PDF URL |\n|-------|---------|----------|---------|\n"
    table_rows = []

    for data in papers_search_results:
        title = data["paper_search"]["title"]
        authors = ", ".join(data["paper_search"]["authors"])
        abstract = data["paper_search"]["abstract"].replace("\n", " ")
        pdf_url = data["paper_search"]["pdf_url"]
        table_rows.append(f"| {title} | {authors} | {abstract} | [Arxiv]({pdf_url}) |")

    table_content = title_project + "\n" + table_header + "\n".join(table_rows)
    with open("README.md", "w") as f:
        f.write(table_content)

    print("Markdown table saved to README.md")


if __name__ == "__main__":
    papers_search_results_file = "output/cvpr_2025_valid_search_results.json"
    with open(papers_search_results_file, "r") as f:
        papers_search_results = json.load(f)
    print(f"Total valid search results: {len(papers_search_results)}")

    generate_markdown_table(papers_search_results)


