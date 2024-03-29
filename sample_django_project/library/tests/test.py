from datetime import datetime

from django.test import TestCase

from ..utils import yesterday, timezone
from unittest.mock import patch, MagicMock, Mock



class SampleTest(TestCase):
    """Test to be deleted simply to test pre-commit"""

    def test_pre_commit(self):
        # test flake8 and black allow more than 88 chars less than 120
        a = "I am a very very lsdknf lkjasd nlkajsdbflk sdjbfklajsdbfkjdbfkljsdabf lkdbflkasjdbfakjsdbflahsbdfbhvsdfhba"
        print(a)


class YesterdayTest(TestCase):
    @patch("library.utils.timezone.now")
    def test_success(self, mock):
        mock.return_value = datetime(1945, 2, 12, 0, 0, 0)

        expected = datetime(1945, 2, 11).date()

        self.assertEqual(yesterday(), expected)

class YesterdayTestMagicMock(TestCase):
    def test_success(self):
        tz = timezone
        tz.now = MagicMock(return_value=datetime(1945, 2, 12, 0, 0, 0))

        expected = datetime(1945, 2, 11).date()

        self.assertEqual(yesterday(), expected)

class YesterdayTestMock(TestCase):
    def test_success(self):
        tz = timezone
        tz.now = Mock(return_value=datetime(1945, 2, 12, 0, 0, 0))

        expected = datetime(1945, 2, 11).date()

        self.assertEqual(yesterday(), expected)
