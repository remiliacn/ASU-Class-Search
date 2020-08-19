import unittest

from src.rmp_class import RateMyProfAPI

class MyTestCase(unittest.TestCase):
    def test_issue_1(self):
        # This test is for issue 1
        api = RateMyProfAPI(111, 'Ken Rohly')
        api.retrieve_rmp_info()
        self.assertTrue(api.get_first_tag())
        self.assertTrue(api.get_rmp_info())
        self.assertTrue(api.get_would_take_again())
        self.assertTrue(api.get_tags())

    def test_invalid_school_code(self):
        try:
            RateMyProfAPI(-1, 'Ken Rohly')
            self.fail('ValueError Exception should be thrown.')
        except ValueError:
            self.assertTrue(True)
        except Exception as err:
            self.fail(f'Wrong exception is thrown: {err}\n'
                      'Should be ValueError')



if __name__ == '__main__':
    unittest.main()
