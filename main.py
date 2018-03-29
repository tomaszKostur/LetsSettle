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
from kivy.properties import DictProperty, StringProperty, ListProperty,\
                            NumericProperty, BooleanProperty
from copy import deepcopy
from pprint import pprint
from inspect import getmembers
from kivy.clock import Clock
import kivy.metrics


class ProductList(BoxLayout):
    """
    Well, the most important idea is, the only interface of the widget are it's
    two properties: 'prod_list, and 'last_selected'.
    'prod_list' is designed to be input of the widget. Adding/edit elements to
        'prod_list' causes adding/edit buttons to the widget.
    'last_selected' is designed to be output of the widegt. It's value is
        allways name of last touched button on products (see id :products)
    """
    prod_list = ListProperty([])
    last_selected = StringProperty("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.widget_list = []
        self.minimum_height = 20

        # TODO It looks like there are no ids yet. First widgets cannot be added via:
        # self.ids.products.add_widget(prod_btn)
#        self._draw_prodlist()

    def _draw_prodlist(self):
        print('PL::pl: {}'.format(self.prod_list))
        self.ids.products.clear_widgets()
        for name in self.prod_list:
            prod_btn = Button(text=name, size_hint=(1, None), height=100)
            self.widget_list.append(prod_btn)
            prod_btn.bind(on_press=self._last_selected)
            print("DEBUG::{}".format(self.ids))
            self.ids.products.add_widget(prod_btn)

    def _last_selected(self, instance):
        self.last_selected = instance.text
        print("Prodlist::last_selected: {}".format(self.last_selected))

    def on_prod_list(self, instance, value):
        self._draw_prodlist()


class MateWidget(BoxLayout):
    """
    The widegt represents bar of name and costs of one person.
    It should be used only as widgets added to ProductView.
    """
    q_num = NumericProperty(0)
    mate_name = StringProperty("Tomek")
    mate_cost = NumericProperty("77")
    is_used = BooleanProperty(True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def update_cost_p(self):
        self.mate_cost = self.ids.cost_w.text
        print("MateWidget::mate_cost: {}".format(self.mate_cost))

    def update_name_p(self):
        self.mate_name = self.ids.name_w.text
        print("MateWidget::mante_name: {}".format(self.mate_name))


class PersonTitleBar(BoxLayout):
    pass


class ProductView(BoxLayout):
    prod_name = StringProperty("Product name")
    people = ListProperty([["aaa", 123], ["bbb", 222]])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.mate_widgets = []
        self.total_cost = '999'

        # TODO same as in ProductList
#        self.redraw_mates()

    def redraw_mates(self):
        self.ids.mates_list.clear_widgets(self.mate_widgets)
        for q_num, mate_obj in enumerate(self.people):
            mate = MateWidget(mate_name=mate_obj[0],
                              mate_cost=mate_obj[1],
                              q_num=q_num,
                              size_hint=(1, None),
                              height=100)
            mate.bind(mate_name=self.update_people)
            mate.bind(mate_cost=self.update_people)
            self.mate_widgets.append(mate)
            self.ids.mates_list.add_widget(mate)

    def update_people(self, instance, value):
        print("ProdView_v2::update_people, instance:{} value:{}, q_num: {}"
              .format(instance, value, instance.q_num))
        self.people[instance.q_num][0] = instance.mate_name
        self.people[instance.q_num][1] = instance.mate_cost

    def on_people(self, instance, value):
        self.redraw_mates()


class MainView(BoxLayout):
    products = DictProperty({})
    c_uuid = NumericProperty(0)
    test = StringProperty('')


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
