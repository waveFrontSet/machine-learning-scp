import click
import requests

from bs4 import BeautifulSoup


def construct_url(scp_number):
    return f"http://scp-wiki.net/scp-{scp_number:03d}"


def filter_for_page_content(page):
    return BeautifulSoup(page, features="html.parser").find(
        name="div", attrs={"id": "page-content"}
    )


def split_into_label_and_text(raw_text):
    paragraphs = raw_text.find_all("p")
    obj_class_p = next(p for p in paragraphs if "Object Class" in p.get_text())
    paragraphs.remove(obj_class_p)
    label = obj_class_p.contents[-1].strip().upper()
    return label, paragraphs


@click.command()
@click.option("--number", default=2, help="Number of the SCP article to obtain.")
def crawl_for(number):
    url = construct_url(number)
    response = requests.get(url)
    content = filter_for_page_content(response.text)
    click.echo(content)


if __name__ == "__main__":
    crawl_for()
