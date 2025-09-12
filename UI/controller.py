import datetime

import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self.view = view
        # the model, which implements the logic of the program and holds the data
        self.model = model

    def handleCreaGrafo(self, e):
        self.view.txt_result.clean()
        if self.view._ddcategory.value == None or self.view._dp1.value == None or self.view._dp2.value == None:
            self.view.create_alert("Per favore selezionare una Categoria e un Range Di Tempo")
            return
        g = self.model.get_prodotti(self.view._ddcategory.value, self.view._dp1.value.date(), self.view._dp2.value.date())
        self.view.txt_result.controls.append(ft.Text(f"Date Selezionate:"))
        self.view.txt_result.controls.append(ft.Text(f"Start Date: {self.view._dp1.value.date()}"))
        self.view.txt_result.controls.append(ft.Text(f"End Date: {self.view._dp2.value.date()}"))
        self.view.txt_result.controls.append(ft.Text(f"Grafo Correttamente creato:"))
        self.view.txt_result.controls.append(ft.Text(f"Numero di nodi: {self.model.get_nodi()}"))
        self.view.txt_result.controls.append(ft.Text(f"Numero di archi: {self.model.get_archi()}"))

        self.view.update_page()

    def handleBestProdotti(self, e):
        max = self.model.max_vendita()
        self.view.txt_result.controls.append(ft.Text(f"I 5 Prodotti Più Venduti Sono:"))
        for i in max[:5]:
            self.view.txt_result.controls.append(ft.Text(f"{i[1]} ----- Vendite: {i[0]}"))
        self.view.update_page()

    def handleCercaCammino(self, e):
        pass



    def setDates(self):
        first, last = self.model.getDateRange()

        self.view._dp1.first_date = datetime.date(first.year, first.month, first.day)
        self.view._dp1.last_date = datetime.date(last.year, last.month, last.day)
        self.view._dp1.current_date = datetime.date(first.year, first.month, first.day)

        self.view._dp2.first_date = datetime.date(first.year, first.month, first.day)
        self.view._dp2.last_date = datetime.date(last.year, last.month, last.day)
        self.view._dp2.current_date = datetime.date(last.year, last.month, last.day)
        for i in self.model.get_product():
            self.view._ddcategory.options.append(ft.dropdown.Option(key=i, text=i))
        self.view.update_page()

