from datasetLoader import DatasetLoader

loader = DatasetLoader()

claims = loader.load_all()

print(f"Claims Loaded : {len(claims)}")

for claim in claims:

    print(claim.claim_id)

    print(claim.ground_truth.expected_decision)