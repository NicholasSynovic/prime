"""
Temporary plotting functionality for PRIME.

Copyright (C) 2025 Nicholas M. Synovic.

"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas import DataFrame

import prime.api.types as prime_types
from prime.api.db import DB


def plot_size(db: DB) -> None:
    """
    Plot the size per month from the database and save the plot as an image.

    Args:
        db (DB): The Database object used to read the project size data.

    """
    df: DataFrame = db.read_table(
        table="project_size_per_day",
        model=prime_types.T_ProjectSizePerDay,
    )
    data: DataFrame = df[["date", "code"]].copy()
    data["date"] = data["date"].apply(func=pd.Timestamp)
    data["date"] = data["date"].dt.strftime(date_format="%Y-%m")

    data = data.groupby(by="date").sum(numeric_only=True)
    data = data.reset_index()
    data["code"] /= 1000

    sns.lineplot(data=data, x="date", y="code")
    plt.title(label="Project Size per Month")
    plt.xlabel(xlabel="Month")
    plt.ylabel(ylabel="Size (KLOC)")

    # Show every 12 months
    xticks = data["date"][::12]  # every 12th label
    plt.xticks(ticks=range(0, len(data), 12), labels=xticks, rotation=45, ha="right")

    plt.tight_layout()
    plt.savefig("size.png")
    plt.clf()
    plt.close()


def plot_productivity(db: DB) -> None:
    """
    Plot the productivity per month from the database and save the plot as an image.

    Args:
        db (DB): The Database object used to read the project size data.

    """
    df: DataFrame = db.read_table(
        table="project_productivity_per_day",
        model=prime_types.T_ProjectProductivityPerDay,
    )
    data: DataFrame = df[["date", "delta_code"]].copy()
    data["date"] = data["date"].apply(func=pd.Timestamp)
    data["date"] = data["date"].dt.strftime(date_format="%Y-%m")

    data = data.groupby(by="date").sum(numeric_only=True)
    data = data.reset_index()

    sns.lineplot(data=data, x="date", y="delta_code")
    plt.title(label="Project Productivity per Month")
    plt.xlabel(xlabel="Month")
    plt.ylabel(ylabel="Productivity")

    # Show every 12 months
    xticks = data["date"][::12]  # every 12th label
    plt.xticks(ticks=range(0, len(data), 12), labels=xticks, rotation=45, ha="right")

    plt.tight_layout()
    plt.savefig("productivity.png")
    plt.clf()
    plt.close()


db_file: Path = Path("../.temp/tqdm_tqdm.prime.sqlite3")
db: DB = DB(db_path=db_file)
plot_productivity(db=db)
plot_size(db=db)
