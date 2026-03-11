from pathlib import Path
import pandas as pd 
import matplotlib.pyplot as plt

from utils.transformations import load_in_csv_file, calculate_case_time, remove_negative_case_times, filter_by_assumptions, print_general_stats, get_recieved_cases_per_year
from utils.make_plots import plot_case_time_by_status, plot_case_time_by_fylke, plot_case_time_by_saksbehandler, plot_case_time_by_aarsak, plot_cases_per_year, plot_closure_reason_distribution, plot_reason_closed_case_pie, plot_case_time_histogram

def main():
    path_to_data = Path(__file__).parent / "data" / "aap_saker.csv"
    path_to_figures = Path(__file__).parent / "figures" 
    data = load_in_csv_file(path_to_data)
    
    data["decision_time_days"] = calculate_case_time(data["mottatt_dato"], data["vedtak_dato"])
    data["aap_duration_days"] = calculate_case_time(data["vedtak_dato"], data["avsluttet_dato"])
    data["total_time_days"] = calculate_case_time(data["mottatt_dato"], data["avsluttet_dato"])

    data_w_case_time = remove_negative_case_times(data)
    filtered_cases = filter_by_assumptions(data_w_case_time.copy())
    _ =  print_general_stats(filtered_cases)
    cases_per_year = get_recieved_cases_per_year(filtered_cases)
    closed = filtered_cases
    profile = closed.groupby("avslutning_aarsak").agg(
        antall=("sak_id", "count"),
        median_alder=("alder", "median"),
        median_beslutningstid=("decision_time_days", "median"),
        median_aap_varighet=("aap_duration_days", "median")
    ).round(1)
    print(profile)

    plot_cases_per_year(cases_per_year, path_to_figures / "cases_per_year.png")
    plot_case_time_histogram(filtered_cases, path_to_figures / "case_time_histogram.png")
    plot_closure_reason_distribution(filtered_cases, path_to_figures / "reason_closed_antall.png")
    plot_reason_closed_case_pie(filtered_cases, path_to_figures / "reason_closed_pie_diagram.png")

    plot_case_time_by_status(filtered_cases, path_to_figures / "ase_time_by_status.png")
    plot_case_time_by_fylke(filtered_cases, path_to_figures / "case_time_by_fylke.png")
    plot_case_time_by_saksbehandler(filtered_cases, path_to_figures / "case_time_by_saksbehandler.png")
    plot_case_time_by_aarsak(filtered_cases, path_to_figures / "case_time_by_aarsak.png")




if __name__ == "__main__":
    main()
