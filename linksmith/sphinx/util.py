from pathlib import Path


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
