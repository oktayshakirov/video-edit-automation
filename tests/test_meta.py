

def test_notice_kicker_puts_a_routing_line_on_the_notice_card():
    """A disclaimer is detected from its words; a routing line asks by kicker."""
    from video_automation.longform.meta import is_notice
    assert is_notice(("", "This is not financial advice."))
    assert is_notice(("NOTICE", "New ringing? Get it checked."))
    assert not is_notice(("", "New ringing? Get it checked."))
    assert not is_notice(("", "tinnire: to ring"))
