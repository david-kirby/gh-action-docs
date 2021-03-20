import logging
import unittest
from src.gh_action_docs import app

logging.disable(logging.CRITICAL)


class TestActionFileCheck(unittest.TestCase):
    def test_no_files_found(self):
        results = app.check_for_file("not-existent-file")
        self.assertFalse(results)


if __name__ == "__main__":
    unittest.main()
