from itertools import repeat
from typing import NamedTuple, Self

from erdb.typing.models.correction_graph import CorrectionGraph
from erdb.typing.params import ParamRow
from erdb.typing.enums import ItemIDFlag
from erdb.typing.api_version import ApiVersion
from erdb.table._retrievers import ParamDictRetriever, RetrieverData
from erdb.table._common import RowPredicate, TableSpecContext


def calc_output(stage_min: float, stage_max: float, val_min: float, val_max: float, mult_val_min: float, mult_val_max: float, input_val: float) -> float:
    input_ratio = (input_val - stage_min) / (stage_max - stage_min)

    if mult_val_min > 0:
        growth_val = input_ratio ** mult_val_min
    else:
        growth_val = 1 - ((1 - input_ratio) ** abs(mult_val_min))

    return val_min + ((val_max - val_min) * growth_val)

class CorrectionRange(NamedTuple):
    threshold_left: int
    threshold_right: int
    coefficient_left: float
    coefficient_right: float
    adjustment: float

    def get_correction(self, level: int) -> float:
        """
        Calculate the correction value given level and CalcCorrectGraph, shamelessly stolen from:
        https://github.com/kingborehaha/CalcCorrectGraph-Calculation-Tool
        """
        level_ratio = (level - self.threshold_left) / (self.threshold_right - self.threshold_left)

        growth = \
            level_ratio ** self.adjustment \
            if self.adjustment > 0 else \
            1 - ((1 - level_ratio) ** abs(self.adjustment))

        return self.coefficient_left + ((self.coefficient_right - self.coefficient_left) * growth)

    @classmethod
    def from_row(cls, row: ParamRow, left: int, right: int) -> Self:
        return cls(
            row[f"stageMaxVal{left}"].as_int,
            row[f"stageMaxVal{right}"].as_int,
            row[f"stageMaxGrowVal{left}"].as_float,
            row[f"stageMaxGrowVal{right}"].as_float,
            row[f"adjPt_maxGrowVal{left}"].as_float,
        )

class CorrectionGraphTableSpec(TableSpecContext):
    model = {
        ApiVersion.VER_1: CorrectionGraph,
    }

    main_param_retriever = ParamDictRetriever("CalcCorrectGraph", ItemIDFlag.NON_EQUIPABBLE)

    predicates: list[RowPredicate] = [
        lambda row: row.index < 17
    ]

    @classmethod # override
    def get_pk(cls, data: RetrieverData, row: ParamRow) -> str:
        return str(row.index)

    @classmethod
    def make_object(cls, api: ApiVersion, data: RetrieverData, row: ParamRow):
        points = range(0, 5)
        points_shift = range(1, 5)
        ranges = [CorrectionRange.from_row(row, left, right) for left, right in zip(points, points_shift)]

        values: list[float] = [0.]

        for r in ranges:
            values += [r.get_correction(v) / 100.0 for v in range(r.threshold_left + 1, r.threshold_right + 1)]

        values += list(repeat(values[-1], 150 - len(values)))
        assert len(values) == 150, "Correction values length mismatch"

        # 0th index is not valid, add another 0 to offset
        return [0.] + values