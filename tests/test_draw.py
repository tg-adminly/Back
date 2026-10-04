from tgagent.agents.giveaway import draw


def test_commit_matches_seed():
    seed = draw.new_seed()
    assert len(seed) == 64
    assert draw.commit_of(seed) == draw.commit_of(seed)
    assert draw.commit_of(seed) != draw.commit_of(draw.new_seed())


def test_list_hash_ignores_input_order():
    a = [(1, 111), (2, 222), (3, 333)]
    assert draw.participants_hash(a) == draw.participants_hash(list(reversed(a)))
    assert draw.participants_file(a) == b"1:111\n2:222\n3:333\n"


def test_rank_is_deterministic_permutation():
    seed, lh = "s" * 64, "h" * 64
    numbers = list(range(1, 101))
    order = draw.rank(seed, lh, numbers)
    assert sorted(order) == numbers
    assert order == draw.rank(seed, lh, reversed(numbers))
    assert order != draw.rank("x" * 64, lh, numbers)


def test_rank_can_be_reproduced_by_hand():
    import hashlib

    seed, lh = "abc", "def"
    expected = min([1, 2, 3], key=lambda n: hashlib.sha256(f"abc:def:{n}".encode()).hexdigest())
    assert draw.rank(seed, lh, [1, 2, 3])[0] == expected
