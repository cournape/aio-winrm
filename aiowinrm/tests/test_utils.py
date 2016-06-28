import unittest

from aiowinrm.constants import TranportKind
from aiowinrm.utils import parse_host


class TestParseHost(unittest.TestCase):
    def test_simple(self):
        # Given
        r_complete_host = "http://192.168.1.1:5985/wsman"
        host = "192.168.1.1"

        # When
        complete_host = parse_host(host, TranportKind.http)

        # Then
        self.assertEqual(complete_host, r_complete_host)

        # Given
        r_complete_host = "https://192.168.1.1:5986/wsman"
        host = "192.168.1.1"

        # When
        complete_host = parse_host(host)

        # Then
        self.assertEqual(complete_host, r_complete_host)
