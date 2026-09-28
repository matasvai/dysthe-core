import copy
import json
from pathlib import Path
import unittest
from dysthe_core import validate_case, validate_splits

class Contracts(unittest.TestCase):
    def setUp(self):
        self.case = json.loads((Path(__file__).parents[1] / 'examples/case.json').read_text())

    def test_example_and_refinements(self):
        validate_case(self.case)
        validate_splits([dict(case_id='coarse',initial_condition_id='a',split='train'),
                         dict(case_id='fine',initial_condition_id='a',split='train'),
                         dict(case_id='other',initial_condition_id='b',split='test')])

    def test_refined_copy_cannot_leak_into_test(self):
        with self.assertRaisesRegex(ValueError, 'leakage'):
            validate_splits([dict(case_id='coarse',initial_condition_id='a',split='train'),
                             dict(case_id='fine',initial_condition_id='a',split='test')])

    def test_invalid_physics_layout_and_time(self):
        for key, value in [('model_id','vlasov-poisson'), ('times',[0,0]),
                           ('times',[0,float('nan')]), ('axis_order',['t','v','x']),
                           ('shape',[True,16,16]), ('lengths',[20,-1,20])]:
            case = copy.deepcopy(self.case)
            case[key] = value
            with self.subTest(key=key, value=value), self.assertRaises(ValueError):
                validate_case(case)

    def test_duplicate_case_rejected(self):
        case = dict(case_id='same',initial_condition_id='a',split='train')
        with self.assertRaises(ValueError):
            validate_splits([case, case])
