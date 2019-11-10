import os
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
    paragraphs = raw_text.find_all("p", recursive=False)
    obj_class_p = next(p for p in paragraphs if "Object Class" in p.get_text())
    paragraphs.remove(obj_class_p)
    label = obj_class_p.contents[-1].strip().upper()
    return label, paragraphs


def write_to(f, label, paragraphs):
    f.write(label + "\n")
    for paragraph in paragraphs:
        f.write(paragraph.get_text() + "\n")


@click.command()
@click.argument("filepath", type=click.Path(exists=True))
@click.option("--lower", default=2, help="Lower bound of SCP articles to crawl")
@click.option("--upper", default=1000, help="Upper bound of SCP articles to crawl")
def crawl_for(lower, upper, filepath):
    for number in range(lower, upper):
        url = construct_url(number)
        response = requests.get(url)
        content = filter_for_page_content(response.text)
        label, paragraphs = split_into_label_and_text(content)
        with open(os.path.join(filepath, f"scp-{number:03d}.txt"), "w") as f:
            write_to(f, label, paragraphs)


if __name__ == "__main__":
    crawl_for()
