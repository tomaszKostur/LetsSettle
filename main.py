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
from kivy.properties import DictProperty, StringProperty, ListProperty, NumericProperty
from copy import deepcopy
from pprint import pprint
from inspect import getmembers
from kivy.clock import Clock
import kivy.metrics


class ProductList(BoxLayout):
    products = {}
    r_uuid = NumericProperty()
    def add_product(self, name, uuid):
        product_button = Button(size_hint=(1, None), height=100,
                                text=name)
        product_button.uuid = uuid
        self.products[uuid] = product_button
        self.ids.products.add_widget(product_button)

        product_button.bind(on_press=self.get_pressed_uuid)

    def get_pressed_uuid(self, instance):
        print('presed uuid: {}'.format(instance.uuid))
        self.r_uuid = instance.uuid

    def remove_product(self, uuid):
        self.ids.products.remove_widget(self.products[uuid])
        self.products.pop(uuid)


class PersonView(BoxLayout):
    name = StringProperty('Tomek')
    cost = NumericProperty(0)


class PersonTitleBar(BoxLayout):
    pass


class ProductView(BoxLayout):

    def add_person(self):
        self.ids.people.add_widget(PersonView())


class MainView(BoxLayout):
    products = DictProperty({})
    c_uuid = NumericProperty(0)
    test = StringProperty('')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.uuid = 0
        self.c_prodname = ''

        # bind add_prod_btn to self.add_product
        add_prod_btn = self.ids.product_list.ids.add_prod_btn
        add_prod_btn.bind(on_press=self.add_product)

        # bind rm_prod_btn to self.remove_product
        rm_prod_btn = self.ids.product_list.ids.rm_prod_btn
        rm_prod_btn.bind(on_press=self.remove_product)

        # update_c_uuid if recent product button was pressed
        self.ids.product_list.bind(r_uuid=self.update_c_uuid)

        # add_person_btn bind
        add_person_btn = self.ids.product_view.ids.add_person_btn
        add_person_btn.bind(on_press=self.add_person)


    def update_c_uuid(self, instance, value):
        self.c_uuid = value
        print('MainView::update_c_uuid: {}'.format(self.c_uuid))
        self._generate_product_view()

    def _generate_product_view(self):
        print("MainView::_generate_product_view")
        self.c_prodname = str(list(self.products[self.c_uuid])[0])
        self.ids.product_view.ids.product_name.text = self.c_prodname
        people_widget = self.ids.product_view.ids.people
        prod_name_input = self.ids.product_view.ids.product_name
        prod_name_input.bind(focus=self.product_name_setter)

        # clear all people from list
        people_widget.clear_widgets()
        c_prod_dict = self.products[self.c_uuid][self.c_prodname]
        for mate in c_prod_dict:
            person_widget = PersonView(name=mate, cost=c_prod_dict[mate])
            person_widget.ids.ammount.bind(text=self.mate_cost_setter(mate))
            person_widget.ids.name.bind(focus=self.mate_name_setter(mate))
            people_widget.add_widget(person_widget)
        print('Test::test: {}'.format(self.test))

    def print_event_attr(self, *args):
        print("EventArgs: {}, focus: {}".format(args, args[0].focus))

    def get_c_totalcost(self):
        c_prod_costs = self.products[self.c_uuid][self.c_prodname]
        c_totalcost = 0
        try:
            for mate_cost in c_prod_costs.values():
                print("mc: {}".format(mate_cost))
                c_totalcost += float(mate_cost)
        except:
            pass
        return str(c_totalcost)

    def mate_cost_setter(self, mate):
        def setter(instance, value):
            self.products[self.c_uuid][self.c_prodname][mate] = value

            # set value to total cost widget
            self.ids.product_view.ids.total_cost.text = self.get_c_totalcost()
        return setter

    def mate_name_setter(self, mate):
        def setter(instance, value):
            if not instance.focus:
                print("on_focus")
                self.products[self.c_uuid][self.c_prodname][instance.text] =\
                    self.products[self.c_uuid][self.c_prodname].pop(mate)
                self._generate_product_view()
        return setter

    def product_name_setter(self, instance, value):
        if not instance.focus:
            c_prodbtn_wdgt = self.ids.product_list.products[self.c_uuid]
            c_prodbtn_wdgt.text = instance.text
            self.products[self.c_uuid][instance.text] =\
                self.products[self.c_uuid].pop(self.c_prodname)

    def _get_uuid(self):
        self.uuid += 1
        return self.uuid

    def add_product(self, instance):
        print('MainView::add_product')
        prod_name = 'product_{}'.format(len(self.products))
        prod_uuid = self._get_uuid()
        self.ids.product_list.add_product(prod_name, prod_uuid)
        self.products[prod_uuid] = {prod_name: {}}
        self.update_c_uuid(None, prod_uuid)

    def remove_product(self, instance):
        try:
            self.ids.product_list.remove_product(self.c_uuid)
            self.products.pop(self.c_uuid)
            self.update_c_uuid(None, max(self.products))
            print('MainView::remove_widget, c_uuid: {}'.format(self.c_uuid))
        except (ValueError, KeyError):
            print("nothing to remove, c_uuid:{}".format(self.c_uuid))
        finally:
            print(self.products)

    def add_person(self, instance):
        print('MainView::add_person')
        try:
            mate_number = len(self.products[self.c_uuid][self.c_prodname])
            dflt_mate = "mate_{}".format(mate_number)

            self.products[self.c_uuid][self.c_prodname][dflt_mate] = 0
            self._generate_product_view()
        except (KeyError):
            print("no product for adding person to")
        finally:
            print(self.products)



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
