from pathlib import Path

from typing import List

from models import ClaimPackage

from config import DATASET_PATH

from groundTruthLoader import GroundTruthLoader

gt_loader = GroundTruthLoader()

class DatasetLoader:

    def __init__(self):

        self.dataset_root = DATASET_PATH

def get_categories(self):

    categories=[]

    for folder in self.dataset_root.iterdir():

        if folder.is_dir():

            categories.append(folder)

    return categories

def load_claim(

        self,

        claim_folder,

        category

):

    docs={}

    gt = self.gt_loader.load(claim_folder.name)


    for file in claim_folder.iterdir():

        if file.is_file():

            docs[file.name]=file

    return ClaimPackage(

        claim_id=claim_folder.name,

        category=category,

        folder=claim_folder,

        documents=docs,

         ground_truth=gt

    )

def load_all(self):

    claims=[]

    for category_folder in self.get_categories():

        category=category_folder.name

        for claim_folder in category_folder.iterdir():

            if claim_folder.is_dir():

                claims.append(

                    self.load_claim(

                        claim_folder,

                        category

                    )

                )

    return claims

def get_claim(

        self,

        claim_id

):

    claims=self.load_all()

    for claim in claims:

        if claim.claim_id==claim_id:

            return claim

    return None

def get_document(

        self,

        claim,

        name

):

    return claim.documents.get(name)

def dataset_summary(self):

    claims=self.load_all()

    print(

        "Total Claims:",

        len(claims)

    )

    approved=sum(

        1

        for c in claims

        if c.category=="approved"

    )

    fraud=sum(

        1

        for c in claims

        if c.category=="fraud"

    )

    nigo=sum(

        1

        for c in claims

        if c.category=="nigo"

    )

    print(

        approved,

        fraud,

        nigo

    )

