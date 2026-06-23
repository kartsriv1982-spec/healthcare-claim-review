# Simple Insurance Claim Processing — LangGraph

A beginner-friendly 3-agent LangGraph workflow. No RAG, no vector stores —
just three simple steps connected in a straight line.

```
OCR Agent  -->  Validation Agent  -->  Recommendation Agent
```

- **OCR Agent**: reads a claim image using AWS Textract, pulls out the raw text
  plus a claim number and claim amount.
- **Validation Agent**: checks the claim with simple if/else rules
  (fields present? amount under the limit?).
- **Recommendation Agent**: says APPROVE or REJECT based on the validation result, and can optionally use an OpenAI model for a more natural explanation.

## Project Structure

```
simple_insurance_claim/
├── Agents/
│   ├── OCR_Agent.py
│   ├── Validation_Agent.py
│   └── Recommendation.py
├── sample_claims/        # put a claim image here to test
├── langgraph_app.py       # builds and runs the graph
├── requirements.txt
└── .env.example
```

## Setup

```bash
python -m venv venv
source venv/bin/activate     # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

Fill in your AWS credentials in `.env` (needed for Textract OCR).
If you want the recommendation agent to use OpenAI, also add `OPENAI_API_KEY` (and optionally `OPENAI_MODEL`).

## Run it

```bash
python langgraph_app.py sample_claims/SampleInsuranceClaim.jpg
```

You'll see each agent print as it runs, then a final summary:
```
----- FINAL RESULT -----
Claim Number   : CLM-001
Claim Amount   : 45000
Is Valid       : True
Reasons        : []
Recommendation : APPROVE
Reasoning      : Claim passed all validation checks.
```

## How the graph works (langgraph_app.py)

1. `StateGraph` is created with a simple dictionary-like state (`ClaimState`).
2. Each agent is registered as a node: `workflow.add_node(name, function)`.
3. Nodes are connected in a straight line with `add_edge`.
4. `workflow.compile()` turns it into something you can call with `.invoke(...)`.

That's the whole pattern — once you're comfortable with this, you can add
more nodes, branches (`add_conditional_edges`), or loops later.

## Testing agents individually

```bash
python Agents/OCR_Agent.py sample_claims/SampleInsuranceClaim.jpg
python Agents/Validation_Agent.py
python Agents/Recommendation.py
```
