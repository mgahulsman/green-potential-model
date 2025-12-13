from pathlib import Path


class Paths:
    def __init__(self):
        self.dir_path: Path = Path.cwd()

    @property
    def raw(self) -> Path:
        return self.dir_path / "data" / "raw"

    @property
    def processed(self) -> Path:
        return self.dir_path / "data" / "processed"
