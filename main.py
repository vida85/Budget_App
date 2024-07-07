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

import os
import json
from typing import Any, Dict



cwd = os.path.dirname(os.path.abspath(__file__))
json_file_path = os.path.join(cwd, "budget_data.json")



def load_data() -> json:
    print('loading data')
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)
        return data


def save_data(data: Dict[str, Any], file_path: str=json_file_path) -> True:
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)
    return True



if os.path.exists(json_file_path):
    data = load_data()
    print('data, loaded')
else:
    data = {
        "budget": None,
        "balance": None,
        "items": {"item": None,
                  "description": None,
                  "amount": None},
    }
    print('data, empty')
    save_data(data)



class BudgetInterface(MDBoxLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.padding = sp(30)
        self.spacing = sp(10)

        self.total = 0
        self.balance = 0
        self.budget = 0
        self.items = []

    def __post_init__(self):
        self.load_items()


    def load_items(self):
        print(data, ' loading file')
        self.budget = data["budget"]
        self.balance = data["balance"]
        self.items = data["items"]

        for item in self.items:
            print(item["item"], item["description"], item["amount"])
            self.update_list(item["item"], item["description"], item["amount"])
        

    def add_item(self):
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
            self.update_list(self, item, description, amount)
            self.update_total_expenses(amount=amount)
            self.save_data(item, description, amount)
            self.ids.item.text = ''
            self.ids.description.text = ''
            self.ids.amount.text = ''


    def update_list(self, item, description, amount):
        self.ids.item_list.add_widget(
                        MDListItem(
                            MDListItemHeadlineText(text=item, ),
                            MDListItemLeadingIcon(icon='cash', ),
                            MDListItemSupportingText(text=description, ),
                            MDListItemTertiaryText(text=f"${amount}", ),
                            MDListItemTrailingCheckbox(icon='checkbox-blank-outline', ),
                            pos_hint={"center_x": .5, "center_y": .5}, size_hint_x=0.8,),
                        )


    def update_total_expenses(self, amount: float | str):
            try:
                amount = float(amount)
            except ValueError:
                print('Must be numbers only')
                return
            self.total += amount
            self.balance = self.update_income(value=self.total)
            self.ids.total.text = str(f"Total Expenses: ${round(self.total, 2)}")

    
    def update_income(self, value: float=0):
        if value:
            try:
                income = float(self.ids.income.text)
            except ValueError:
                income = 0
            balance = round(income - value, 2)
        else:
            try:
                balance = float(self.ids.income.text)
            except ValueError:
                balance = 0

        self.ids.balance.text = f'Balance: ${balance}'
        return balance


    def save_data(self, item: str, description: str, amount: str):
        item = {"item": item,
                  "description": description,
                  "amount": amount}
        self.items.append(item)
        
        item_data = {
            "budget": self.budget,
            "balance": self.balance,
            "items": self.items
                    }
        save_data(item_data)



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