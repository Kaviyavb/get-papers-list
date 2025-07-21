import argparse
from get_papers_list.fetcher import search_pubmed, fetch_paper_details, parse_xml


def main():
    parser = argparse.ArgumentParser(description="Fetch PubMed papers with non-academic authors.")
    parser.add_argument('--query', type=str, required=True, help='PubMed search query')
    parser.add_argument('-f', '--file', type=str, help='Output CSV file (optional)')
    parser.add_argument('-d', '--debug', action='store_true', help='Enable debug output')

    args = parser.parse_args()

    if args.debug:
        print(f"🔍 Searching PubMed for: {args.query}")

    ids = search_pubmed(args.query)
    if args.debug:
        print(f"✅ Found {len(ids)} results")

    xml_data = fetch_paper_details(ids)
    df = parse_xml(xml_data)

    if args.file:
        df.to_csv(args.file, index=False)
        print(f"📁 Saved {len(df)} records to {args.file}")
    else:
        print(df.to_string(index=False))


if __name__ == '__main__':
    main()
