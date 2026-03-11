import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path

def plot_status_pie(data: pd.DataFrame, path_to_plot: Path) -> None:
    status_counts = data["status"].value_counts()
    plt.figure(figsize=(8, 8))
    plt.pie(
        status_counts,
        labels=status_counts.index,
        autopct="%1.1f%%",
        startangle=90
    )
    plt.title("Fordeling av saksstatus")
    plt.tight_layout()
    plt.savefig(path_to_plot)

def plot_reason_closed_case_pie(data: pd.DataFrame, path_to_plot: Path) -> None:
    closed_cased = data.loc[data["status"] == "Avsluttet", :]
    aarsak_counts = closed_cased["avslutning_aarsak"].value_counts()
    plt.figure(figsize=(8, 8))
    plt.pie(
        aarsak_counts,
        labels=aarsak_counts.index,
        autopct="%1.1f%%",
        startangle=90
    )
    plt.title("Fordeling av saksstatus")
    plt.tight_layout()
    plt.savefig(path_to_plot)

def plot_case_time_by_saksbehandler(data: pd.DataFrame, path_to_plot: Path) -> None:
    closed = data.loc[data["status"] == "Avsluttet", :]

    groups = closed.groupby("saksbehandler_id")["decision_time_days"]
    labels = list(groups.groups.keys())
    values = [group.dropna().values for _, group in groups]

    plt.figure(figsize=(12, 6))
    plt.boxplot(values, labels=labels)
    plt.title("Saksbehandlingstid per saksbehandler")
    plt.xlabel("Saksbehandler")
    plt.ylabel("Saksbehandlingstid (dager)")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(path_to_plot)

def plot_case_time_by_fylke(data: pd.DataFrame, path_to_plot: Path) -> None:
    closed = data.loc[data["status"] == "Avsluttet", :]

    groups = data.groupby("fylke")["decision_time_days"]
    labels = list(groups.groups.keys())
    values = [group.dropna().values for _, group in groups]

    plt.figure(figsize=(12, 6))
    plt.boxplot(values, labels=labels)
    plt.title("Saksbehandlingstid per saksbehandler")
    plt.xlabel("Saksbehandler")
    plt.ylabel("Saksbehandlingstid (dager)")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(path_to_plot)

def plot_case_time_by_status(data: pd.DataFrame, path_to_plot: Path) -> None:
    status_groups = [
        group["decision_time_days"].dropna().values
        for _, group in data.groupby("status")
    ]
    labels = data["status"].unique()

    plt.figure(figsize=(10, 6))
    plt.boxplot(status_groups, labels=labels)
    plt.title("Saksbehandlingstid per avslutningsårsak")
    plt.xlabel("Status")
    plt.ylabel("Saksbehandlingstid (dager)")
    plt.tight_layout()
    plt.savefig(path_to_plot)

def plot_case_time_by_aarsak(data: pd.DataFrame, path_to_plot: Path) -> None:
    groups = data.groupby("avslutning_aarsak")["decision_time_days"]
    labels = list(groups.groups.keys())
    values = [group.dropna().values for _, group in groups]

    plt.figure(figsize=(10, 6))
    plt.boxplot(values, labels=labels)
    plt.title("Saksbehandlingstid per avslutningsårsak")
    plt.xlabel("Avslutningsårsak")
    plt.ylabel("Saksbehandlingstid (dager)")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(path_to_plot)

def plot_case_time_histogram(data: pd.DataFrame, path_to_plot: Path) -> None:
    plt.figure(figsize=(10, 6))
    plt.hist(data["total_time_days"].dropna(), bins=50, edgecolor="black")
    plt.title("Fordeling av totaltid")
    plt.xlabel("Totaltid (dager)")
    plt.ylabel("Antall saker")
    plt.tight_layout()
    plt.savefig(path_to_plot)


def plot_closure_reason_distribution(data: pd.DataFrame, path_to_plot: Path) -> None:
    closed = data.loc[data["status"] == "Avsluttet", :]
    counts = closed["avslutning_aarsak"].value_counts().sort_values()

    plt.figure(figsize=(10, 6))
    plt.barh(counts.index, counts.values)
    plt.title("Fordeling av avslutningsårsaker")
    plt.xlabel("Antall saker")
    plt.ylabel("Avslutningsårsak")
    plt.tight_layout()
    plt.savefig(path_to_plot)


def plot_cases_per_year(data: list[dict], path_to_plot: Path) -> None:
    years = [d["year"] for d in data]
    total = [d["total_cases_per_year"] for d in data]
    per_worker = [d["cases_per_worker_year"] for d in data]

    x = range(len(years))
    width = 0.25

    fig, ax1 = plt.subplots(figsize=(8, 5))

    bars1 = ax1.bar([i - width/2 for i in x], total, width=width, label="Totalt antall saker")
    bars2 = ax1.bar([i + width/2 for i in x], per_worker, width=width, label="Saker per saksbehandler")

    for bar in bars1:
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5,
                 str(int(bar.get_height())), ha="center", va="bottom", fontsize=9)

    for bar in bars2:
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5,
                 str(int(bar.get_height())), ha="center", va="bottom", fontsize=9)

    ax1.set_xticks(list(x))
    ax1.set_xticklabels(years)
    ax1.set_ylabel("Antall saker")
    ax1.set_title("Saker per år")
    ax1.legend()

    plt.tight_layout()
    plt.savefig(path_to_plot)