from tgagent.agents.giveaway.handlers.participant import ReplyThrottle


def test_throttle_limits_repeated_error_replies(monkeypatch):
    now = [1000.0]
    monkeypatch.setattr("time.monotonic", lambda: now[0])
    t = ReplyThrottle()
    assert t.allow(1)
    assert not t.allow(1)  # 19 ta xato xabar o'rniga bitta
    assert t.allow(2)  # boshqa foydalanuvchiga ta'sir qilmaydi
    now[0] += ReplyThrottle.WINDOW
    assert t.allow(1)
    t.reset(1)
    assert t.allow(1)
