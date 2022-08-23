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
    general_duration = general_infos.split(" ")[-1]
    general_nbr_of_tests = 0
    general_nbr_of_success = 0
    general_nbr_of_fails = 0

    for test in re.findall(R_TEST, report_content):
        test_title = re.search(R_TEST_TITLE, test).group()
        test_nbr_total = len(test.split(" ")[1])
        general_nbr_of_tests += len(test.split(" ")[1])
        test_nbr_success = test.split(" ")[1].count(".")
        general_nbr_of_success += test.split(" ")[1].count(".")
        test_nbr_fail = test_nbr_total - test_nbr_success
        general_nbr_of_fails += test_nbr_total - test_nbr_success
        test_coverage_percent = test_nbr_success / test_nbr_total * 100

        tests_table.append(
            str(r) for r in [
                test_title,
                coverage_badge_editor(test_coverage_percent),
                test_nbr_total,
                test_nbr_success,
                test_nbr_fail,
            ]
        )

    general_coverage = general_nbr_of_success / general_nbr_of_tests * 100
    return (
        str(general_nbr_of_tests),
        str(general_nbr_of_success),
        str(general_nbr_of_fails),
        str(general_coverage),
        str(general_duration),
        tests_table,
    )


def create_readme_replacement(coverage, detailed_table, general_table):
    return (
        """
[Pytest Table]: <>

"""
        + coverage_badge_editor(float(coverage))
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
