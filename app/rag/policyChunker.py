import re

from langchain_core.documents import Document

def extract_plan_name(text):

    first_line = text.split("\n")[0]

    return first_line.replace(
        "PLAN",
        ""
    ).strip()

def get_section(
        text,
        start_marker,
        end_markers
):

    start = text.find(start_marker)

    if start == -1:
        return ""

    start += len(start_marker)

    end = len(text)

    for marker in end_markers:

        idx = text.find(marker, start)

        if idx != -1:
            end = min(end, idx)

    return text[start:end].strip()

def extract_plan_summary(text):

    markers = [
        "Covered Expenses",
        "Waiting Period",
        "Waiting Periods",
        "Human Review Threshold",
        "Exclusions"
    ]

    end = len(text)

    for marker in markers:

        idx = text.find(marker)

        if idx != -1:
            end = min(end, idx)

    return text[:end].strip()

def policy_coverage_chunking(
        documents
):

    text = "\n".join(
        d.page_content
        for d in documents
    )

    plan_name = extract_plan_name(
        text
    )

    chunks = []

    coverage = get_section(
        text,
        "Covered Expenses:",
        [
            "Waiting Period",
            "Waiting Periods",
            "Human Review Threshold",
            "Exclusions"
        ]
    )

    if coverage:

        chunks.append(
            Document(
                page_content=coverage,
                metadata={
                    "plan_name": plan_name,
                    "rule_type": "coverage",
                    "section": "covered_expenses"
                }
            )
        )
    exclusions = get_section(
        text,
        "Exclusions:",
        []
    )    

    if exclusions:

        exclusions_list = [
            e.strip()
            for e in exclusions.split(",")
            if e.strip()
        ]

    for exclusion in exclusions_list:

            chunks.append(
                Document(
                    page_content=exclusion,
                    metadata={
                        "plan_name": plan_name,
                        "rule_type": "exclusion",
                        "section": "exclusions",
                        "exclusion": exclusion
                    }
                )
            )    
    waiting = get_section(
        text,
        "Waiting Periods:",
        [
            "Human Review Threshold",
            "Exclusions"
        ]
    )    

    if not waiting:

        waiting = get_section(
            text,
            "Waiting Period:",
            [
                "Human Review Threshold",
                "Exclusions"
            ]
        )      
    for line in waiting.split("\n"):

        line = line.strip()

        if not line:
            continue

        match = re.search(
            r"(.+?)\s+(\d+)\s+months",
            line,
            re.IGNORECASE
        )    

        if match:

            condition = match.group(1).strip()

            months = int(
                match.group(2)
            )

            chunks.append(
                Document(
                    page_content=line,
                    metadata={
                        "plan_name": plan_name,
                        "rule_type":
                            "waiting_period",
                        "condition":
                            condition,
                        "months":
                            months
                    }
                )
            )             
    review = get_section(
        text,
        "Human Review Threshold:",
        [
            "Exclusions"
        ]
    )

    if review:

        amount_match = re.search(
            r"USD\s+([\d,]+)",
            review
        )

        threshold = None

        if amount_match:

            threshold = int(
                amount_match.group(1)
                .replace(",", "")
            )

        chunks.append(
            Document(
                page_content=review,
                metadata={
                    "plan_name": plan_name,
                    "rule_type":
                        "human_review",
                    "threshold":
                        threshold
                }
            )
        )

    
    plan_summary = extract_plan_summary(text)

    if plan_summary:

        chunks.append( Document(
            page_content=plan_summary,
            metadata={
                "plan_name": plan_name,
                "rule_type": "plan_summary",
                "section": "plan_summary"
            }
        )
    )    
    return chunks
        






