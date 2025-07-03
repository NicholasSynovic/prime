"""
Type checking for DataFrames.

Copyright (C) 2025 Nicholas M. Synovic.

"""

from datetime import datetime

from pydantic import BaseModel, Field


class ProjectProductivityPerCommit(BaseModel):
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
    start: datetime = Field(default=..., description="Starting datetime")
    end: datetime = Field(default=..., description="Ending datetime")
    open_events: int = Field(
        default=..., description="Number of open issues in the period"
    )


class PullRequestSpoilagePerDay(BaseModel):
    start: datetime = Field(default=..., description="Starting datetime")
    end: datetime = Field(default=..., description="Ending datetime")
    open_events: int = Field(
        default=..., description="Number of open pull requests in the period"
    )


class IssueDensityPerDay(BaseModel):
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
