import math

import helper_functions


def main():
    positions = [{
        'x': 1,
        'y': 1,
        'target_x': 2,
        'target_y': 2,
        'expected': 45
    }, {
        'x': 2,
        'y': 2,
        'target_x': 1,
        'target_y': 1,
        'expected': -45
    }, {
        'x': 0,
        'y': 20,
        'target_x': 40,
        'target_y': 20,
        'expected': 180
    }, {
        'x': 20,
        'y': 20,
        'target_x': 0,
        'target_y': 0,
        'expected': -45
    }, {
        'x': 40,
        'y': 20,
        'target_x': 0,
        'target_y': 20,
        'expected': -180
    }]

    for test in positions:
        start = test['x'], test['y']
        end = test['target_x'], test['target_y']
        angle = math.degrees(helper_functions.angle_to(*start, *end))
        expected = test['expected']
        if not angle == expected:
            print(f'Got {angle}, expected {expected}')
        else:
            print('Passed')


if __name__ == '__main__':
    main()
