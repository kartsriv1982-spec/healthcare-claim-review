def route_validation(state):

    if state["is_valid"]:
        return "VALID"

    return "INVALID"