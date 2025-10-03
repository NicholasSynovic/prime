from pathlib import Path
from typing import Any

from git.exc import InvalidGitRepositoryError
from pandas import DataFrame

from prime.api.utils import (
    copy_dataframe_cols_and_remove_duplicate_rows_by_col,
    copy_dataframe_columns_to_dataframe,
    replace_dataframe_value_column_with_index_reference,
    replace_dataframe_value_column_with_index_reference_list,
)
from prime.vcs.git import Git
from prime.vcs.vcs import VersionControlSystem


def identify_vcs(repo_path: Path) -> VersionControlSystem | int:
    """
    Identify and return the version control system used at a given repository path.

    Attempts to initialize a Git repository at the specified path. If the path
    is not a valid Git repository, returns -1 to indicate failure.

    Args:
        repo_path (Path): The filesystem path to the repository.

    Returns:
        VersionControlSystem | int: An instance of a `VersionControlSystem` (e.g.,
        `Git`) if successful; otherwise, -1 if the repository is invalid or unsupported.

    """
    try:
        return Git(repo_path=repo_path)
    except InvalidGitRepositoryError:
        return -1


def parse_vcs(
    vcs: VersionControlSystem,
    existing_revision_hashes: DataFrame | None,
) -> dict[str, DataFrame]:
    """
    Parse and structure version control system data into normalized DataFrames.

    This function processes revision and release data from a version control
    system (VCS), filters out revisions that have already been processed, and
    normalizes the data by extracting static information (authors, committers,
    commit hashes) into separate DataFrames. It also replaces values in the
    commit and release logs with references to these static tables to support
    database-friendly indexing.

    Args:
        vcs (VersionControlSystem): The version control system instance to parse.
        existing_revision_hashes (DataFrame | None): Optional DataFrame of
            processed commit hashes to exclude from the current run.

    Returns:
        dict[str, DataFrame]: A dictionary of normalized DataFrames with the
        following keys:
            - "commit_hashes": Unique commit hashes.
            - "authors": Unique authors based on email.
            - "committers": Unique committers based on email.
            - "releases": Mapped and filtered release information.
            - "commit_logs": Normalized commit logs with references to static tables.

    """
    data: dict[str, DataFrame] = {}

    # Extract the commit log and release revisions
    revisions: tuple[Any, int] = vcs.get_revisions()
    releases_df: DataFrame = vcs.get_release_revisions()
    commit_log_df: DataFrame = vcs.parse_revisions(revisions=revisions)

    # Remove previously stored revisions from DataFrames
    if isinstance(existing_revision_hashes, DataFrame):
        commit_log_df = commit_log_df[
            ~commit_log_df["commit_hash"].isin(existing_revision_hashes["commit_hash"])
        ]
        releases_df = releases_df[
            ~releases_df["commit_hash_id"].isin(existing_revision_hashes["commit_hash"])
        ]

    # Copy static information to output data structure
    data["commit_hashes"] = copy_dataframe_columns_to_dataframe(
        df=commit_log_df,
        columns=["commit_hash"],
    )
    data["authors"] = copy_dataframe_cols_and_remove_duplicate_rows_by_col(
        df=commit_log_df,
        keep_columns=["author", "author_email"],
        unique_column="author_email",
    )
    data["committers"] = copy_dataframe_cols_and_remove_duplicate_rows_by_col(
        df=commit_log_df,
        keep_columns=["committer", "committer_email"],
        unique_column="committer_email",
    )

    # Replace commit log information with the index to static DataFrames
    releases_df = replace_dataframe_value_column_with_index_reference(
        df_1=releases_df,
        df_2=data["commit_hashes"],
        df_1_col="commit_hash_id",
        df_2_col="commit_hash",
    )
    releases_df = releases_df.dropna(how="any", ignore_index=True)
    releases_df["commit_hash_id"] = releases_df["commit_hash_id"].apply(int)

    commit_log_df = replace_dataframe_value_column_with_index_reference(
        df_1=commit_log_df,
        df_2=data["commit_hashes"],
        df_1_col="commit_hash",
        df_2_col="commit_hash",
    )
    commit_log_df = replace_dataframe_value_column_with_index_reference(
        df_1=commit_log_df,
        df_2=data["authors"],
        df_1_col="author_email",
        df_2_col="author_email",
    )
    commit_log_df = replace_dataframe_value_column_with_index_reference(
        df_1=commit_log_df,
        df_2=data["committers"],
        df_1_col="committer_email",
        df_2_col="committer_email",
    )

    # Replace commit log information with a list of indicies from static
    # DataFrames
    commit_log_df = replace_dataframe_value_column_with_index_reference_list(
        df_1=commit_log_df,
        df_2=data["authors"],
        df_1_col="co_author_emails",
        df_2_col="author_email",
    )
    commit_log_df = replace_dataframe_value_column_with_index_reference_list(
        df_1=commit_log_df,
        df_2=data["commit_hashes"],
        df_1_col="parents",
        df_2_col="commit_hash",
    )

    # Drop irrelevant columns and rename existing columns to match database
    # schema
    commit_log_df = commit_log_df.drop(
        columns=["author", "committer", "co_authors"],
    )
    commit_log_df = commit_log_df.rename(
        columns={
            "author_email": "author_id",
            "co_author_emails": "co_author_ids",
            "commit_hash": "commit_hash_id",
            "committer_email": "committer_id",
            "parents": "parent_hash_ids",
        },
    )

    data["releases"] = releases_df
    data["commit_logs"] = commit_log_df

    return data
