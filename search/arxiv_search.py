import re
import arxiv

# arxiv api documentation:
# element	explanation
# entry_id	A url http://arxiv.org/abs/{id}.
# updated	When the result was last updated.
# published	When the result was originally published.
# title	The title of the result.
# authors	The result's authors, as arxiv.Authors.
# summary	The result abstract.
# comment	The authors' comment if present.
# journal_ref	A journal reference if present.
# doi	A URL for the resolved DOI to an external resource if present.
# primary_category	The result's primary arXiv category. See arXiv: Category Taxonomy[4].
# categories	All of the result's categories. See arXiv: Category Taxonomy.
# links	Up to three URLs associated with this result, as arxiv.Links.
# pdf_url	A URL for the result's PDF if present. Note: this URL also appears among result.links.


# prefix	explanation
# ti	Title
# au	Author
# abs	Abstract
# co	Comment
# jr	Journal Reference
# cat	Subject Category
# rn	Report Number
# id	Id (use id_list instead)
# all	All of the above


def clean_text(text):
    # 使用正则表达式替换所有非字母、数字和空格的字符为''
    cleaned_text = re.sub(r"[^a-zA-Z0-9 ]", "", text)
    return cleaned_text


def search_paper(title, author, max_res=1, output_dir=None):
    """
    Search for a paper on arxiv using the title and author name.
    Args:
        title: str, the title of the paper.
        author: str, the author name of the paper.
        search_method: arxiv.SortCriterion, the sorting criterion for the search results.
            [arxiv.SortCriterion.SubmittedDate, arxiv.SortCriterion.Relevance,
            arxiv.SortCriterion.LastUpdatedDate]
        max_res: int, the maximum number of search results to return.
    """
    search_results = []
    query_str = "au:{} AND ti:{}".format(author, clean_text(title))

    search = arxiv.Search(query=query_str, max_results=max_res)

    try:
        _ = next(search.results())
    except StopIteration:
        return search_results

    for result in search.results():
        res = {}
        # res['entry_id'] = result.entry_id
        # res['updated'] = result.updated
        res["published"] = result.published.isoformat()
        res["title"] = result.title
        res["authors"] = [author.name for author in result.authors]
        res["abstract"] = result.summary
        # res['comment'] = result.comment
        # res['journal_ref'] = result.journal_ref
        res["doi"] = result.doi
        # res['primary_category'] = result.primary_category
        # res['categories'] = result.categories
        res["links"] = [link.href for link in result.links]
        res["pdf_url"] = result.pdf_url
        search_results.append(res)
        if output_dir:
            result.download_pdf(
                dirpath=output_dir, filename="{}.pdf".format(clean_text(res["title"]))
            )
    return search_results


if __name__ == "__main__":
    title = "A2XP: Towards Private Domain Generalization"
    author = "Geunhyeok Yu"
    search_results = search_paper(title, author, max_res=1)
    print(search_results)
