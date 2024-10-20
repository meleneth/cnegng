import pytest

from cnegng.generations.two.log_widget import LogWidget


def test_log_widget_logs_messages():
    log_widget = LogWidget(x=0, y=0, width=400, height=200)
    log_widget("some", "log", "message")
    assert log_widget.messages[0] == "somelogmessage"
