import re

# Regex Schemas
R_GENERAL_INFO = r"([0-9]* passed in [0-9.]*s)"
R_TEST = r"(tests\/.+\[[0-9 ]*%\])"
R_TEST_TITLE = r"(([^\/]*)_([^\.])*)"
R_README_POSITION_TARGET = r"(\[Pytest Table\]: \<\>(?:.|\n)*\[Pytest Table\]: \<\>)"


def coverage_badge_editor(percent):
    color = ""
    if percent < 40:
        color = "red"
    elif percent >= 40 and percent < 60:
        color = "orange"
    elif percent >= 60 and percent < 80:
        color = "yellow"
    elif percent >= 80 and percent < 90:
        color = "green"
    else:
        color = "success"

    badge = (
        "![coverage](https://img.shields.io/badge/coverage-"
        + str(percent)
        + "%25-"
        + color
        + ")"
    )
    return badge


def pytest_report_parser(report_content):
    tests_table = []
    general_infos = re.search(R_GENERAL_INFO, report_content).group()
    general_nbr_of_tests = general_infos.split(" ")[0]
    general_duration = general_infos.split(" ")[-1]
    general_nbr_of_success = 0
    general_nbr_of_fails = 0

    for test in re.findall(R_TEST, report_content):
        test_title = re.search(R_TEST_TITLE, test).group()
        test_nbr_total = str(len(test.split(" ")[1]))
        test_nbr_success = str(test.split(" ")[1].count("."))
        general_nbr_of_success = str(
            int(general_nbr_of_success) + int(test_nbr_success)
        )
        test_nbr_fail = str(int(test_nbr_total) - int(test_nbr_success))
        general_nbr_of_fails = str(int(general_nbr_of_fails) + int(test_nbr_fail))
        test_coverage_percent = int(test_nbr_success) // int(test_nbr_total) * 100

        tests_table.append(
            [
                test_title,
                coverage_badge_editor(test_coverage_percent),
                test_nbr_total,
                test_nbr_success,
                test_nbr_fail,
            ]
        )

    general_coverage = str(
        int(int(general_nbr_of_success) / int(general_nbr_of_tests) * 100)
    )
    return (
        general_nbr_of_tests,
        general_nbr_of_success,
        general_nbr_of_fails,
        general_coverage,
        general_duration,
        tests_table,
    )


def create_readme_replacement(coverage, detailed_table, general_table):
    return (
        """
[Pytest Table]: <>

"""
        + coverage_badge_editor(int(coverage))
        + """

<details>
<summary>Coverage Report</summary>

"""
        + detailed_table
        + """

</details>

"""
        + general_table
        + """

[Pytest Table]: <>
        """
    )
