from pathlib import Path
from typing import List

from MetalSettings import MetalSettings


class InputFileLocator:
    """Znajduje foldery projektu: folder z plikiem .catnip lokalnie, /app w Dockerze; tworzy output i models."""

    def __init__(self, settings: MetalSettings):
        self.input_folder = settings.input_folder
        self.model_cache = settings.model_cache

    def locator(self) -> "InputFileLocator":
        return self

    def find_input(self, file_name: str) -> Path:
        candidates = []
        for root in self.project_roots():
            candidates += [root / self.input_folder / file_name, root / file_name]
        for candidate in candidates:
            if candidate.is_file():
                return candidate
        raise FileNotFoundError("Nie znaleziono %s w folderze '%s' obok pliku .catnip" % (file_name, self.input_folder))

    def output_folder(self) -> Path:
        folder = self.project_roots()[0] / "output"
        folder.mkdir(parents=True, exist_ok=True)
        return folder

    def model_folder(self) -> Path:
        folder = self.project_roots()[0] / self.model_cache
        folder.mkdir(parents=True, exist_ok=True)
        return folder

    @staticmethod
    def project_roots() -> List[Path]:
        """Foldery z plikiem .catnip najpierw; nigdy korzeń systemu (w Dockerze dirname('/app') == '/')."""
        here = Path(__file__).resolve().parent
        roots = []
        for folder in (Path.cwd(), here, here.parent):
            if folder not in roots and folder != Path(folder.anchor):
                roots.append(folder)
        return sorted(roots, key=lambda folder: not any(folder.glob("*.catnip")))
