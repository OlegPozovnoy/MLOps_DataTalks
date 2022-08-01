from datetime import datetime
from deepdiff import DeepDiff
import pandas as pd
from HW6 import batch


def dt(hour, minute, second=0) -> datetime:
    return datetime(2021, 1, 1, hour, minute, second)


def test_sample_input():
    data = [
        (None, None, dt(1, 2), dt(1, 10)),
        (1, 1, dt(1, 2), dt(1, 10)),
        (1, 1, dt(1, 2, 0), dt(1, 2, 50)),
        (1, 1, dt(1, 2, 0), dt(2, 2, 1)),
    ]

    print(data)
    columns = ['PUlocationID', 'DOlocationID', 'pickup_datetime', 'dropOff_datetime']
    df = pd.DataFrame(data, columns=columns)

    df_res = batch.prepare_data(df, columns)

    columns.append('duration')
    data_expect = [
        ("-1", "-1", dt(1, 2), dt(1, 10), 8.),
        ("1", "1", dt(1, 2), dt(1, 10), 8.),
    ]

    df_expect = pd.DataFrame(data_expect, columns=columns)
    df_expect[columns[:-1]] = df_expect[columns[:-1]].astype(int).astype('str')

    ddiff = DeepDiff(df_res.to_dict(), df_expect.to_dict(), significant_digits=3)
    print(f'diff = {ddiff}')

    assert ddiff == {}
