import unittest
from unittest.mock import patch

import eiti_info


class TestMain(unittest.TestCase):

    def test_check_anns(self):
        # Check wheter function raises TypeError on 
        # inappropriate argument type.
        with self.assertRaises(TypeError):
            eiti_info.check_anns('test', 'test')

    @patch('eiti_info.requests.get')
    def test_download_anns(self, r_mock):
        # Check wheter function returns "Bad response"
        # on not ok response.
        r_mock.return_value.ok = False

        act_call = eiti_info.download_anns('mock')
        self.assertEqual(act_call, "Bad response")

        # Check wheter function returns ResultSet
        # on ok response.
        r_mock.return_value.ok = True
        r_mock.return_value.text = 'mock'

        act_call = eiti_info.download_anns('')
        self.assertIsInstance(act_call, eiti_info.ResultSet)


if __name__ == '__main__':
    unittest.main()
