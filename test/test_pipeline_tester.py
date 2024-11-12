from src.pipeline_tester import sample_func


def test_returns_6():
    output = sample_func(2, 3)
    assert output == 6
