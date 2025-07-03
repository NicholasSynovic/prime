"""
Base metric types.

Copyright (C) 2025 Nicholas M. Synovic.

"""

from datetime import datetime

from pydantic import BaseModel, Field


class ProjectProductivityPerCommit(BaseModel):
    """
    A model representing the productivity metrics per commit.

    This model captures the changes in various metrics such as lines of code,
    comments, blanks, and bytes for a specific commit.
    """

    commit_hash_id: int = Field(default=..., description="Commit hash ID from database")
    delta_lines: int = Field(default=..., description="Change in total number of lines")
    delta_code: int = Field(
        default=..., description="Change in total number of code lines"
    )
    delta_comments: int = Field(
        default=..., description="Change in total number of comment lines"
    )
    delta_blanks: int = Field(
        default=..., description="Change in total number of blank lines"
    )
    delta_bytes: int = Field(default=..., description="Change in total number of bytes")


class ProjectProductivityPerDay(BaseModel):
    """
    A model representing the productivity metrics per day.

    This model captures the daily changes in various metrics such as lines of code,
    comments, blanks, and bytes.
    """

    date: datetime = Field(default=..., description="Date of measurement")
    delta_lines: int = Field(default=..., description="Change in total number of lines")
    delta_code: int = Field(
        default=..., description="Change in total number of code lines"
    )
    delta_comments: int = Field(
        default=..., description="Change in total number of comment lines"
    )
    delta_blanks: int = Field(
        default=..., description="Change in total number of blank lines"
    )
    delta_bytes: int = Field(default=..., description="Change in total number of bytes")


class BusFactorPerDay(BaseModel):
    """
    A model representing the bus factor metrics per day.

    This model captures the daily changes in various metrics attributed to a
    specific committer.
    """

    date: datetime = Field(default=..., description="Date of measurement")
    committer_id: int = Field(default=..., description="Committer ID")
    delta_lines: int = Field(default=..., description="Change in total number of lines")
    delta_code: int = Field(
        default=..., description="Change in total number of code lines"
    )
    delta_comments: int = Field(
        default=..., description="Change in total number of comment lines"
    )
    delta_blanks: int = Field(
        default=..., description="Change in total number of blank lines"
    )
    delta_bytes: int = Field(default=..., description="Change in total number of bytes")


class IssueSpoilagePerDay(BaseModel):
    """
    A model representing the issue spoilage metrics per day.

    This model captures the number of open issues within a specific time period.
    """

    start: datetime = Field(default=..., description="Starting datetime")
    end: datetime = Field(default=..., description="Ending datetime")
    open_events: int = Field(
        default=..., description="Number of open issues in the period"
    )


class PullRequestSpoilagePerDay(BaseModel):
    """
    A model representing the pull request spoilage metrics per day.

    This model captures the number of open pull requests within a specific time period.
    """

    start: datetime = Field(default=..., description="Starting datetime")
    end: datetime = Field(default=..., description="Ending datetime")
    open_events: int = Field(
        default=..., description="Number of open pull requests in the period"
    )


class IssueDensityPerDay(BaseModel):
    """
    A model representing the issue density metrics per day.

    This model captures the number of open issues and the total size metrics of
    the project within a specific time period.
    """

    start: datetime = Field(default=..., description="Starting datetime")
    end: datetime = Field(default=..., description="Ending datetime")
    open_events: int = Field(
        default=..., description="Number of open issues in the period"
    )
    lines: int = Field(default=..., description="Total number of lines")
    code: int = Field(default=..., description="Total number of code lines")
    comments: int = Field(default=..., description="Total number of comment lines")
    blanks: int = Field(default=..., description="Total number of blank lines")
    bytes: int = Field(default=..., description="Total number of bytes")
