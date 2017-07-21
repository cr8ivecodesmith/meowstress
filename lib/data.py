import csv
import os

from . import LIB_PATH


def _read_skill_data(data_csv):
    dataset = []
    with open(data_csv) as fh:
        rows = csv.DictReader(fh, delimiter=',', quotechar='"')
        for row in rows:
            row = {k: float(v) if '_chance' in k else v
                   for k, v in row.items()}
            row = {k: int(v) if k == 'cost' else v
                   for k, v in row.items()}
            dataset.append(row)
        return dataset


PALICO_CLASSES = [
    'charisma',
    'fighting',
    'protection',
    'assisting',
    'healing',
    'bombing',
    'gathering',
]

SKILL_DATA = _read_skill_data(os.path.join(LIB_PATH, 'skill_data.csv'))

SKILL_COMBOS = [
    ['A', 'B', 'B', 'C'],
    ['A', 'B', 'C', 'C', 'C'],
    ['A', 'C', 'C', 'C', 'C', 'C'],
    ['B', 'B', 'B', 'B'],
    ['B', 'B', 'B', 'C', 'C'],
    ['B', 'B', 'C', 'C', 'C', 'C'],
    ['C', 'C', 'C', 'C', 'C', 'C', 'C', 'C'],
]

SKILL_COMBOS_CHARISMA = [['A', 'B', 'B', 'B']] + [i + ['C']
                                                  for i in SKILL_COMBOS]
