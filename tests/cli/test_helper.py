from cli import helper
import pytest

def test_helper_get_top_prefixes():
    topic_names = [
        "DOMAINONE.example.v1",
        "_domainOne.example.v1",
        "domainTwo-example.v1",
        "DomainTwo-example.v2",
        "domainThree_example.v1",
        "domainThree_test.v1",
        "domainThree.example.v2",
        "domainfour_example.v1.example",
        "domainfour.example.v2",
        "domainfour-example.v3",
        ".domainFour-example.v3",
        "_domainFour-example.v3",
        "-domainFour-example.v3",
        "domainFour.example.v4",
        "domainFour.example.v4",
    ]
    expected_result = {
        "domainfour": 8,
        "domainthree": 3,
        "domainone": 2
    }
    result = helper.get_top_prefixes(topic_names, max_keys=3)
    assert result == expected_result

def test_helper_get_top_prefixes_with_empty_input():
    topic_names = []
    expected_result = {}
    result = helper.get_top_prefixes(topic_names)
    assert result == expected_result

def test_shorten():
    # Test case 1: text is shorter than width
    text = 'short'
    width = 10
    assert helper.shorten(text, width) == text
    
    # Test case 2: text is longer than width and placeholder is shorter
    text = 'this is a long text'
    width = 10
    assert helper.shorten(text, width) == 'this is...'
    
    # Test case 3: text is longer than width and placeholder is longer
    text = 'this is a long text'
    width = 10
    placeholder = '…'
    assert helper.shorten(text, width, placeholder) == 'this is a…'
