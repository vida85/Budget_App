from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.core.text import LabelBase
from kivy.metrics import sp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import (MDListItem,
                             MDListItemHeadlineText,
                             MDListItemSupportingText,
                             MDListItemTertiaryText,
                             MDListItemTrailingCheckbox,
                             MDListItemLeadingIcon, )



class BudgetInterface(MDBoxLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.padding = sp(30)
        self.spacing = sp(10)
    total = 0
    
    def add_item(self, debug=False, i='', d='', a=''):
        if debug:
            
            item = i
            description = d
            amount: str = a
        else:
            item = self.ids.item.text
            description = self.ids.description.text
            amount: str = self.ids.amount.text

        try:
            amount = amount.split(',')
            amount = float(''.join(amount))
        except ValueError:
            print(f"{amount} must be numbers only")
            return
        
        if not item or not description or not amount:
            print("All fields are required")
            return
        else:
            self.ids.item_list.add_widget(MDListItem(
                                    MDListItemHeadlineText(text=item, ),
                                    MDListItemLeadingIcon(icon='cash', ),
                                    MDListItemSupportingText(text=description, ),
                                    MDListItemTertiaryText(text=f"${amount}", ),
                                    MDListItemTrailingCheckbox(icon='checkbox-blank-outline', ),
                                    pos_hint={"center_x": .5, "center_y": .5}, size_hint_x=0.8,),
                                    )
            self.update_total_expenses(amount=amount)
            self.ids.item.text = '0'
            self.ids.description.text = '0'
            self.ids.amount.text = '0'
    
    
    def update_total_expenses(self, amount: float | str):
            try:
                amount = float(amount)
            except ValueError:
                print('Must be numbers only')
                return
            self.total += amount
            self.update_income(value=self.total)
            self.ids.total.text = str(f"Total Expenses: ${round(self.total, 2)}")
    
    
    
    def update_income(self, value: float=0):
        if value:
            try:
                income = float(self.ids.income.text)
            except ValueError:
                income = 0
            result = round(income - value, 2)
        else:
            try:
                result = float(self.ids.income.text)
            except ValueError:
                result = 0
                
        amount = float(self.ids.amount.text)
        self.ids.balance.text = f'Balance: ${result - amount}'


    def add_items_debug(self):
        data = {
                'Location': [
                    'Burger Palace',
                    'Pizza Haven',
                    'Sushi World',
                    'Pasta Paradise',
                    'Taco Town',
                    'Steakhouse Grill',
                    'Vegan Delights',
                    'Coffee Corner'
                ],
                'Description': [
                    'Fast food',
                    'Italian',
                    'Japanese',
                    'Pasta',
                    'Mexican',
                    'Steak',
                    'Vegan',
                    'Cafe'
                ],
                'Amount': [
                    '12.50',
                    '20.00',
                    '35.75',
                    '18.40',
                    '9.99',
                    '45.00',
                    '25.30',
                    '5.50'
                ]
            }
        for i, d, a in zip(data['Location'], data['Description'], data['Amount']):
            self.add_item(debug=True, i=i, d=d, a=a)
    
    

class MainApp(MDApp):
    def build(self):
        self.theme_cls.theme_style_switch_animation = True
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Teal"
        Window.size = [sp(600), sp(1140)]

        LabelBase.register(
            name="corbelb",
            fn_regular="fonts/corbelb.ttf", )

        self.theme_cls.font_styles["corbelb"] = {
            "large": {
                "line-height": 1.64,
                "font-name": "corbelb",
                "font-size": sp(57),
            },

        }
    
    def switch_theme_style(self):
        self.theme_cls.primary_palette = "Teal" if self.theme_cls.primary_palette == "Green" else "Green"
        self.theme_cls.theme_style = "Light" if self.theme_cls.theme_style == "Dark" else "Dark"


MainApp().run()