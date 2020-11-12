import unittest

from src.asu_class_search import generate_response, ASUClassFinder

INFO_NOT_AVAILABLE = "Oops, no information document."


class MyTestCase(unittest.TestCase):
    def test_generate_response(self):
        mock_instruction_node = ['Yinong Chen']
        mock_class_number = '76545'
        mock_seats_open = '15'

        resp = generate_response(
            mock_instruction_node,
            mock_class_number,
            mock_seats_open
        )

        self.assertTrue(resp)

    def test_invalid_major(self):
        api = ASUClassFinder('CSEDD', '1232123')
        self.assertEqual(api.get_page_count(), 0)
        self.assertEqual(api.__str__(), INFO_NOT_AVAILABLE)

    def test_valid_major(self):
        api = ASUClassFinder('CSE', '110')
        self.assertGreater(api.get_page_count(), 0)
        self.assertTrue(api.__str__())
        self.assertNotEqual(api.__str__(), INFO_NOT_AVAILABLE)


if __name__ == '__main__':
    unittest.main()
