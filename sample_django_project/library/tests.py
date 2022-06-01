from django.test import TestCase


class SampleTest(TestCase):
    """Test to be deleted simply to test pre-commit"""

    def test_pre_commit(self):
        # test flake8 and black allow more than 88 chars less than 120
        a = "I am a very very lsdknf lkjasd nlkajsdbflk sdjbfklajsdbfkjdbfkljsdabf lkdbflkasjdbfakjsdbflahsbdfbhvsdfhba"
        print(a)
