from datetime import timezone
from pathlib import Path
from typing import Iterator

from git import Commit, Repo, TagReference
from pandas import DataFrame
from progress.bar import Bar

from prime.vcs.revision import Revision
from prime.vcs.vcs import VersionControlSystem


class Git(VersionControlSystem):
    """
    Git version control system interface.

    This class extends the VersionControlSystem base class to provide
    Git-specific functionality using the GitPython library. It supports
    operations such as retrieving commits, parsing revision metadata,
    identifying releases (tags), and checking out revisions.

    Attributes:
        repo_path (Path): Path to the Git repository.
        repo (Repo): GitPython `Repo` object for interacting with the repository.

    """

    def __init__(self, repo_path: Path) -> None:
        """
        Initialize the Git handler with the given repository path.

        Args:
            repo_path (Path): The file system path to the root of the repository.

        """
        super().__init__(repo_path=repo_path)
        self.repo.config_writer(config_level="repository").set_value(
            "core",
            "symlinks",
            "false",
        )

    def _initialize_repo(self) -> Repo:
        """
        Initialize and return a GitPython Repo object for the repository path.

        Returns:
            Repo: A GitPython `Repo` instance pointing to the specified repository.

        """
        return Repo(path=self.repo_path)

    def _extract_revision_hash_from_git_tag(
        self,
        git_tag: TagReference,
    ) -> str | None:
        """
        Extract the commit hash from a Git tag.

        Attempts to resolve the provided Git tag to its associated commit and
        return the commit hash. Returns None if the tag cannot be resolved.

        Args:
            git_tag (TagReference): A GitPython TagReference object.

        Returns:
            str | None: The commit hash (SHA-1) if resolvable, otherwise None.

        """
        try:
            return git_tag.commit.hexsha
        except ValueError:
            return None

    def get_revisions(self) -> tuple[Iterator[Commit], int]:
        """
        Retrieve an iterator of all commits along with the total count.

        Returns a tuple containing
        - An iterator over commits in chronological order (oldest to newest).
        - The total number of commits in the repository.

        Returns:
            tuple[Iterator[Commit], int]: A tuple of commit iterator and commit
            count.

        """
        revision_count: int = sum(1 for _ in self.repo.iter_commits())
        return (
            self.repo.iter_commits(
                reverse=True,
                date="raw",
            ),
            revision_count,
        )

    def parse_revisions(
        self,
        revisions: tuple[Iterator[Commit], int],
    ) -> DataFrame:
        """
        Parse a sequence of Git commits into a structured DataFrame.

        Iterates over a provided iterator of Git `Commit` objects, extracting relevant
        metadata from each commit such as author, committer, timestamps, GPG signature,
        commit message, parents, and co-authors. The data is structured into
        dictionaries and collected into a DataFrame. A progress bar is displayed
        during processing.

        Args:
            revisions (tuple[Iterator[Commit], int]): A tuple containing:
                - An iterator over `Commit` objects.
                - An integer representing the total number of revisions (for
                    progress bar tracking).

        Returns:
            DataFrame: A pandas DataFrame where each row represents a parsed commit with
            structured metadata fields.

        """
        data: list[dict] = []

        with Bar(
            self.parseRevisionsBarMessage,
            max=revisions[1],
        ) as bar:
            commit: Commit
            for commit in revisions[0]:
                data.append(
                    Revision(
                        author=commit.author.name,
                        author_email=commit.author.email,
                        authored_datetime=commit.authored_datetime.astimezone(
                            tz=timezone.utc
                        ),
                        co_authors=[co_author.name for co_author in commit.co_authors],
                        co_author_emails=[
                            co_author.email for co_author in commit.co_authors
                        ],
                        commit_hash=commit.hexsha,
                        committed_datetime=commit.committed_datetime.astimezone(
                            tz=timezone.utc
                        ),
                        committer=commit.committer.name,
                        committer_email=commit.committer.email,
                        encoding=commit.encoding,
                        gpgsign=commit.gpgsig,
                        message=commit.message,
                        parents=[parent.hexsha for parent in commit.parents],
                    ).data
                )
                bar.next()

        return DataFrame(data=data)

    def get_release_revisions(self) -> DataFrame:
        """
        Extract commit hashes associated with Git tags (releases).

        This method iterates through all tags in the repository, extracts the
        commit hash each tag points to (if valid), and returns them in a
        DataFrame under the column "commit_hash_id".

        Returns:
            DataFrame: A DataFrame containing a single column, "commit_hash_id",
            which lists the commit hashes corresponding to valid tags.

        """
        data: dict[str, list[str]] = {"commit_hash_id": []}

        tags: list[TagReference] = self.repo.tags
        tag_revision_hashes: map[str | None] = map(
            self._extract_revision_hash_from_git_tag, tags
        )

        # trh is an abbreviation for tag_revision_hash
        data["commit_hash_id"] = [trh for trh in tag_revision_hashes if trh is not None]

        return DataFrame(data=data)

    def checkout_revision(self, revision_hash: str) -> None:
        """
        Check out a specific commit in the repository by its hash.

        This method resolves the given commit hash and performs a Git checkout
        to switch the working directory to that commit.

        Args:
            revision_hash (str): The SHA-1 hash of the commit to check out.

        """
        commit: Commit = self.repo.commit(rev=revision_hash)
        self.repo.git.checkout(commit, force=True)

    def checkout_most_recent_revision(self) -> None:
        """
        Check out the most recent (HEAD) commit in the repository.

        Retrieves the latest commit hash from the current branch and checks it out
        using the `checkout_revision` method.

        """
        self.checkout_revision(revision_hash=self.repo.head.commit.hexsha)
