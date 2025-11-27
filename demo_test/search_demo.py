# search_demo.py

"""
# 按关键词 + 分类
python search_demo.py \
  --keyword "large language model" \
  --categories cs.LG,cs.AI \
  --sort-by submittedDate \
  --sort-order descending \
  --date-mode submitted \
  --date-from 2024-01-01 \
  --max-results 5

"""

import argparse
from datetime import datetime
from arxiv_client import ArxivSearchParams, search_arxiv


def parse_date(s: str):
    return datetime.strptime(s, "%Y-%m-%d").date()


def main():
    parser = argparse.ArgumentParser(
        description="Lightweight arXiv search demo"
    )

    parser.add_argument("--keyword", type=str, default=None, help="all: keyword")
    parser.add_argument("--title", type=str, default=None, help="ti:")
    parser.add_argument("--abstract", type=str, default=None, help="abs:")
    parser.add_argument("--author", type=str, default=None, help="au:")
    parser.add_argument(
        "--categories",
        type=str,
        default=None,
        help="comma-separated categories, e.g. cs.LG,cs.AI",
    )
    parser.add_argument(
        "--date-mode",
        type=str,
        choices=["submitted", "updated"],
        default=None,
        help="Use submittedDate or lastUpdatedDate for range filter",
    )
    parser.add_argument(
        "--date-from",
        type=parse_date,
        default=None,
        help="Start date YYYY-MM-DD",
    )
    parser.add_argument(
        "--date-to",
        type=parse_date,
        default=None,
        help="End date YYYY-MM-DD",
    )
    parser.add_argument(
        "--sort-by",
        type=str,
        choices=["relevance", "submittedDate", "lastUpdatedDate"],
        default="relevance",
    )
    parser.add_argument(
        "--sort-order",
        type=str,
        choices=["ascending", "descending"],
        default="descending",
    )
    parser.add_argument(
        "--max-results",
        type=int,
        default=10,
        help="Max results (will be capped at 50)",
    )

    args = parser.parse_args()

    categories = (
        [c.strip() for c in args.categories.split(",") if c.strip()]
        if args.categories
        else None
    )

    params = ArxivSearchParams(
        all_terms=args.keyword,
        title=args.title,
        abstract=args.abstract,
        author=args.author,
        categories=categories,
        date_mode=args.date_mode,   # None / 'submitted' / 'updated'
        date_from=args.date_from,
        date_to=args.date_to,
        sort_by=args.sort_by,       # 'relevance' / 'submittedDate' / 'lastUpdatedDate'
        sort_order=args.sort_order, # 'ascending' / 'descending'
        max_results=args.max_results,
    )

    papers = search_arxiv(params)

    print(f"✅ Got {len(papers)} results.\n")
    for i, p in enumerate(papers, 1):
        print(f"[{i}] {p['title']}")
        print(f"    arXiv ID: {p['arxiv_id']}{' (' + p['version'] + ')' if p['version'] else ''}")
        print(f"    Authors : {', '.join(p['authors'])}")
        print(f"    Primary : {p['primary_category']}")
        print(f"    Cats    : {', '.join(p['categories'])}")
        print(f"    Published: {p['published']}")
        print(f"    Updated  : {p['updated']}")
        print(f"    PDF : {p['pdf_url']}")
        print(f"    ABS : {p['abs_url']}")
        if p['doi']:
            print(f"    DOI : {p['doi']}")
        if p['journal_ref']:
            print(f"    Journal: {p['journal_ref']}")
        print("    Summary:", (p['summary'][:200] + "...") if p['summary'] else "")
        print("-" * 80)


if __name__ == "__main__":
    main()
