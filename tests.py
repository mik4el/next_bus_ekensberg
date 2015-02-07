import unittest
from next_bus import minutes_to_next_bus


class TestMinutesToNextBus(unittest.TestCase):
    def setUp(self):
        pass

    def test_minutes_to_next_bus(self):
        result = minutes_to_next_bus()
        self.assertNotEqual(result, 0)