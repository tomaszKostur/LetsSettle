from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.checkbox import CheckBox
from kivy.uix.textinput import TextInput
from copy import deepcopy

class Scroller(BoxLayout):

    def add_member(self):
        self.ids.products.add_widget(Button(size_hint=(1, None), height=100))


class PersonView(BoxLayout):
    pass


class PersonTitleBar(BoxLayout):
    pass


class ProductView(BoxLayout):

    def add_person(self):
        self.ids.people.add_widget(PersonView())


class MainView(BoxLayout):
    pass


class LetsSettleApp(App):
    def build(self):
        self.main_view = MainView()
        return self.main_view


class Calculator():
    """
    Calculator that makes calculation of who ows who money.
    Structures conventions:
        data_dict = {<str:product_name>: {<str:person>: <int:paid>,
                                          ...}
                     ...}

        debit_dict = {<str:person>: {<str:mate_that_person_ows>: <int:ammount>,
                                     ...}
                      ...}

        great_debit_dict = {<str:product>: debit_dict, ...}
    """
    def __init__(self):
        """
        Declares class variables.
        Dict's structure descriptions are in class docstring.
        """
        self.data_dict = {}  # structure of data_dict.
        self.great_debit_dict = {}  # structure of great_debit_dict.
        self.total_debit_dict = {}  # structure of debit_dict.

    def add_product(self, product_name):
        """
        Add product to self.data_dict.

        product_name: string
        """
        self.data_dict[product_name] = {}

    def add_person(self, product_name, name, paid):
        """
        Adds person to self.product_name[name]: paid.
        product_name: string, name of existing products
        name: string, person name
        paid: int, person cost
        """
        self.data_dict[product_name][name] = paid

    def calculate_single_product(self, product_name):
        """
        Calculates debits to each other for product.
        Requires self.data_dict[product_name] filled with data.
            The data is dictionary with people and ammount of theirs individual
            costs.
        product_name: string, name of the product.
        """
        product_dict = self.data_dict[product_name]
        product_cost = sum([cost for cost in product_dict.values()])
        people_num = len(product_dict)
        person_cost = float(product_cost)/float(people_num)

        # calculate fraction of total cost for every person_cost
        cost_frac = {}
        for person in product_dict:
            cost_frac[person] = product_dict[person]/product_cost

        # calculate debit all to all
        debit_dict = {}
        for person in product_dict:
            debit_dict[person] = {}
            for mate in product_dict:
                if mate is person: continue
                debit_dict[person][mate] = cost_frac[mate] * person_cost

        # simplify debit_dict
        self._simplify_debit_dict(debit_dict)

        # save result in class variable
        self.great_debit_dict[product_name] = debit_dict

    @staticmethod
    def _simplify_debit_dict(debit_dict):
        """
        Simplify debit_dict structure.
            For example: if 'A' ows 'B' 5 and 'B' ows 'A' 4,
                then 'A' ows 'B' 1
        debit_dict: dict, see structure in class docstring.
        returns: None, debit_dict values are changed.
        """
        for person in debit_dict:
            for mate in debit_dict[person]:
                if debit_dict[person][mate] >= debit_dict[mate][person]:
                    debit_dict[person][mate] -= debit_dict[mate][person]
                    debit_dict[mate][person] = 0
        return debit_dict

    def summary(self):
        """
        Get all debit_dict's from self.great_debit_dict's products.
        Merge them into one debit_dict structure.
        Save into self.total_debit_dict
        """
        summary_debit_dict = {}
        for product in self.great_debit_dict:
            for person in self.great_debit_dict[product]:
                if person not in summary_debit_dict:
                    summary_debit_dict[person] = \
                        deepcopy(self.great_debit_dict[product][person])
                else:
                    for mate in self.great_debit_dict[product][person]:
                        if mate not in summary_debit_dict[person]:
                            summary_debit_dict[person][mate] = \
                                deepcopy(self.great_debit_dict
                                         [product][person][mate])
                        else:
                            summary_debit_dict[person][mate] += \
                                self.great_debit_dict[product][person][mate]

        self._simplify_debit_dict(summary_debit_dict)
        self.total_debit_dict = summary_debit_dict

    def calculate_all(self):
        """
        Calculates debits for all people and all producs.
        returns: debit_dict, dict for summary of all debits.
        """
        for product in self.great_debit_dict:
            self.calculate_single_product(product)
        self.summary()
        return self.total_debit_dict


if __name__ == '__main__':
    LetsSettleApp().run()
