from unittest import mock
from cli.timer import Timer


@mock.patch("cli.timer.time.perf_counter")
def test_elapsed_time(mock_perf_counter):
    mock_perf_counter.side_effect = [0, 1]
    t = Timer(clock=mock_perf_counter)
    assert abs(t.elapsed_time - 1) < 0.1


@mock.patch("cli.timer.time.perf_counter")
def test_has_elapsed_true(mock_perf_counter):
    mock_perf_counter.side_effect = [0, 1]
    t = Timer(clock=mock_perf_counter)
    assert t.has_elapsed(0.5) is True


@mock.patch("cli.timer.time.perf_counter")
def test_has_elapsed_false(mock_perf_counter):
    mock_perf_counter.side_effect = [0, 0.5]
    t = Timer(clock=mock_perf_counter)
    assert t.has_elapsed(1) is False


@mock.patch("cli.timer.time.perf_counter")
def test_reset(mock_perf_counter):
    mock_perf_counter.side_effect = [0, 1, 2, 3]
    t = Timer(clock=mock_perf_counter)
    t.reset()
    assert t.start_time == 1
    t.reset()
    assert t.start_time == 2
    t.reset()
    assert t.start_time == 3

