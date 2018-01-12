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
    def __init__(self):
        self.data_dict = {}
        self.debtor_dict = {}

    def add_product(self, product_name):
        self.data_dict[product_name] = {}

    def add_person(self, product_name, name, cost):
        self.data_dict[product_name][name] = cost

    def calculate_single_product(self, product_name):
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
        for person in debit_dict:
            for mate in debit_dict[person]:
                if person is mate: continue
                elif debit_dict[person][mate] > debit_dict[mate][person]:
                    debit_dict[person][mate] -= debit_dict[mate][person]
                    debit_dict[mate][person] = 0

        return debit_dict



if __name__ == '__main__':
    LetsSettleApp().run()
