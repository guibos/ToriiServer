from src.domain.library_interface import LibraryInterface


class LibraryService:
    def __init__(self, library_repository: LibraryInterface):
        self.library_interface = library_repository

    def add_groups(self, *, group):
        pass
