import pandas as pd


def custom_date_parser(date_str) -> pd.DatetimeIndex:
    cleaned_date_str = date_str.replace(" b", "").strip()
    return pd.to_datetime(cleaned_date_str, format='%d.%m.%Y %H:%M:%S')


def create_actuals(start_time, test_loads) -> pd.DataFrame:
    new_df = pd.DataFrame()
    dataset_id = 0

    while start_time <= test_loads.index[-1] - pd.Timedelta(hours=25):
        end_period = start_time + pd.Timedelta(hours=12) - pd.Timedelta(minutes=15)
        subset = test_loads[start_time:end_period].copy()
        subset['dataset_id'] = dataset_id
        new_df = pd.concat([new_df, subset])
        dataset_id += 1
        start_time += pd.Timedelta(hours=25)
    return new_df


def create_peak_actuals(thresholds, all_actuals) -> pd.DataFrame:
    peak_loads = all_actuals.copy()
    for load in [x for x in peak_loads.columns if x != 'dataset_id']:
        peak_loads[load] = peak_loads[load].apply(lambda x: 0 if x < thresholds[load] else x)
    return peak_loads


LOAD_FILE_2016 = 'LoadProfile_20IPs_2016.csv'
START_TIME_STAMP_2016 = pd.Timestamp('2016-09-01 00:00:00')
load_profiles_2016 = pd.read_csv(LOAD_FILE_2016, skiprows=1, delimiter=";", index_col=0, date_parser=custom_date_parser)
actuals_2016 = load_profiles_2016[load_profiles_2016.columns[13:]]
actuals_2016 = actuals_2016[START_TIME_STAMP_2016:]
actuals_2016 = create_actuals(START_TIME_STAMP_2016, actuals_2016)
actuals_2016.to_csv('2016_actuals.csv')
thresholds_2016 = load_profiles_2016.max() * 0.85
peak_actuals_2016 = create_peak_actuals(thresholds_2016, actuals_2016)
peak_actuals_2016.to_csv('2016_peak_actuals.csv')

LOAD_FILE_2017 = 'LoadProfile_30IPs_2017.csv'
START_TIME_STAMP_2017 = pd.Timestamp('2017-09-01 00:00:00')
load_profiles_2017 = pd.read_csv(LOAD_FILE_2017, skiprows=1, delimiter=";", index_col=0, date_parser=custom_date_parser)
load_profiles_2017 = load_profiles_2017.dropna()
actuals_2017 = load_profiles_2017[load_profiles_2017.columns[22:]]
actuals_2017 = actuals_2017[START_TIME_STAMP_2017:]
actuals_2017 = create_actuals(START_TIME_STAMP_2017, actuals_2017)
actuals_2017.to_csv('2017_actuals.csv')
thresholds_2017 = load_profiles_2017.max() * 0.85
peak_actuals_2017 = create_peak_actuals(thresholds_2017, actuals_2017)
peak_actuals_2017.to_csv('2017_peak_actuals.csv')
