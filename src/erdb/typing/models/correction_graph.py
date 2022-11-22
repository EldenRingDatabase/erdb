from pydantic import NonNegativeFloat, conlist

CorrectionGraph = conlist(NonNegativeFloat, min_items=151, max_items=151)