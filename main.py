import os
import re
from github import Github
from markdown_table_generator import (
    generate_markdown,
    table_from_string_list,
    Alignment,
)

from utils import *

os.system("ls -Rla /")

USERNAME = os.environ["INPUT_USERNAME"]
TOKEN = os.environ["INPUT_TOKEN"]

REPO = os.environ["INPUT_REPO"]
BRANCH = os.environ["INPUT_BRANCH"]

GITHUB_ACCESS = Github(USERNAME, TOKEN)


class table_data:
    def __init__(self):
        f = open("test_result.txt", "r")
        (
            self.__general_nbr_of_tests,
            self.__general_nbr_of_success,
            self.__general_nbr_of_fails,
            self.__general_coverage,
            self.__general_duration,
            self.__tests_table,
        ) = pytest_report_parser(f.read())

    def get_markdown_data(self):
        general_table = [
            ["Tests", "Success", "Failed", "Time"],
            [
                self.__general_nbr_of_tests,
                self.__general_nbr_of_success,
                self.__general_nbr_of_fails,
                self.__general_duration,
            ],
        ]
        table = table_from_string_list(general_table, Alignment.CENTER)
        self.__general_table_markdown = generate_markdown(table)

        details_table = [["Tests", "Coverage", "Total", "Success", "Fail"]]
        for test in self.__tests_table:
            details_table.append(test)
        table = table_from_string_list(details_table, Alignment.CENTER)
        self.__details_table_markdown = generate_markdown(table)

    def create_report_table(self):
        return create_readme_replacement(
            self.__general_coverage,
            self.__details_table_markdown,
            self.__general_table_markdown,
        )


def execute_pytest():
    os.system("pytest /app/tests/* > test_result.txt")


def get_current_github_readme():
    repo = GITHUB_ACCESS.get_user().get_repo(REPO)
    file = repo.get_contents("README.md", ref=BRANCH)
    return file.decoded_content.decode("utf-8")


def push_new_github_readme(new_github_readme):
    repo = GITHUB_ACCESS.get_user().get_repo(REPO)
    file = repo.get_contents("README.md", ref=BRANCH)
    repo.update_file(
        "README.md", "commit message", new_github_readme, file.sha, branch=BRANCH
    )


def edit_readme(current_readme, new_content):
    return re.sub(
        R_README_POSITION_TARGET,
        new_content,
        current_readme,
        flags=re.DOTALL,
    )


execute_pytest()

table = table_data()
table.get_markdown_data()
table_report = table.create_report_table()

current_readme = get_current_github_readme()
new_readme = edit_readme(current_readme, table_report)

# print(new_readme)
push_new_github_readme(new_readme)
