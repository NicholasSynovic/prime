from datetime import datetime
from typing import Any, NamedTuple

from pandas import DataFrame


class Revision(NamedTuple):
    """
    Represents a Git revision (commit) with detailed metadata.

    This named tuple holds information extracted from a version control commit,
    including authorship, commit metadata, parent relationships, and cryptographic
    signature information. It is used to structure and serialize commit data
    for further processing or database insertion.

    Attributes:
        author (str): Name of the commit author.
        author_email (str): Email address of the commit author.
        authored_datetime (datetime): Date and time the commit was authored (UTC).
        co_authors (list[str]): Names of co-authors listed in the commit.
        co_author_emails (list[str]): Email addresses of co-authors.
        commit_hash (str): SHA-1 hash identifying the commit.
        committed_datetime (datetime): Date and time the commit was committed (UTC).
        committer (str): Name of the person who committed the change.
        committer_email (str): Email address of the committer.
        encoding (str): Character encoding used for the commit message.
        message (str): Commit message content.
        gpgsign (str): GPG signature of the commit, if present.
        parents (list[str]): List of parent commit hashes.

    Properties:
        data (dict[str, Any]): Dictionary representation of the commit metadata.

    """

    author: str
    author_email: str
    authored_datetime: datetime
    co_authors: list[str]
    co_author_emails: list[str]
    commit_hash: str
    committed_datetime: datetime
    committer: str
    committer_email: str
    encoding: str
    message: str
    gpgsign: str
    parents: list[str]

    @property
    def data(self) -> dict[str, Any]:
        """
        Return a dictionary representation of the revision metadata.

        This property provides access to all fields of the `Revision` instance
        as a dictionary, mapping attribute names to their corresponding values.
        Useful for serialization or structured logging.

        Returns:
            dict[str, Any]: Dictionary containing all commit metadata fields.

        """
        return self._asdict()

    @property
    def dataframe(self) -> DataFrame:
        return DataFrame(data=self.data)
