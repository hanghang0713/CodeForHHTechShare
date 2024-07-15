#!/usr/bin/env python3
"""Build and Test Tools

Usage:
  build-and-test.py [build] [test] [options]
  build-and-test.py (-h | --help)
  build-and-test.py --version

Subcommands:
  build                 build only
  test                  test only

Options:
  --conan                   Install conan package
  --32                      Build X86, build X86_64 by default
  --release                 Build Release, build Debug by default
  --ninja                   Use Ninja CMake Generator, Visual studio Generator by Default
  --clean                   Clean build
  --install                 Install after build
  --coverage                Run OpenCppCoverage, you must install OpenCppCoverage first
  --check                   Run static check
  --coverage_cobertura      Output Cobertura XML
  --coverage_ignore=<cig>   Ignore coverage files: e.g. D:\*
  --build-test              Build Unit Test
  --19                      Deprecated, only 2019 now
  --gui                     Deprecated, use --build-tools --build-test instead.
  -t TAG                    Special catch2 TAG
  -r REPEAT                 Test repeat nums
  -h --help                 Show this screen
  --version                 Show version

"""

import os
import sys
import re
import shutil
import platform
from docopt import docopt


def read_version_from_properties(versionfile):
    with open(versionfile) as version:
        properties = {}
        for line in version:
            x, y = line.strip().split("=")
            properties[x] = y

        build_version = "0"
        return "U.{}.{}.{}.{}".format(
            properties["MAJOR_VERSION"],
            properties["MINOR_VERSION"],
            properties["PATCH_VERSION"],
            build_version,
        )


def border_msg(msg):
    count = len(msg) + 2  # dash will need +2 too
    dash = "*" * count

    print("*{}*".format(dash))
    print("* {} *".format(msg))
    print("*{}*".format(dash))


def run_and_echo(cmd):
    border_msg(cmd)
    if not os.system(cmd) == 0:
        sys.exit(-1)


def init_environ():
    if "CAMERA_CASCADE_VERSION" not in os.environ:
        os.environ["CAMERA_CASCADE_VERSION"] = read_version_from_properties(
            "version.properties"
        )

    if "CAMERA_CASCADE_VERSION" not in os.environ:
        os.environ["CAMERA_CASCADE_VERSION"] = read_version_from_properties(
            "tools/udi-debug-gui/version.properties"
        )

    if sys.platform != "win32" and "SELF_UPGRADE" not in os.environ:
        os.environ["SELF_UPGRADE"] = "0"


def create_build_path(arguments):
    build_path = os.path.join(os.getcwd(), "build")

    if arguments["--clean"]:
        shutil.rmtree(build_path, ignore_errors=True)
        arguments["--conan"] = True

    if not os.path.exists(build_path):
        os.mkdir(build_path)

    return build_path


def install_conan_packages(arguments, build_path):
    if not arguments["--conan"]:
        return

    install_path = os.path.join(build_path)
    source_path = os.getcwd()

    install_command = "conan install {} --build missing -if {}".format(
        source_path, install_path
    )

    if arguments["--release"]:
        install_command += " -s build_type=Release"
    else:
        install_command += " -s build_type=Debug"

    if platform.machine() != "aarch64":
        if arguments["--32"]:
            install_command += " -s arch=x86"
        else:
            install_command += " -s arch=x86_64"

    # windows only settings
    if sys.platform == "win32":
        if arguments["--release"]:
            install_command += " -s compiler.runtime=MT"
        else:
            install_command += " -s compiler.runtime=MTd"

        install_command += " -s compiler.version=16"

    run_and_echo(install_command)


def get_cmake_generator(arguments):
    if arguments["--ninja"]:
        return '-G "Ninja"'

    if not sys.platform == "win32":
        return '-G "Unix Makefiles"'

    if arguments["--32"]:
        return '-G "Visual Studio 16 2019" -A Win32'
    else:
        return '-G "Visual Studio 16 2019" -A x64'


def generate_build_script(arguments, build_path):
    cmake_generator = get_cmake_generator(arguments)

    source_path = os.getcwd()
    cmake_command = "cmake {} -B {} -S {}".format(
        cmake_generator, build_path, source_path
    )

    if arguments["--release"]:
        cmake_command += " -DCMAKE_BUILD_TYPE=Release"
    else:
        cmake_command += " -DCMAKE_BUILD_TYPE=Debug"

    if arguments["--build-test"]:
        cmake_command += " -DBUILD_TESTS=ON"

    if arguments["--check"]:
        cmake_command += " -STATIC_CHECK=ON"

    run_and_echo(cmake_command)


def build_project(arguments, build_path):
    cmake_command = "cmake --build {} -j 4".format(build_path)

    if arguments["--release"]:
        cmake_command += " --config Release"
    else:
        cmake_command += " --config Debug"

    if arguments["--install"]:
        cmake_command += " --target install"

    run_and_echo(cmake_command)


def build_application(arguments, build_path):
    if arguments["--conan"]:
        install_conan_packages(arguments, build_path)

    generate_build_script(arguments, build_path)
    build_project(arguments, build_path)


def print_html_coverage(index_html):
    with open(index_html, "r", encoding="utf-8") as ifile:
        for line in ifile:
            match = re.search(r"'labels', (\['Cover \d+%','Uncover \d+%'\])", line)
            if not match:
                continue

            return border_msg(match[1])


def print_xml_coverage(xml):
    with open(xml, "r", encoding="utf-8") as ifile:
        for line in ifile:
            match = re.search(r'line-rate="(0\.\d+)"', line)
            if not match:
                continue
            cover = int(float(match[1]) * 100)
            uncover = 100 - cover
            msg = f"['Cover {cover}%', 'Uncover {uncover}%']"
            return border_msg(msg)


def run_unit_test(arguments, build_path):
    repeat = 1 if not arguments["-r"] else int(arguments["-r"])
    tags = arguments["-t"] if arguments["-t"] else ""
    command = "{}/bin/CodeForHHTechShareTest --abort {}".format(build_path, tags)
    outdir = "Coverage"
    outfile = "Coverage.xml"

    if arguments["--coverage"]:
        source = "--source {}*".format(os.path.join(os.getcwd(), "src"))

        if arguments["--coverage_ignore"]:
            excluded = "--excluded_sources {}".format(arguments["--coverage_ignore"])
        else:
            excluded = ""

        export_type = "--export_type html:{}".format(outdir)
        if arguments["--coverage_cobertura"]:
            export_type = "--export_type cobertura:{}".format(outfile)

        command = "OpenCppCoverage.exe {} {} {} -- {}".format(
            source, excluded, export_type, command
        )

    for num in range(repeat):
        print("test repeat: ", num)
        run_and_echo(command)

    if arguments["--coverage"]:
        if arguments["--coverage_cobertura"]:
            print_xml_coverage(os.path.join(os.getcwd(), outfile))
        else:
            print_html_coverage(os.path.join(os.getcwd(), outdir, "index.html"))


def run_gui(arguments, build_path):
    tags = arguments["-t"] if arguments["-t"] else ""

    command = "{}/bin/UdiUi.exe {}".format(build_path, tags)
    run_and_echo(command)


def main():
    init_environ()

    arguments = docopt(__doc__, version="1.0")

    build_path = create_build_path(arguments)

    run_build = True if not arguments["test"] else False
    run_test = True if not arguments["build"] else False

    if run_build:
        build_application(arguments, build_path)

    if run_test:
        run_unit_test(arguments, build_path)


if __name__ == "__main__":
    main()
    sys.exit(0)
