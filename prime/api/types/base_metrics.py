"""
Base metric types.

Copyright (C) 2025 Nicholas M. Synovic.

"""

from datetime import datetime

from pydantic import BaseModel, Field


class FileSizePerCommit(BaseModel):
    """
    A model representing the size of a file per commit.

    This model captures various metrics related to the size and composition
    of a file at the time of a specific commit.

    """

    language: str = Field(
        default=..., description="Identified programming language of the file"
    )
    provider: str = Field(default=..., description="Absolute filepath")
    lines: int = Field(default=..., description="Number of lines in the file")
    code: int = Field(default=..., description="Number of lines of code")
    comments: int = Field(default=..., description="Number of lines of comments")
    blanks: int = Field(default=..., description="Number of blank lines")
    bytes: int = Field(default=..., description="Number of bytes")
    commit_hash_id: int = Field(default=..., description="Commit hash ID from database")


class ProjectSizePerDay(BaseModel):
    """
    A model representing the project size metrics per day.

    This model captures the total size and composition of a project on a
    daily basis, including lines of code, comments, blanks, and bytes.

    """

    date: datetime = Field(default=..., description="Date of measurement")
    lines: int = Field(default=..., description="Total number of lines")
    code: int = Field(default=..., description="Total number of code lines")
    comments: int = Field(default=..., description="Total number of comment lines")
    blanks: int = Field(default=..., description="Total number of blank lines")
    bytes: int = Field(default=..., description="Total number of bytes")


class ProjectSizePerCommit(BaseModel):
    """
    A model representing the project size metrics per commit.

    This model captures the size and composition of a project at the time
    of a specific commit, including lines of code, comments, blanks, and bytes.

    """

    lines: int = Field(default=..., description="Number of lines in the project")
    code: int = Field(default=..., description="Number of lines of code")
    comments: int = Field(default=..., description="Number of lines of comments")
    blanks: int = Field(default=..., description="Number of blank lines")
    bytes: int = Field(default=..., description="Number of bytes")
    commit_hash_id: int = Field(default=..., description="Commit hash ID from database")


class CommitHashes(BaseModel):
    """
    Represents a commit hash of a specific commit.

    This model captures the commit hash between a release and the corresponding
    commit in the version control history.

    Attributes:
        commit_hash (str): Commit hash associated with a commit.

    """

    commit_hash: str = Field(default=..., description="Commit hash")


class Releases(BaseModel):
    """
    Represents a release entry linked to a specific commit.

    This model captures the relationship between a release and the corresponding
    commit hash in the version control history.

    Attributes:
        commit_hash_id (int): ID referencing the commit hash associated with the
            release.

    """

    commit_hash_id: int = Field(default=..., description="Revision hash")


class Authors(BaseModel):
    """
    Represents an author entity with name and email information.

    This model is used to store and validate data related to individuals
    who have authored commits in a version control system.

    Attributes:
        author (str): Name of the author.
        author_email (str): Email address of the author.

    """

    author: str = Field(default=..., description="Author name")
    author_email: str = Field(default=..., description="Author email")


class Committers(BaseModel):
    """
    Represents a committer entity with name and email information.

    This model is used to store and validate data related to individuals
    who have committed changes in a version control system.

    Attributes:
        committer (str): Name of the committer.
        committer_email (str): Email address of the committer.

    """

    committer: str = Field(default=..., description="Committer name")
    committer_email: str = Field(
        default=...,
        description="Committer email",
    )


class CommitLog(BaseModel):
    """
    Data model representing metadata for a single commit in a version control system.

    This model captures information about commit authorship, message content,
    associated signatures, and relationships to other commits or contributors.
    It is designed to support version control history analysis, contributor
    tracking, and auditing.

    Attributes:
        commit_hash_id (int): Index value referencing the related commit hash in
            the database.
        author_id (int): Index value referencing the author of the commit.
        committer_id (int): Index value referencing the committer of the commit.
        co_author_ids (str): JSON-encoded list of index values representing co-authors.
        parent_hash_ids (str): JSON-encoded list of index values representing parent
            commits.
        authored_datetime (datetime): UTC timestamp of when the commit was authored.
        committed_datetime (datetime): UTC timestamp of when the commit was committed.
        encoding (str): Character encoding used for the commit message.
        message (str): Full commit message as recorded in the version control system.
        gpgsign (str): GPG signature associated with the commit, if available.

    """

    commit_hash_id: int = Field(
        default=...,
        description="Index value of related commit hash",
    )
    author_id: int = Field(
        default=...,
        description="Index value of related author",
    )
    committer_id: int = Field(
        default=...,
        description="Index value of related committer",
    )
    co_author_ids: str = Field(
        default=...,
        description="JSON stringified index values of co-authors",
    )
    parent_hash_ids: str = Field(
        default=...,
        description="JSON stringified index values of parent hashes",
    )
    authored_datetime: datetime = Field(
        default=...,
        description="UTC datetime of when the commit was authored",
    )
    committed_datetime: datetime = Field(
        default=...,
        description="UTC datetime of when the commit was committed",
    )
    encoding: str = Field(default=..., description="Message encoding")
    message: str = Field(default=..., description="Commit message")
    gpgsign: str = Field(default=..., description="GPG signature")


class IssueIDs(BaseModel):
    """
    Pydantic model representing a GitHub issue ID.

    Attributes:
        issue_id (str): Unique identifier of the issue as returned by the GitHub
            GraphQL API.

    """

    issue_id: str = Field(default=..., description="Issue ID")


class Issues(BaseModel):
    """
    Pydantic model representing metadata for a GitHub issue.

    Attributes:
        issue_id_key (int): Index value of the related issue in the database.
        created_at (datetime): Datetime when the issue was created.
        closed_at (datetime): Datetime when the issue was closed.
        labels (str): Stringify JSON dict of issue labels {"labels": list[str]}

    """

    issue_id_key: int = Field(
        default=...,
        description="Index value of related issue",
    )
    created_at: datetime = Field(
        default=..., description="Datetime when an issue was created"
    )
    closed_at: datetime = Field(
        default=..., description="Datetime when an issue was closed"
    )
    labels: dict = Field(
        default=...,
        description='Stringify JSON dict of issue labels {"labels": list[str]}',
    )


class PullRequestIDs(BaseModel):
    """
    Pydantic model representing a GitHub pull request ID.

    Attributes:
        pull_request_id (str): Unique identifier of the pull request as returned
        by the GitHub GraphQL API.

    """

    pull_request_id: str = Field(default=..., description="Pull request ID")


class PullRequests(BaseModel):
    """
    Pydantic model representing metadata for a GitHub pull request.

    Attributes:
        pull_request_id_key (int): Index value of the related pull request in
            the database.
        created_at (datetime): Datetime when the pull request was created.
        closed_at (datetime): Datetime when the pull request was closed.

    """

    pull_request_id_key: int = Field(
        default=...,
        description="Index value of related pull request",
    )
    created_at: datetime = Field(
        default=..., description="Datetime when an pull request was created"
    )
    closed_at: datetime = Field(
        default=..., description="Datetime when an pull request was closed"
    )
