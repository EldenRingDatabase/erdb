from itertools import repeat
from typing import Dict, NamedTuple, Tuple
from scripts.er_params import ParamDict, ParamRow
from scripts.er_params.enums import ItemIDFlag
from scripts.erdb_common import get_schema_properties
from scripts.erdb_generators._base import GeneratorDataBase

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
    def from_row(cls, row: ParamRow, left: int, right: int) -> "CorrectionRange":
        return cls(
            row.get_int(f"stageMaxVal{left}"),
            row.get_int(f"stageMaxVal{right}"),
            row.get_float(f"stageMaxGrowVal{left}"),
            row.get_float(f"stageMaxGrowVal{right}"),
            row.get_float(f"adjPt_maxGrowVal{left}"),
        )

class CorrectionGraphGeneratorData(GeneratorDataBase):
    Base = GeneratorDataBase

    @staticmethod # override
    def output_file() -> str:
        return "correction-graph.json"

    @staticmethod # override
    def schema_file() -> str:
        return "correction-graph.schema.json"

    @staticmethod # override
    def element_name() -> str:
        return "CorrectionGraph"

    @staticmethod # override
    def get_key_name(row: ParamRow) -> str:
        return str(row.index)

    main_param_retriever = Base.ParamDictRetriever("CalcCorrectGraph", ItemIDFlag.NON_EQUIPABBLE)

    param_retrievers = {}
    msgs_retrievers = {}
    lookup_retrievers = {}

    @staticmethod
    def schema_retriever() -> Tuple[Dict, Dict[str, Dict]]:
        return get_schema_properties("correction-graph")

    def main_param_iterator(self, correct_graph: ParamDict):
        for index in range(0, 17):
            yield correct_graph[str(index)]

    def construct_object(self, row: ParamRow) -> Dict:
        points = range(0, 5)
        points_shift = range(1, 5)
        ranges = [CorrectionRange.from_row(row, left, right) for left, right in zip(points, points_shift)]

        values = [0]
        for r in ranges:
            values += [r.get_correction(v) / 100.0 for v in range(r.threshold_left + 1, r.threshold_right + 1)]
        values += repeat(values[-1], 150 - len(values))

        assert len(values) == 150, "Correction values length mismatch"

        return {str(i + 1): values[i] for i in range(0, 150)}