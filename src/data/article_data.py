import logging


logger = logging.getLogger(__name__)


class Article(object):
    """
    Holds the data of an SCP article.

    Attributes:
    - `label`: The Object Class of the SCP.
    - `name`: If present in the article, the SCP number.
    - `procedures`: The Special Containment Procedures part of the SCP article.
    - `desc`: The Description part of the SCP article.
    """

    ALLOWED_LABELS = ("SAFE", "EUCLID", "KETER")

    def __init__(self, label, name, procedures, desc):
        self.label = label.strip()
        self.name = name.strip()
        self.procedures = procedures.strip()
        self.desc = desc.strip()

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, orig_label):
        labels = [
            label for label in self.ALLOWED_LABELS if orig_label.startswith(label)
        ]
        if not labels:
            raise ValueError(f"Unknown label '{orig_label}'!")
        self._label = labels.pop()

    PROCEDURES_START = "Special Containment Procedures:"
    DESC_STARTS = ("Description:", "Summary:")

    @classmethod
    def _extract_procedures(cls, text):
        name, *rest_list = text.split(cls.PROCEDURES_START)
        rest = "".join(rest_list)
        if not rest:
            raise RuntimeError(f"Procedures could not be extracted from: {text}")
        return name, rest

    @classmethod
    def _extract_description(cls, rest):
        desc = None
        for desc_start in cls.DESC_STARTS:
            procedures, *desc_list = rest.split(desc_start)
            if desc_list:
                desc = "".join(desc_list)
                break
        if not desc:
            raise RuntimeError(f"Description could not be extracted from: {rest}")
        return procedures, desc

    @classmethod
    def from_text(cls, lines):
        """
        Constructs an SCP article object from the list of text `lines`.

        Arguments:
        - `lines`: List of strings containing the article.
        Returns:
        - `Article` object based on the text.
        """
        label, *text = lines
        text = "".join(text)
        name, rest = cls._extract_procedures(text)
        procedures, desc = cls._extract_description(rest)
        logger.debug("Procedures: %s, Desc: %s", procedures, desc)
        return cls(label, name, procedures, desc)

    def to_dict(self):
        """
        Turns the article into a dictionary.

        Each attribute becomes the value of a key which is the
        capitalized name of the attribute.
        """
        return {
            "Label": self.label,
            "Name": self.name,
            "Procedures": self.procedures,
            "Description": self.desc,
            "Procedures_Length": len(self.procedures),
            "Description_Length": len(self.desc),
            "Procedures_Description_Ratio": len(self.procedures) / len(self.desc)
            if len(self.desc) > 0
            else 0,
        }

    def __repr__(self):
        return (
            f"Article(label={self.label}, name={self.name}, "
            + "procedures={self.procedures}, desc={self.desc})"
        )
