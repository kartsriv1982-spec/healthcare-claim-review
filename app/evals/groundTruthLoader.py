from pathlib import Path
import json

from config import GROUND_TRUTH_FOLDER
from models import GroundTruth

class GroundTruthLoader:

    def __init__(self):

        self.folder = GROUND_TRUTH_FOLDER

def load(self, claim_id: str) -> GroundTruth:

    file = self.folder / f"{claim_id}.json"

    if not file.exists():

        raise FileNotFoundError(file)

    with open(file, "r") as f:

        data = json.load(f)

    return GroundTruth(**data)

def load_all(self):

    gt = {}

    for file in self.folder.glob("*.json"):

        with open(file) as f:

            data = json.load(f)

        obj = GroundTruth(**data)

        gt[obj.claim_id] = obj

    return gt

def validate(self):

    files = list(self.folder.glob("*.json"))

    print(f"Loaded {len(files)} ground truth files.")

    for file in files:

        self.load(file.stem)

    print("Validation Successful")