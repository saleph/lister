from django.test import TestCase
from .models import Reader


class ReaderMethodTests(TestCase):
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
