from cnegng.ACME import BasicStats


def test_basic_stats():
    stats = BasicStats(maximum_life=100)
    assert stats.maximum_life == 100


def test_basic_stats_dir_is_attributes_based():
    stats = BasicStats(maximum_life=100)
    assert dir(stats) == ["maximum_life"]
