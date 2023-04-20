from cli import helper
import pytest

def test_helper_get_top_prefixes():
    topic_names = [
        "domainOne.example.v1",
        "_domainOne.example.v1",
        "domainTwo-example.v1",
        "domainTwo-example.v2",
        "domainThree_example.v1",
        "domainThree_test.v1",
        "domainThree.example.v2",
        "domainFour_example.v1.example",
        "domainFour.example.v2",
        "domainFour-example.v3",
        ".domainFour-example.v3",
        "_domainFour-example.v3",
        "-domainFour-example.v3",
        "domainFour.example.v4",
        "domainFour.example.v4",
    ]
    expected_result = {
        "domainFour": 8,
        "domainThree": 3,
        "domainOne": 2
    }
    result = helper.get_top_prefixes(topic_names, max_keys=3)
    assert result == expected_result

def test_helper_get_top_prefixes_with_empty_input():
    topic_names = []
    expected_result = {}
    result = helper.get_top_prefixes(topic_names)
    assert result == expected_result