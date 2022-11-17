from typing import List, NamedTuple
import pytest

from erdb.typing.params import ParamDict
from erdb.utils.common import find_offset_indices


class ParamDictGenerator(NamedTuple):
    starting_element: int
    element_interval: int
    levels: List[int]
    level_interval: int

    def generate(self) -> ParamDict:
        def _rangec(start: int, count: int, step: int):
            return range(start, start + count * step, step)

        element_count = len(self.levels)
        element_range = _rangec(self.starting_element, element_count, self.element_interval)

        params: ParamDict = dict()

        for row_id, level_count in zip(element_range, self.levels):
            for offset in _rangec(0, level_count, self.level_interval):
                params[str(row_id + offset)] = {}

        return params

@pytest.mark.parametrize("starting_element,element_interval,levels,level_interval,results", [
    (1000, 100, [11, 26, 26], 1, [range(1000, 1011), range(1100, 1126), range(1200, 1226)]),
    (10000, 10000, [11, 1, 26], 100, [range(10000, 11001, 100), range(20000, 20001, 100), range(30000, 32501, 100)]),
])
def test_find_offset_indices(starting_element: int, element_interval: int, levels: List[int], level_interval: int, results):
    possible_maxima = list(set([l - 1 for l in levels]))
    params = ParamDictGenerator(starting_element, element_interval, levels, level_interval).generate()

    for element in range(len(levels)):
        base = starting_element + element * element_interval
        ids, levels = find_offset_indices(base, params, possible_maxima, level_interval)
        element_offset = starting_element + element_interval * element 

        assert list(results[element]) == list(ids)
        assert [index - element_offset for index in results[element]] == list(levels)