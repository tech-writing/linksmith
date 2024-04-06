import logging
import re
from pathlib import Path

import requests

logger = logging.getLogger(__name__)


class LocalObjectsInv:
    """
    Support discovering an `objects.inv` in current working directory.
    """

    # Candidate paths where to look for `objects.inv` in current working directory.
    objects_inv_candidates = [
        Path("objects.inv"),
        Path("doc") / "_build" / "objects.inv",
        Path("docs") / "_build" / "objects.inv",
        Path("doc") / "_build" / "html" / "objects.inv",
        Path("docs") / "_build" / "html" / "objects.inv",
        Path("doc") / "build" / "html" / "objects.inv",
        Path("docs") / "build" / "html" / "objects.inv",
    ]

    @classmethod
    def discover(cls, project_root: Path) -> Path:
        """
        Return `Path` instance of discovered `objects.inv` in current working directory.
        """
        for candidate in cls.objects_inv_candidates:
            path = project_root / candidate
            if path.exists():
                return path
        raise FileNotFoundError("No objects.inv found in working directory")


class RemoteObjectsInv:
    """
    Support discovering an `objects.inv` on Read the Docs.
    """

    HTTP_TIMEOUT = 5

    def __init__(self, project: str):
        self.project = project

    def discover(self) -> str:
        try:
            return self.discover_rtd()
        except FileNotFoundError:
            return self.discover_pypi()

    def discover_rtd(self) -> str:
        logger.info(f"Attempting to resolve project through RTD: {self.project}")
        try:
            result = requests.get(
                "https://readthedocs.org/api/v3/search/",
                params={"q": f"project:{self.project} *"},
                timeout=self.HTTP_TIMEOUT,
            ).json()["results"][0]
        except IndexError:
            raise FileNotFoundError(f"Project not found at Read the Docs: {self.project}")
        domain = result["domain"]
        path = result["path"]

        # No way to discover the language slot via API?
        # Derive `/en/latest/` into `/en/latest/objects.inv`. (requests)
        # Derive `/en/stable/examples.html` into `/en/stable/objects.inv`. (requests-cache)
        # Derive `/genindex.html` into `/objects.inv`. (cratedb-guide)
        # TODO: Also handle nested URLs like `/en/latest/snippets/myst/dropdown-group.html`.
        path = re.sub(r"(.*)/.*\.html?$", "\\1", path)

        rtd_url = f"{domain}/{path}"
        rtd_exists = requests.get(rtd_url, allow_redirects=True, timeout=self.HTTP_TIMEOUT).status_code == 200

        if rtd_exists:
            return rtd_url

        raise FileNotFoundError("No objects.inv discovered through Read the Docs")

    def discover_pypi(self) -> str:
        logger.info(f"Attempting to resolve project through PyPI: {self.project}")
        pypi_url = f"https://pypi.org/pypi/{self.project}/json"
        metadata = requests.get(pypi_url, timeout=self.HTTP_TIMEOUT).json()
        docs_url = metadata["info"]["docs_url"]
        home_page = metadata["info"]["home_page"]
        home_page2 = metadata["info"]["project_urls"]["Homepage"]
        for candidate in docs_url, home_page, home_page2:
            if candidate is None:
                continue
            objects_inv_candidate = f"{candidate.rstrip('/')}/objects.inv"
            try:
                objects_inv_status = requests.get(
                    objects_inv_candidate,
                    allow_redirects=True,
                    timeout=self.HTTP_TIMEOUT,
                ).status_code
                if objects_inv_status < 400:
                    return candidate
            except Exception:  # noqa: S110
                pass

        raise FileNotFoundError("No objects.inv discovered through PyPI")
