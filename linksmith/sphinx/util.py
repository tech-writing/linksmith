import logging
import typing as t
from pathlib import Path

import requests
from dynamic_imports import import_module_attr

logger = logging.getLogger(__name__)


class LocalFileDiscoverer:
    """
    Support discovering a file in current working directory.
    """

    filename: str

    # Candidate paths where to look for file in current working directory.
    candidates: t.List[Path] = []

    @classmethod
    def discover(cls, project_root: Path) -> Path:
        """
        Return `Path` instance of discovered file in current working directory.
        """
        for candidate in [Path(".")] + cls.candidates:
            path = project_root / candidate / cls.filename
            if path.exists():
                return path
        raise FileNotFoundError(f"No {cls.filename} found in working directory")


class LocalObjectsInv(LocalFileDiscoverer):
    """
    Support discovering an `objects.inv` in current working directory.
    """

    # Designated file name.
    filename = "objects.inv"

    # Candidate paths.
    candidates = [
        Path("doc") / "_build",
        Path("docs") / "_build",
        Path("doc") / "_build" / "html",
        Path("docs") / "_build" / "html",
        Path("doc") / "build" / "html",
        Path("docs") / "build" / "html",
    ]


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
        logger.info(f"Attempting to resolve project through Read the Docs: {self.project}")
        try:
            result = requests.get(
                "https://readthedocs.org/api/v3/search/",
                params={"q": f"project:{self.project} *"},
                timeout=self.HTTP_TIMEOUT,
            ).json()["results"][0]
        except IndexError:
            raise FileNotFoundError(f"Project not found at Read the Docs: {self.project}")
        domain = result["domain"]
        response = requests.get(domain, allow_redirects=True, timeout=self.HTTP_TIMEOUT)
        rtd_url = response.url
        logger.info(f"Project found at Read the Docs: {rtd_url}")
        rtd_exists = requests.get(rtd_url, allow_redirects=True, timeout=self.HTTP_TIMEOUT).status_code == 200

        if rtd_exists:
            return rtd_url

        raise FileNotFoundError("No objects.inv discovered through Read the Docs")  # pragma: no cover

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


class LocalConfPy(LocalFileDiscoverer):
    """
    Support discovering a `conf.py` in current working directory.
    """

    # Designated file name.
    filename = "conf.py"

    # Candidate paths.
    candidates = [
        Path("doc"),
        Path("docs"),
    ]


def read_intersphinx_mapping_urls(conf_py: Path) -> t.List[str]:
    """
    Read `intersphinx_mapping` from `conf.py` and return list of URLs to `object.inv`.
    """
    urls = []
    intersphinx_mapping = import_module_attr(conf_py, "intersphinx_mapping")
    for item in intersphinx_mapping.values():
        urls.append(f"{item[0].rstrip('/')}/objects.inv")
    return urls
