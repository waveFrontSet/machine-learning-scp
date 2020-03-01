# -*- coding: utf-8 -*-
import click
import logging.config
import pandas as pd
from pathlib import Path
from src.data.article_data import Article


PROJECT_DIR = Path(__file__).resolve().parents[2]
logging.config.fileConfig(PROJECT_DIR / "logging_config.ini")
logger = logging.getLogger(__name__)


@click.command()
@click.argument("input_filepath", type=click.Path(exists=True))
@click.argument("output_filepath", type=click.Path())
def main(input_filepath, output_filepath):
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    logger.info("making final data set from raw data")
    df = pd.DataFrame({})
    for file in Path(input_filepath).glob("scp-*.txt"):
        logger.info("File: %s", file)
        with file.open() as f:
            try:
                article = Article.from_text(f.readlines())
            except ValueError as e:
                logger.warning("ValueError in file %s: %s", file, e)
                continue
        df = df.append(article.to_dict(), ignore_index=True)
    logger.info("DataFrame extracted. Writing to data.json in %s", output_filepath)
    df.to_json(Path(output_filepath) / "data.json")
    logger.info("Done.")


if __name__ == "__main__":
    main()
