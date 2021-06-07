import requests
from tkinter import *
import tkinter as tk
from tkinter import ttk

from requests.api import request


class CurrencyConverter():
    def __init__(self, url):
        self.data = requests.get(url).json()
        self.currencies = self.data['conversion_rates']

    def convert(self, from_currency, to_currency, amount):
        # Convert to USD first
        if from_currency != 'USD':
            amount = amount / self.currencies[from_currency]
        amount = round(amount * self.currencies[to_currency], 4)
        return amount


class CurrencyConverterGUI(tk.Tk):
    def __init__(self, converter):
        tk.Tk.__init__(self)
        self.title = 'Currency Converter'
        self.currency_converter = converter

        self.geometry("500x200")
        # Label
        self.title_label = Label(
            self, text= self.title)
        self.title_label.config(font=('Courier', 15, 'bold'))
        self.date_label = Label(
            self, text=f"Date : {self.currency_converter.data['time_last_update_utc'][:-14]}")
        self.title_label.place(x=150, y=5)
        self.date_label.place(x=175, y=50)

        # Entry box
        self.amount_field = Entry(
            self, bd=3, relief=tk.RIDGE, justify=tk.CENTER)
        self.converted_amount_field_label = Label(
            self, text='', fg='black', bg='white', relief=tk.RIDGE, justify=tk.CENTER, width=17, borderwidth=3)

        # Dropdown
        self.from_currency_variable = StringVar(self)
        self.from_currency_variable.set("USD")  # default value
        self.to_currency_variable = StringVar(self)
        self.to_currency_variable.set("EUR")  # default value

        font = ("Courier", 12, "bold")
        self.option_add('*TCombobox*Listbox.font', font)
        self.from_currency_dropdown = ttk.Combobox(self, textvariable=self.from_currency_variable, values=list(
            self.currency_converter.currencies.keys()), font=font, state='readonly', width=12, justify=tk.CENTER)
        self.to_currency_dropdown = ttk.Combobox(self, textvariable=self.to_currency_variable, values=list(
            self.currency_converter.currencies.keys()), font=font, state='readonly', width=12, justify=tk.CENTER)

        # Placing
        self.from_currency_dropdown.place(x=30, y=120)
        self.amount_field.place(x=30, y=150)
        self.to_currency_dropdown.place(x=340, y=120)
        self.converted_amount_field_label.place(x=340, y=150)

        # Convert button
        self.convert_button = Button(
            self, text="Convert", fg="black", command=self.calculate)
        self.convert_button.config(font=('Courier', 10, 'bold'))
        self.convert_button.place(x=225, y=135)

    def calculate(self,):
        try:
            amount = float(self.amount_field.get())
        except ValueError:
            print("Error: You did not enter a valid number")
        else:

            from_curr = self.from_currency_variable.get()
            to_curr = self.to_currency_variable.get()

            converted_amount = self.currency_converter.convert(
                from_curr, to_curr, amount)
            converted_amount = round(converted_amount, 2)

            self.converted_amount_field_label.config(
                text=str(converted_amount))


url = 'https://v6.exchangerate-api.com/v6/a3d7aaaff8a7851740985d0f/latest/USD'
converter = CurrencyConverter(url)
CurrencyConverterGUI(converter)
mainloop()
