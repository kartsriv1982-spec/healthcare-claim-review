import re


# ==================================================
# Mandatory Fields with Synonyms
# ==================================================

FIELD_PATTERNS = {

    "Patient Name": [

        r"Patient Name",

        r"Patient",

        r"Member Name",

        r"Insured Name",

        r"Beneficiary Name"

    ],

    "Policy Number": [

        r"Policy Number",

        r"Policy No",

        r"Policy ID",

        r"Member ID"

    ],

    "Hospital Name": [

        r"Hospital Name",

        r"Hospital",

        r"Medical Center",

        r"Healthcare Facility"

    ],

    "Admission Date": [

        r"Admission Date",

        r"Date of Admission"

    ],

    "Discharge Date": [

        r"Discharge Date",

        r"Date of Discharge"

    ],

    "Attending Doctor": [

        r"Attending Doctor",

        r"Treating Doctor",

        r"Consulting Doctor",

        r"Physician"

    ],

    "Diagnosis": [

        r"Diagnosis",

        r"Clinical Diagnosis"

    ],

    "Procedure": [

        r"Procedure",

        r"Treatment",

        r"Surgery"

    ]
}


# ==================================================
# Helper Functions
# ==================================================

def get_field_value(
    patterns,
    text
):

    """
    Returns the value for the first matching synonym.
    """

    for pattern in patterns:

        match = re.search(

            rf"{pattern}\s*:\s*(.+)",

            text,

            re.IGNORECASE

        )

        if match:

            return match.group(1).strip()

    return None


def is_missing(value):

    """
    Determines whether a field value is missing.
    """

    if value is None:

        return True

    value = value.strip().lower()

    invalid_values = [

        "",

        "not provided",

        "n/a",

        "na",

        "none",

        "-"

    ]

    return value in invalid_values


# ==================================================
# Validation Agent
# ==================================================

def validation_agent(state):

    text = state["ocr_text"]

    missing_fields = []

    print("=" * 60)
    print("VALIDATION AGENT STARTED")
    print("=" * 60)

    # ----------------------------------------------
    # Validate All Mandatory Fields
    # ----------------------------------------------

    for field_name, patterns in FIELD_PATTERNS.items():

        value = get_field_value(
            patterns,
            text
        )

        print(f"{field_name} : {value}")

        if is_missing(value):

            missing_fields.append(field_name)

    # ----------------------------------------------
    # Update State
    # ----------------------------------------------

    state["missing_fields"] = missing_fields

    state["is_valid"] = len(missing_fields) == 0

    if state["is_valid"]:

        state["validation_result"] = (
            "Validation Successful"
        )

    else:

        state["validation_result"] = (
            "Mandatory Fields Missing"
        )

    # ----------------------------------------------
    # Workflow Tracking
    # ----------------------------------------------

    if "workflow_steps" not in state:

        state["workflow_steps"] = []

    state["workflow_steps"].append(
        "Validation Completed"
    )

    print()

    print(f"Validation Status : {state['is_valid']}")

    print(f"Missing Fields : {missing_fields}")

    print("=" * 60)

    return state