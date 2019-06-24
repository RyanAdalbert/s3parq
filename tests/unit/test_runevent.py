import pytest
import mock
from unittest.mock import MagicMock, patch
from core.airflow.plugins.runevent_operator import RunEvent_task as ret
from core.helpers.session_helper import SessionHelper
import core.models.configuration as config

class MockSession:

    def add(self, run_event_obj):
        run_event_obj.id = 42

    def commit(self):
        return True

    def close(self):
        return True


class MockTaskInstance:

    def xcom_push(self, **kwargs):
        return True


def test_xcomm_push_called_with_42(monkeypatch):
    session_mock = MockSession()
    ti_mock = MockTaskInstance()
    ti_mock.xcom_push = MagicMock()
    monkeypatch.setattr(SessionHelper, "session", session_mock)
    ret(1, ti=ti_mock)
    ti_mock.xcom_push.assert_called_with(key="run_id", value=42)
