import os
import click
import requests
import logging
import logging.config

from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


def construct_url(scp_number):
    return f"http://scp-wiki.net/scp-{scp_number:03d}"


def filter_for_page_content(page):
    return BeautifulSoup(page, features="html.parser").find(
        name="div", attrs={"id": "page-content"}
    )


def split_into_label_and_text(raw_text):
    paragraphs = raw_text.find_all("p", recursive=False)
    logger.debug("All paragraphs: %s", paragraphs)
    obj_class_p = next(p for p in paragraphs if "Object Class" in p.get_text())
    paragraphs.remove(obj_class_p)
    label = obj_class_p.contents[-1].strip().upper().replace(": ", "")
    return label, paragraphs


def write_to(f, label, paragraphs):
    f.write(label + "\n")
    for paragraph in paragraphs:
        f.write(paragraph.get_text() + "\n")


def crawl(filepath, number):
    logger.info("Crawling number %d", number)
    url = construct_url(number)
    logger.debug("URL: %s", url)
    response = requests.get(url)
    logger.debug("Response: %s", response.text)
    content = filter_for_page_content(response.text)
    logger.debug("Content: %s", content)
    try:
        label, paragraphs = split_into_label_and_text(content)
    except Exception:
        logger.exception("Exception when splitting for number %d", number)
        return
    logger.info("Identified label %s", label)
    logger.debug("Paragraphs: %s", paragraphs)
    if label not in ("SAFE", "EUCLID", "KETER"):
        logger.warn("Unknown label %s for number %d", label, number)
    with open(os.path.join(filepath, f"scp-{number:03d}.txt"), "w") as f:
        write_to(f, label, paragraphs)


@click.command()
@click.argument("filepath", type=click.Path(exists=True))
@click.option("--lower", default=2, help="Lower bound of SCP articles to crawl")
@click.option("--upper", default=1000, help="Upper bound of SCP articles to crawl")
@click.option("--max_workers", default=64, help="Max number of threads to use")
def crawl_for(max_workers, lower, upper, filepath):
    logger.debug(
        "Called with lower = %s, upper = %s, filepath = %s", lower, upper, filepath
    )
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        executor.map(
            crawl, (filepath for _ in range(lower, upper)), range(lower, upper)
        )
    logger.debug("End...")


if __name__ == "__main__":
    logging.config.fileConfig("logging_config.ini")
    logger.info("Start webcrawling...")
    crawl_for()
    logger.info("End webcrawling...")
