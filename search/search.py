import re

from . import arxiv_search
from . import google_search

search_methods = {
    "arxiv": arxiv_search.search_paper,
    "google": google_search.search_paper,
}


def json2pd(json_data):
    results = []
    for data in json_data:
        res = {}
        for k, v in data.items():
            if isinstance(v, dict):
                for kk, vv in v.items():
                    res["{}_{}".format(kk, k)] = vv
            else:
                res[k] = v
        results.append(res)
    return results


class Paper:
    def __init__(
        self,
        title="",
        authors=[],
        abstract="",
        published="",
        doi="",
        links=[],
        pdf_url="",
    ):
        self.title = title
        self.authors = authors
        self.abstract = abstract
        self.published = published
        self.doi = doi
        self.links = links
        self.pdf_url = pdf_url


class Search:
    def __init__(self, paper_origin=Paper(), method="arxiv"):
        self.method = method
        self.search_paper = search_methods[method]
        self.paper_origin = paper_origin
        self.paper_search = Paper()

    @staticmethod
    def clean_text(text):
        cleaned_text = re.sub(r"[^a-zA-Z0-9 ]", "", text)
        return cleaned_text

    @classmethod
    def compare_text(cls, text1, text2):
        return (
            cls.clean_text(text1).strip().lower()
            == cls.clean_text(text2).strip().lower()
        )

    def is_search_valid(self):
        if self.compare_text(
            self.paper_origin.title, self.paper_search.title
        ) and self.compare_text(
            self.paper_origin.authors[0], self.paper_search.authors[0]
        ):
            return True
        return False

    def to_json(self, valid=False):
        return {
            "valid": valid,
            "paper_origin": {
                "title": self.paper_origin.title,
                "authors": self.paper_origin.authors,
                "abstract": self.paper_origin.abstract,
                "published": self.paper_origin.published,
                "doi": self.paper_origin.doi,
                "links": self.paper_origin.links,
                "pdf_url": self.paper_origin.pdf_url,
            },
            "paper_search": {
                "title": self.paper_search.title,
                "authors": self.paper_search.authors,
                "abstract": self.paper_search.abstract,
                "published": self.paper_search.published,
                "doi": self.paper_search.doi,
                "links": self.paper_search.links,
                "pdf_url": self.paper_search.pdf_url,
            },
        }

    def reset(self):
        self.paper_search = Paper()

    def search(self, max_res=1):
        search_results = self.search_paper(
            self.paper_origin.title, self.paper_origin.authors[0], max_res
        )
        if len(search_results) == 0:
            print("{} is not found".format(self.paper_origin.title))
            return self.to_json(valid=False)

        self.paper_search = Paper(**search_results[0])

        if not self.is_search_valid():
            # print(
            #     "Search result title is {} while the paper title is {}".format(
            #         self.paper_search.title, self.paper_origin.title
            #     )
            # )
            return self.to_json(valid=False)

        print("Search success")
        return self.to_json(valid=True)


if __name__ == "__main__":
    # paper = {
    #     "title": "Attention Is All You Need",
    #     "authors": ['Ashish Vaswani', 'Noam Shazeer', 'Niki Parmar', 'Jakob Uszkoreit', 'Llion Jones', 'Aidan N. Gomez', 'Lukasz Kaiser', 'Illia Polosukhin'],
    #     "pdf_url": ""
    # }

    # paper = {
    #     "title": "A2XP: Towards Private Domain Generalization",
    #     "authors": ["Geunhyeok Yu", "Hyoseok Hwang"],
    #     "pdf_url": ""
    # }

    paper = {
        "title": "VSRD: Instance-Aware Volumetric Silhouette Rendering for Weakly Supervised 3D Object Detection",
        "pdf_url": "",
        "authors": ["Zihua Liu", "Hiroki Sakuma", "Masatoshi Okutomi"],
    }

    paper_origin = Paper(**paper)
    search = Search(paper_origin=paper_origin, method="arxiv")
    res = search.search(max_res=1)
    print(res)