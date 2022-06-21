#!/usr/bin/env python
# coding: utf-8

import pickle
import pandas as pd
import sklearn
import argparse


categorical = ['PUlocationID', 'DOlocationID']


def read_data(filename):
    df = pd.read_parquet(filename)
    
    df['duration'] = df.dropOff_datetime - df.pickup_datetime
    df['duration'] = df.duration.dt.total_seconds() / 60

    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()

    df[categorical] = df[categorical].fillna(-1).astype('int').astype('str')
    
    return df


def main():
    parser = get_parser()
    args = parser.parse_args()
    year = args.year
    month = args.month

    with open('model.bin', 'rb') as f_in:
        dv, lr = pickle.load(f_in)

    df = read_data(f'https://nyc-tlc.s3.amazonaws.com/trip+data/fhv_tripdata_{year:04d}-{month:02d}.parquet')
    dicts = df[categorical].to_dict(orient='records')
    X_val = dv.transform(dicts)
    y_pred = lr.predict(X_val)
    print(y_pred.mean())

    df['ride_id'] = f'{year:04d}/{month:02d}_' + df.index.astype('str')
    df['ride_duration'] = y_pred
    df_result = df[['ride_id', 'ride_duration']]

    output_file = f'result_{year:04d}_{month:02d}.parquet'

    df_result.to_parquet(
        output_file,
        engine='pyarrow',
        compression=None,
        index=False
    )


def get_parser():
    """
    Creates a new argument parser.
    """
    parser = argparse.ArgumentParser('Data2TabShop')
    parser.add_argument('--year', '-y', dest='year', type=int, required=True)
    parser.add_argument('--month', '-m', dest='month', type=int, required=True)
    return parser


if __name__ == "__main__":
    main()

