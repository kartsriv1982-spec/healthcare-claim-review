from pathlib import Path

def ensure_directory(path):

    Path(path).mkdir(

        parents=True,

        exist_ok=True

    )

def percentage(numerator, denominator):

    if denominator==0:

        return 0

    return round(

        numerator/denominator,

        4

    )