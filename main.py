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

# from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.floatlayout import MDFloatLayout


class BudgetInterface(MDBoxLayout):
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
            
            self.total += float(amount)
            self.ids.total.text = str(f"${round(self.total, 2)}")
    
            self.ids.item.text = ''
            self.ids.description.text = ''
            self.ids.amount.text = ''


    def add_items(self):
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
            name="corbell",
            fn_regular="fonts/corbell.ttf", )

        LabelBase.register(
            name="corbelb",
            fn_regular="fonts/corbelb.ttf", )

        self.theme_cls.font_styles["corbell"] = {
            "large": {
                "line-height": 1.64,
                "font-name": "corbell",
                "font-size": sp(14),
            },

        }
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