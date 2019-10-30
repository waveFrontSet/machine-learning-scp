import argparse
import requests

from bs4 import BeautifulSoup


def construct_url(scp_number):
    return f"http://scp-wiki.net/scp-{scp_number:03d}"


def filter_for_page_content(page):
    return BeautifulSoup(page).find(name="div", attrs={"id": "page-content"})


def crawl_for(scp_number):
    url = construct_url(scp_number)
    response = requests.get(url)
    content = filter_for_page_content(response.text)
    return content


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--number",
        type=int,
        dest="scp_number",
        default=2,
        help="Number of the SCP article to obtain.",
    )
    args = parser.parse_args()
    print(crawl_for(args.scp_number))
