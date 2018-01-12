from pprint import pprint
from main import Calculator
import pytest



class TestCalculator:

#    @pytest.fixture(scope='class')
#    def calc():
#        return Calculator()

    def test_calculator(calc):
        calc = Calculator()
        calc.add_product('mlekoihuj')
        calc.add_person('mlekoihuj', 'Tomek', 20)
        calc.add_person('mlekoihuj', 'Jacek', 10)
        calc.add_person('mlekoihuj', 'Ola', 0)

        result = calc.calculate_single_product('mlekoihuj')
        pprint(result)
