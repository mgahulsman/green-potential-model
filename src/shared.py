from pathlib import Path


class Paths:
    def __init__(self):
        self._dir_path: Path = Path.cwd()

    @property
    def raw(self) -> Path:
        return self._dir_path / "data" / "raw"

    @property
    def processed(self) -> Path:
        return self._dir_path / "data" / "processed"
