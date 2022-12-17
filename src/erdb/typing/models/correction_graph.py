from pydantic import NonNegativeFloat, ConstrainedList

"""
`conlist` cannot be used, otherwise model is not pickable.

Functional equivalent:
CorrectionGraph = conlist(NonNegativeFloat, min_items=151, max_items=151)
"""
class CorrectionGraph(ConstrainedList):
    item_type = NonNegativeFloat
    __args__ = (NonNegativeFloat,)
    min_items = 151
    max_items = 151