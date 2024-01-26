"""Module tasked with the Verify Qty and Reports section of the ADVANCED TAB"""

from tkinter import Frame, Label, IntVar, END
from tkinter import messagebox
from tktooltip import ToolTip
import os
import pandas
import customtkinter
from functions import clear, list_box, listboxin
from entry import Input
from exit import Exit

FG = "white"
BACKGROUND_COLOR = "#212121"
report_type = ["Entry Records", "Exit Records", "Ledger Records", "Current Stock Level", "Removed From Stock"]
FONT1=("Century Gothic", 12, "bold")
FONT2=("Century Gothic", 10, "bold")
FONT3 = ("Century Gothic", 8, "bold")


class StockLook():
    """
    - Class tasked with allowing the user to verify the quantity of an Atricle,
    Delete an Article from Stock.
    - Can also generate ENTRY, EXIT, LEDGER and STOCK LEVEL reports
    """
    def __init__(self, frame:Frame, entry_update:Input, exit_update:Exit):
        self.frame = frame
        self.entry_update = entry_update
        self.exit_update = exit_update

        self.in_label = Label(master=self.frame, text="[VERIFY QTY]", font=FONT2, bg=BACKGROUND_COLOR, fg=FG)
        self.in_label.place(x=200, y=50)

        self.art_id_entry = customtkinter.CTkEntry(master=self.frame, width=120, placeholder_text="Article ID", takefocus=0)
        self.art_id_entry.place(x=10, y=120)

        self.ch_qty_entry = customtkinter.CTkEntry(master=self.frame, width=120, placeholder_text="Quantity in Stock", takefocus=0)
        self.ch_qty_entry.place(x=10, y=170)

        self.ch_listbox = list_box(frame=self.frame, x_cor=300, y_cor=100, l_height=20, l_width=50)

        self.select_btn = customtkinter.CTkButton(master=self.frame, text=" Select  ", font=FONT3, command=self.check, width=80)
        self.select_btn.place(x=150, y=240)

        self.refresh_btn = customtkinter.CTkButton(master=self.frame, text=" Refresh", font=FONT3, command=self.refresh, width=80)
        self.refresh_btn.place(x=150, y=280)

        self.remove_btn = customtkinter.CTkButton(master=self.frame, text="Remove", font=FONT3, command=self.rem_in_stock, width=80)
        self.remove_btn.place(x=150, y=320)

        ToolTip(self.select_btn, msg="Select Article from Box and click to see details")
        ToolTip(self.refresh_btn, msg="Refresh to Update Inventory")
        ToolTip(self.remove_btn, msg="Remove Selected Article from Inventory")

        self.report_label = Label(master=self.frame,text="[RECORDS]", font=FONT2, bg=BACKGROUND_COLOR, fg=FG)
        self.report_label.place(x=150, y=600)

        self.radio_state = IntVar()
        x_cor = 10
        y_cor = 500

        for r_int, report in enumerate(report_type, 1):
            gen_radiobutton = customtkinter.CTkRadioButton(master=frame, text=report, value=r_int, variable=self.radio_state, font=FONT2)
            gen_radiobutton.place(x=x_cor, y=y_cor)
            y_cor += 50

        self.gen_excel_btn = customtkinter.CTkButton(master=frame, text="GENERATE EXCEL SHEET",  font=FONT2, hover_color="green", command=self.generate_excel)
        self.gen_excel_btn.place(x=170, y=600)

        listboxin(self.ch_listbox)


    def refresh(self):
        """Reloads the listbox to get current stock data"""
        clear(self.ch_listbox)

        listboxin((self.ch_listbox))


    def check(self):
        """
        - Loops through the stock data to update the quantity and inserts the ArticleID and quantity of the selected material in their entries so that the current stock quantity can be known
        """
        selected = ""

        clear( self.art_id_entry, self.ch_qty_entry)

        for _ in self.ch_listbox.curselection():
            selected = self.ch_listbox.get(self.ch_listbox.curselection())

        try:
            stock_data = pandas.read_csv("./data/Stock_level.csv")
        except FileNotFoundError:
            print("No data")
        else:
            for (_, row) in stock_data.iterrows():

                if row.Article == selected:

                    self.art_id_entry.insert(END, row.ArticleID)
                    self.ch_qty_entry.insert(END, row.Quantity)


    def generate_excel(self):
        """
        Based on the record type chosen, this function will automatically create an xlsx file and open the file in MICROSOFT EXCEL
        """
        record_type = ["Entries", "Exit", "General_ledger", "Stock_level", "Removed"]

        radio_get = self.radio_state.get() - 1

        if radio_get < 0 :
            messagebox.showinfo(
                title="Error",
                message="No record was selected",
            )
        else:
            try:
                data = pandas.read_csv(f"./data/{record_type[radio_get]}.csv")
            except FileNotFoundError:
                messagebox.showinfo(
                    title="Error",
                    message="Record does not exit"
                )
            else:
                data.to_excel(f"./reports/{record_type[radio_get]}.xlsx", index=False)
                os.system(f'start "excel" "./reports/{record_type[radio_get]}.xlsx"')
            self.radio_state.set(-1)


    def rem_in_stock(self):
        """
        - Removes an Article from Stock and stores it in the Removed csv file.
        - Automatically updates the Article and ArticleID listboxes on the ENTRY and EXIT Tab
        """
        for i in self.ch_listbox.curselection():
            selected = self.ch_listbox.get(i)

        if not selected:
            messagebox.showinfo(
                    title="Error",
                    message="No Article was selected"
                )
        else:
            try:
                data = pandas.read_csv("./data/Stock_level.csv")
            except FileNotFoundError:
                messagebox.showinfo(
                        title="Error",
                        message="No Inventory"
                    )
            else:
                confirm = messagebox.askokcancel(
                        title="CONFIRM",
                        message=f"You are about to remove {selected} from Inventory"
                    )
                if confirm is True:

                    validate = messagebox.askokcancel(
                        title="VALIDATE",
                        message="Action can not be reversed.\nProceed?"
                    )

                    if validate is True:
                        del_data = data[data.Article == selected]
                        rem_data = pandas.DataFrame(del_data)
                        sheet_data = pandas.DataFrame(data)
                        try:
                            pandas.read_csv("./data/Removed.csv")
                        except FileNotFoundError:
                            rem_data.to_csv("./data/Removed.csv", mode='a', index=False)
                        else:
                            rem_data.to_csv("./data/Removed.csv", mode='a', index=False, header=False)

                        for (i, row) in sheet_data.iterrows():

                            if row.Article == selected:
                                sheet_data = data.drop(data.index[i], axis=0)
                                sheet_data.to_csv("./data/Stock_level.csv", index=False)

                        del_index = self.ch_listbox.get(0, END).index(selected)
                        self.ch_listbox.delete(del_index)

                        clear(self.entry_update.article_listbox, self.entry_update.id_listbox, self.exit_update.article_listbox, self.exit_update.id_listbox)

                        listboxin(self.entry_update.article_listbox, self.entry_update.id_listbox)
                        listboxin(self.exit_update.article_listbox, self.exit_update.id_listbox)
