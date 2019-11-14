Classifying SCP articles
==============================

This Machine Learning project aims at building a Machine Learning model that is
able to classify SCP articles by their Object Class.

About the accompanying blog posts
------------

This project is documented through various blog posts. At the moment, the
following have been written:
- <a href="https://paul-grillenberger.de/2019/11/10/a-machine-learning-project-classifying-scps-overview/">Overview</a>
- Building a web crawler

Furthermore, the git tags point at exercises and their solutions that are
referenced in the blog posts.

About SCPs
------------

The web site http://www.scp-wiki.net/ is a site for collaborative writing. The
fictional SCP (short for "Secure, Contain, Protect") foundation aims to contain
so-called SCPs that are anomalous fictional objects.

The articles about SCPs follow a fixed format that potentially makes it possible
to predict the Object Class from the article text.

Important make targets
------------

The following new or modified make targets are available.

- `make data/raw` - Executes the web crawler run to fetch data.
- `make clean` - Deletes compiled Python files and `__pycache__` directories (standard behavior) as well as log files (new behavior)


Project Organization
------------

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── make_dataset.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    │   │   ├── predict_model.py
    │   │   └── train_model.py
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │       └── visualize.py
    │
    └── tox.ini            <- tox file with settings for running tox; see tox.testrun.org


--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
