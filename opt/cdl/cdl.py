#!/bin/env python
import os
import argparse
from pathlib import Path
from typing import Union, Optional

PathType = Union[os.PathLike, str]


class Config:
    # The path to the dir where the course files are stored
    MAGSHIMIM_DIR_PATH = Path.home() / "Magshimim"

    # The existing courses. key: alias, value: dirname in MAGSHIMIM_DIR_PATH
    COURSES = {"p": "programming_cpp", "a": "assembly"}

    # @brief Given a string, is it a week directory?
    # @warn If you set it to always return True, it's your responsibility
    #           to make sure only valid files are located under MAGSHIMIM_DIR_PATH
    IS_WEEK_DIR = lambda s: s.startswith("week")

    # @brief Given a string, is it a course directory?
    # @warn If you set it to always return True, it's your responsibility
    #           to make sure only valid files are located under MAGSHIMIM_DIR_PATH
    IS_COURSE_DIR = lambda s: s.startswith("course")

    # @brief The function used to get the latest week dir.
    # @param weeks the name of the weeks in a directory
    # @type weeks List[str]
    # @return the name of the latest week directory
    # @rtype str
    GET_LATEST_WEEK = lambda weeks: (
        max(weeks, key=lambda w: int(w.lstrip("week")))
    )

    # @brief The function used to get the latest course dir.
    # @param courses the name of the courses in a directory
    # @type courses List[str]
    # @return the name of the latest course directory
    # @rtype str
    GET_LATEST_COURSE = lambda courses: (
        max(courses, key=lambda c: int(c.lstrip("course")))
    )

    # @brief Given a course identification, return the directory name of that course.
    # @param course_id the course identification provided by the user
    # @type course_id str
    # @return the name of the course directory
    # @rtype str
    COURSE_IDENTIFICATION_TO_DIR = lambda course_id: f"course{course_id}"

    # @brief Given a week identification, return the directory name of that week.
    # @param week_id the week identification provided by the user
    # @type week_id str
    # @return the name of the week directory
    # @rtype str
    WEEK_IDENTIFICATION_TO_DIR = lambda week_id: f"week{week_id}"

    @staticmethod
    def create_week_dir(week_path: PathType) -> None:
        """Creates a week directory at the given path. Note: The directory
            might already exist with all the necessary files. You should not
            overwrite existing files.

        :param week_path: The path to the week directory.
        """
        path = Path() / week_path
        mkdir_gracefully(path / "classwork")
        mkdir_gracefully(path / "homework" / "src")
        mkdir_gracefully(path / "homework" / "answ")


def mkdir_gracefully(path: PathType) -> None:
    Path(path).mkdir(parents=True, exist_ok=True)


def get_latest_course(dir: PathType) -> Optional[str]:
    courses = [c for c in os.listdir(dir) if Config.IS_COURSE_DIR(c)]
    return Config.GET_LATEST_COURSE(courses) if courses else None


def get_latest_week(dir: PathType) -> Optional[str]:
    weeks = [w for w in os.listdir(dir) if Config.IS_WEEK_DIR(w)]
    return Config.GET_LATEST_WEEK(weeks) if weeks else None


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Open Magshimim lesson")
    parser.add_argument(
        "directory",
        choices=list(Config.COURSES.keys()),
        help="the directory to navigate to ({})".format(
            ", ".join(
                f"{alias}={dirname}"
                for alias, dirname in Config.COURSES.items()
            )
        ),
    )
    parser.add_argument(
        "hw",
        nargs="?",
        choices=["c", "h"],
        default="h",
        help="the classwork (c) or homework (h) directory to navigate to",
    )
    parser.add_argument(
        "-c", type=str, help="the course identification to navigate to"
    )
    parser.add_argument(
        "-w", type=str, help="the week identification to navigate to"
    )

    return parser


def get_course(path: PathType, args: argparse.Namespace) -> Optional[PathType]:
    """Get the path to the course directory in the given path with the given
    arguments.
    """
    if args.c is None:
        return get_latest_course(path)

    course = Config.COURSE_IDENTIFICATION_TO_DIR(args.c)
    mkdir_gracefully(Path() / path / course)
    return course


def get_week(
    course_path: PathType, args: argparse.Namespace
) -> Optional[PathType]:
    """Get the path to the week directory in the given path with the given
    arguments.
    """
    if args.w is None:
        return get_latest_week(course_path)

    week = Config.WEEK_IDENTIFICATION_TO_DIR(args.w)
    Config.create_week_dir(Path() / course_path / week)
    return week


def main() -> None:
    parser = create_parser()
    args = parser.parse_args()

    selected_dirname = Config.COURSES[args.directory]

    base_path = Path() / Config.MAGSHIMIM_DIR_PATH / selected_dirname
    mkdir_gracefully(base_path)

    course = get_course(base_path, args)
    if course is None:
        parser.error("no course dir to use. Please specify with -c flag")
    course_path = base_path / course

    week = get_week(course_path, args)
    if week is None:
        parser.error("no week dir to use. Please specify with -w flag")
    week_path = course_path / week

    if args.hw == "c":
        print(week_path / "classwork")
    elif args.hw == "h":
        print(week_path / "homework" / "answ")
    else:
        print(week_path)


if __name__ == "__main__":
    main()

