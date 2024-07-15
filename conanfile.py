from conans import ConanFile

import os


class Requirements(ConanFile):
    settings = "os", "arch", "compiler", "build_type"
    requires = (
        ("spdlog/1.8.5"),
        ("catch2/2.13.7"),
    )

    generators = "cmake"

    def configure(self):
        if self.settings.os == "Windows":
            self.options["spdlog"].wchar_support = True

    def imports(self):
        self.copy(
            "*.dll",
            os.path.join(os.path.dirname(__file__), "out", "bin"),
            keep_path=False,
        )

        self.copy(
            "*.dll",
            os.path.join(os.path.dirname(__file__), "build", "bin"),
            keep_path=False,
        )
