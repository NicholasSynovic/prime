from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

from git import Repo
from pandas import DataFrame


class VersionControlSystem(ABC):
    """
    Abstract base class representing a version control system (VCS) interface.

    This class defines the structure and required methods for interacting with
    a version control repository. Subclasses must implement methods for
    repository initialization, revision extraction, revision parsing,
    release identification, and revision checkout.

    Attributes:
        repo_path (Path): The file system path to the repository.
        repo (Repo | Any): The initialized repository object.
        parseRevisionsBarMessage (str): Message to display when parsing
            revisions.

    Methods:
        _initialize_repo(): Initialize and return the repository object.
        get_revisions(): Return an iterable of commits and the total number of
            revisions.
        parse_revisions(revisions): Parse revisions into a structured DataFrame.
        get_release_revisions(): Extract and return release-related revisions.
        checkout_revision(revision_hash): Checkout a specific revision by its hash.
        checkout_most_recent_revision(): Checkout the most recent revision.

    """

    def __init__(self, repo_path: Path) -> None:
        """
        Initialize the VersionControlSystem object.

        Args:
            repo_path (Path): Path to the repository.

        """
        self.repo_path: Path = repo_path
        self.repo: Repo | Any = self._initialize_repo()
        self.parseRevisionsBarMessage: str = "Parsing revisions..."

    @abstractmethod
    def _initialize_repo(self) -> Any: ...  # noqa: ANN401

    @abstractmethod
    def get_revisions(self) -> tuple[Any, int]: ...  # noqa: D102

    @abstractmethod
    def parse_revisions(self, revisions: Any) -> DataFrame: ...  # noqa: D102, ANN401

    @abstractmethod
    def get_release_revisions(self) -> DataFrame: ...  # noqa: D102

    @abstractmethod
    def checkout_revision(self, revision_hash: str) -> None: ...  # noqa: D102

    @abstractmethod
    def checkout_most_recent_revision(self) -> None: ...  # noqa: D102
