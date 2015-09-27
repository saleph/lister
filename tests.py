from django.test import TestCase
from .models import Reader


class ReaderMethodTests(TestCase):
    """
    Tests of:
    1. reset_speech_number()
    2. at_least_one_wants_is_true()
    """
    def test_reset_speech_number_with_zero_value(self):
        """
        reset_speech_number() should return 0 for readers whose
        speech_number equals 0.
        """
        reader = Reader(speech_number=0)
        reader.reset_speech_number()
        self.assertEqual(reader.speech_number, 0)

    def test_reset_speech_number_with_one_value(self):
        """
        reset_speech_number() should return 1 for readers whose
        speech_number equals 1.
        """
        reader = Reader(speech_number=1)
        reader.reset_speech_number()
        self.assertEqual(reader.speech_number, 1)

    def test_reset_speech_number_with_greater_than_one_value(self):
        """
        reset_speech_number() should return 1 for readers whose
        speech_number is greater than 1.
        """
        reader = Reader(speech_number=5)
        reader.reset_speech_number()
        self.assertEqual(reader.speech_number, 1)

    def test_at_least_one_wants_is_true_with_three_false(self):
        """
        at_least_one_wants_is_true() should return False
        if all the wants are False.
        """
        reader = Reader()
        self.assertEqual(reader.at_least_one_wants_is_true(), False)

    def test_at_least_one_wants_is_true_with_two_false_one_true(self):
        """
        at_least_one_wants_is_true() should return True
        if one wants are True.
        """
        reader = Reader(wants_lection=True)
        self.assertEqual(reader.at_least_one_wants_is_true(), True)

    def test_at_least_one_wants_is_true_with_one_false_two_true(self):
        """
        at_least_one_wants_is_true() should return True
        if two wants are True.
        """
        reader = Reader(wants_lection=True, wants_psalm=True)
        self.assertEqual(reader.at_least_one_wants_is_true(), True)

    def test_at_least_one_wants_is_true_with_three_true(self):
        """
        at_least_one_wants_is_true() should return True
        if all the wants are True.
        """
        reader = Reader(wants_lection=True, wants_psalm=True,
                        wants_believers_pray=True)
        self.assertEqual(reader.at_least_one_wants_is_true(), True)
