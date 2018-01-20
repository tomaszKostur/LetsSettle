from pprint import pprint
from main import Calculator
import pytest



class TestCalculator:

    @pytest.fixture(scope='class')
    def calc(self):
        return Calculator()

    def test_calculator(self, calc):
        calc.add_product('mlekoihuj')
        calc.add_person('mlekoihuj', 'Tomek', 20)
        calc.add_person('mlekoihuj', 'Jacek', 10)
        calc.add_person('mlekoihuj', 'Ola', 0)

        calc.calculate_single_product('mlekoihuj')
        print("\nResults:")
        pprint(calc.great_debit_dict['mlekoihuj'])

    def test_great_debit_dict(self, calc):
        calc.add_product('ciasteczka')
        calc.add_person('ciasteczka', 'Tomek', 0)
        calc.add_person('ciasteczka', 'Jacek', 10)
        calc.add_person('ciasteczka', 'Ola', 30)

        result = calc.calculate_single_product('ciasteczka')
        print("\nResults:")
        pprint(calc.great_debit_dict)

    def test_summary(self, calc):
        results = calc.summary()
        print("\nResults:")
        pprint(calc.total_debit_dict)

    def test_calculate_all(self, calc):

        calc.add_product('ciasteczka')
        calc.add_person('ciasteczka', 'Tomek', 30)
        calc.add_person('ciasteczka', 'Jacek', 10)
        calc.add_person('ciasteczka', 'Ola', 30)

        result = calc.calculate_all()
        print("\nResults:")
        pprint(result)
