import pandas as pd 
from pathlib import Path

def load_in_csv_file(path_to_data: Path) -> pd.DataFrame:
    return pd.read_csv(path_to_data, engine="python")

def calculate_case_time(dates_case_recieved: pd.Series, dates_case_decision: pd.Series) -> pd.Series:
    start = pd.to_datetime(dates_case_recieved, errors="coerce")
    end = pd.to_datetime(dates_case_decision, errors="coerce")
    return (end - start).dt.days

def remove_negative_case_times_(dataset: pd.DataFrame, time_columns: list[str]) -> pd.DataFrame:
    mask = pd.Series(True, index=dataset.index)
    for col in time_columns:
        if col in dataset.columns:
            mask &= (dataset[col] > 0) | pd.isna(dataset[col])
    return dataset.loc[mask, :]

def remove_negative_case_times(dataset: pd.DataFrame) -> pd.DataFrame:
    dataset_with_case_time = dataset.copy()
    return dataset_with_case_time.loc[
        (dataset["decision_time_days"] > 0) | pd.isna(dataset["decision_time_days"]), :
    ]

def filter_by_assumptions(data: pd.DataFrame) -> pd.DataFrame:
    valid_avsluttet = data["avsluttet_dato"].isna() | (
        ~data["avsluttet_dato"].isna() & 
        (pd.to_datetime(data["avsluttet_dato"]) >= pd.to_datetime(data["vedtak_dato"]))
    )
    return data.loc[valid_avsluttet, :]

def filter_by_assumptions(data: pd.DataFrame) -> pd.DataFrame:
    today = pd.Timestamp("2026-03-11")
    
    #remove outlier 2124-08-29
    no_future_dates = (
        (pd.to_datetime(data["mottatt_dato"], errors="coerce") <= today) 
    )
    
    valid_avsluttet = data["avsluttet_dato"].isna() | (
        pd.to_datetime(data["avsluttet_dato"], errors="coerce") >= 
        pd.to_datetime(data["vedtak_dato"], errors="coerce")
    )
    return data.loc[valid_avsluttet & no_future_dates , :]

def get_time_frame(data: pd.DataFrame) -> None:
    first_case_received = pd.to_datetime(data["mottatt_dato"], errors="coerce").min()
    last_case_received = pd.to_datetime(data["mottatt_dato"], errors="coerce").max()
    first_case_approved = pd.to_datetime(data["vedtak_dato"], errors="coerce").min()
    last_case_approved = pd.to_datetime(data["vedtak_dato"], errors="coerce").max()
    first_case_closed = pd.to_datetime(data["avsluttet_dato"], errors="coerce").min()
    last_case_closed = pd.to_datetime(data["avsluttet_dato"], errors="coerce").max()

    print(f"Mottatt:    {first_case_received.date()} → {last_case_received.date()}")
    print(f"Vedtak:     {first_case_approved.date()} → {last_case_approved.date()}")
    print(f"Avsluttet:  {first_case_closed.date()} → {last_case_closed.date()}")


def get_recieved_cases_per_year(data: pd.DataFrame) -> list:
    years = pd.to_datetime(data["mottatt_dato"], errors="coerce").dt.year
    temp_df = pd.DataFrame({"years": years, "saksbehandler_id": data["saksbehandler_id"]})
    cases_per_year = []
    for year, group_year in temp_df.groupby("years"):
        cases_per_year.append({
            "year": year, 
            "total_cases_per_year": len(group_year), 
            "cases_per_worker_year": len(group_year) / len(set(group_year["saksbehandler_id"]))
        })
    return cases_per_year

def get_case_numbers(data: pd.DataFrame) -> None:
    print(f"Antall saker {len(data)}")
    print(f"Antall saker {len(set(data['saksbehandler_id']))}")
    print(f"Antall saker per saksbehandler {len(data)/len(set(data['saksbehandler_id']))}")

def get_age(data: pd.DataFrame) -> None:
    print(f"Average age {(data['alder'].mean())}")
    print(f"Min age: {data['alder'].min()}")
    print(f"Max age: {data['alder'].max()}")

def print_general_stats(data: pd.DataFrame) -> pd.DataFrame:
    _ = get_time_frame(data)
    _ = get_case_numbers(data)
    _ = get_age(data)
    return    