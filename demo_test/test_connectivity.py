# test_connectivity.py
import arxiv


def main():
    print("⏳ Testing arXiv connectivity via python-arxiv ...")

    client = arxiv.Client(
        page_size=1,
        delay_seconds=3,
        num_retries=3,
    )

    search = arxiv.Search(
        query="all:electron",
        max_results=1,
    )

    try:
        result = next(client.results(search))
    except StopIteration:
        print("⚠️ arXiv returned no results.")
    except Exception as e:
        print("❌ Error when calling arXiv:", repr(e))
    else:
        print("✅ arXiv reachable.")
        print("   Title:", result.title)
        print("   PDF:", getattr(result, "pdf_url", None))


if __name__ == "__main__":
    main()
