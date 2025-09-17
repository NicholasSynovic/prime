import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas import DataFrame

from prime.api.db import DB
from prime.api.types import base_metrics, derived_metrics


class Plot:
    def __init__(self, db: DB) -> None:
        self.db: DB = db

    def issue_density_per_day(self) -> None:
        pass

    def issue_density_per_week(self) -> None:
        pass

    def issue_density_per_month(self) -> None:
        pass

    def issue_density_per_year(self) -> None:
        pass

    def issue_spoilage_per_day(self) -> None:
        pass

    def issue_spoilage_per_week(self) -> None:
        pass

    def issue_spoilage_per_month(self) -> None:
        pass

    def issue_spoilage_per_year(self) -> None:
        pass

    def project_productivity_per_day(self) -> None:
        pass

    def project_productivity_per_week(self) -> None:
        pass

    def project_productivity_per_month(self) -> None:
        pass

    def project_productivity_per_year(self) -> None:
        pass

    def project_size_per_day(self) -> None:
        pass

    def project_size_per_week(self) -> None:
        pass

    def project_size_per_month(self) -> None:
        pass

    def project_size_per_year(self) -> None:
        pass

    def pull_request_spoilage_per_day(self) -> None:
        pass

    def pull_request_spoilage_per_week(self) -> None:
        pass

    def pull_request_spoilage_per_month(self) -> None:
        pass

    def pull_request_spoilage_per_year(self) -> None:
        pass
