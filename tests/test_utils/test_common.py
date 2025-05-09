import os
from unittest import mock
from app.utils import common

def test_setup_logging_all_paths():
    with mock.patch("logging.config.fileConfig") as mocked_config:
        with mock.patch("os.path.dirname", return_value="/fake/dir"):
            with mock.patch("os.path.normpath") as mocked_normpath:
                # Simulate a normalized path
                mocked_normpath.return_value = "/fake/dir/logging.conf"
                
                common.setup_logging()

                # Ensure path construction happened
                mocked_normpath.assert_called_once()
                mocked_config.assert_called_once_with("/fake/dir/logging.conf", disable_existing_loggers=False)
