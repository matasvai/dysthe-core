"""Metadata checks cannot establish numerical accuracy or actual array contents."""
import math

MODEL_ID = 'optical-dysthe-127-v1'

def finite_number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)

def validate_case(case):
    if case.get('schema_version') != 1 or case.get('model_id') != MODEL_ID:
        raise ValueError('Unsupported schema or equation identity')
    if case.get('boundary') != 'periodic' or case.get('axis_order') != ['t', 'x', 'y', 'z']:
        raise ValueError('Expected periodic optical field layout [t,x,y,z]')
    if case.get('field_encoding') != 'complex128':
        raise ValueError('Reference fields must declare complex128')
    for key in ('case_id', 'initial_condition_id', 'family'):
        if not isinstance(case.get(key), str) or not case[key].strip():
            raise ValueError(f'Missing {key}')
    shape, lengths = case.get('shape', []), case.get('lengths', [])
    if len(shape) != 3 or any(type(n) is not int or n < 2 for n in shape):
        raise ValueError('Expected three positive grid sizes >= 2')
    if len(lengths) != 3 or any(not finite_number(x) or x <= 0 for x in lengths):
        raise ValueError('Expected three finite positive domain lengths')
    times = case.get('times', [])
    if len(times) < 2 or any(not finite_number(t) for t in times):
        raise ValueError('Expected at least two finite observation times')
    if times[0] != 0 or any(b <= a for a, b in zip(times, times[1:])):
        raise ValueError('Times must start at zero and increase strictly')
    physics = case.get('physics', {})
    if any(not finite_number(physics.get(k)) for k in ('epsilon1', 'epsilon2')):
        raise ValueError('Both physical coefficients must be finite')
    if physics['epsilon1'] <= 0:
        raise ValueError('This model convention requires epsilon1 > 0')

def validate_splits(records):
    """Keep every initial condition and its refinements in one data split.

    The producer must assign the same initial_condition_id to all variants of
    the same physical initial field. This check cannot discover mislabeled data.
    """
    if not records:
        raise ValueError('A split manifest cannot be empty')
    seen, groups = set(), {}
    for record in records:
        case_id, group, split = (record.get(k) for k in ('case_id', 'initial_condition_id', 'split'))
        if not isinstance(case_id, str) or not case_id or case_id in seen:
            raise ValueError('Case IDs must be nonempty and unique')
        if not isinstance(group, str) or not group or split not in {'train', 'validation', 'test'}:
            raise ValueError('Invalid initial-condition group or split')
        if group in groups and groups[group] != split:
            raise ValueError('Initial-condition leakage across splits')
        seen.add(case_id)
        groups[group] = split
