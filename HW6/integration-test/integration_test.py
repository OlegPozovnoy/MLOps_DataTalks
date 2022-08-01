import os
import sys
from datetime import datetime
from dotenv import load_dotenv
import pandas as pd
# Append parent directory to import path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import batch


def dt(hour, minute, second=0) -> datetime:
    return datetime(2021, 1, 1, hour, minute, second)


def test_q5():
    data = [
        (None, None, dt(1, 2), dt(1, 10)),
        (1, 1, dt(1, 2), dt(1, 10)),
        (1, 1, dt(1, 2, 0), dt(1, 2, 50)),
        (1, 1, dt(1, 2, 0), dt(2, 2, 1)),
    ]

    columns = ['PUlocationID', 'DOlocationID', 'pickup_datetime', 'dropOff_datetime']
    df_input = pd.DataFrame(data, columns=columns)

    os.environ['INPUT_FILE_PATTERN'] = "s3://nyc-duration/in/{year:04d}-{month:02d}.parquet"
    input_file = batch.get_input_path(2021, 1)

    print("input_file:", input_file)

    df_input.to_parquet(
        input_file,
        engine='pyarrow',
        compression=None,
        index=False,
        storage_options={
            "client_kwargs": {
                'endpoint_url': 'http://localhost:4566'
            }
        },
    )


def test_q6():
    load_dotenv()
    os.system("python3 batch.py 2021 1")
    df = batch.read_data(batch.get_output_path(2021, 1))
    print("The sum of predicted durations for the test dataframe:", df.predicted_duration.sum())


test_q5()
test_q6()
