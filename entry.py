"""This module is responsible for all the functionalities of the ENTRY TAB"""

from tkinter import Frame, END
from tkinter import messagebox
import datetime
from functions import clear, forget, get_values, bind_box, get_details, list_box, listboxin, update, update_input, RecentTransactions, DataInput
from exit import Exit
import pandas

FONT3 = ("Century Gothic", 8, "bold")


class RecentEntries(RecentTransactions):
    """
    Displays listboxes that contain recent transactions for the ENTRY Tab
    """

    def __init__(self, frame:Frame):

        self.frame = frame
        self.file_name = "Entries"

        super().__init__(self.frame, file=self.file_name)

        self.des_label.config(text="[Recent ENTRIES]")


class Input(DataInput):
    """
    - This class displays the Article and Article ID listboxes
    - Also responsible for registering ENTRIES
    """
    def __init__(self, frame:Frame, updates:RecentEntries,  exit_up:Exit):

        self.frame = frame
        self.update = updates
        self.exit_updates = exit_up

        super().__init__(frame=self.frame, updates=self.update)

        self.article_listbox = list_box(frame=self.frame, x_cor=10, y_cor=60, l_height=25, l_width=45)

        self.id_listbox = list_box(frame=self.frame, x_cor=300, y_cor=60, l_height=25, l_width=30)

        self.text_label.place(x=150, y=465)

        self.select_btn.configure(width=80, command=self.selected)
        self.select_btn.place(x=10, y=375)

        self.article_entry_label.place(x=10, y=550)

        self.article_entry_entry.place(x=10, y=465)

        self.id_label.place(x=10, y=640)

        self.id_entry.place(x=10, y=535)

        self.article_unit_label.place(x=10, y=725)

        self.unit_entry.place(x=10, y=600)

        self.article_qty_label.place(x=10, y=810)

        self.qty_entry.place(x=10, y=670)

        self.cancel_btn.configure(hover_color="red", command=self.cancel_tran)
        self.cancel_btn.place(x=350, y=560)

        self.validate_btn.configure(text="Confirm Entry", hover_color="green", command=self.validate_entry)
        self.validate_btn.place(x=350, y=640)

        listboxin(self.article_listbox,  self.id_listbox)

        bind_box(self.article_listbox,  self.id_listbox, func=self.mousewheel)


    def mousewheel(self, event):
        """This function causes the listbox to scroll together"""
        self.article_listbox.yview_scroll(-2 * int(event.delta / 120), "units")
        self.id_listbox.yview_scroll(-2 * int(event.delta / 120), "units")


    def selected(self):
        """
        Uses the get_details function to auto insert the article name, ID, unit and display the current quantity
        """
        clear(self.article_entry_entry, self.id_entry, self.unit_entry, self.qty_entry)
        try:
            art_name, art_id, art_unit, art_qty = get_details(self.article_listbox)
        except TypeError:
            messagebox.showinfo(
            title="Error",
            message="No ARTICLE was selected\n--\nOnly select from the ARTICLE list"
            )
        else:

            self.current_label.place(x=10, y=920)
            self.current_qlabel.place(x=80, y=920)

            self.article_entry_entry.insert(END, art_name[:-5])
            self.id_entry.insert(END, art_id)
            self.unit_entry.insert(END, art_unit)
            self.current_qlabel.config(text=art_qty)

    def cancel_tran(self):
        """Clears all entries for the entry tab and also hides Current quantity Labels"""

        clear(self.article_entry_entry, self.id_entry, self.unit_entry, self.qty_entry)
        forget(self.current_label, self.current_qlabel)


    def validate_entry(self):
        """
        - Gets all Article details and the date, ensure a descriptive Article name/ID, 
        ensures that only integers are entered as quantity
        - Appends the transaction data to the Entries, General ledger and 
        Stock level csv files if all conditions have been fulfilled 
        and the file exits otherwise, it creates the files and appends the data
        - If the Article is already in stock and the Article to be stored has the same ARTICLEID 
        as the Article in stock, it deletes the previous Article data 
        and inserts a new data with an updated quantity 
        (adds current quantity to new quantity)
        - Uses the UPDATE and UPDATE_INPUT functionsto all the Article and Article ID on theExit and Entry Tabs
        """

        current_time = datetime.datetime.now()
        date = current_time.strftime("%d-%b-%Y")

        art_name, art_id, art_unit, art_qty, *_ = get_values(self.article_entry_entry, self.id_entry, self.unit_entry, self.qty_entry)
        stock_name = f"{art_name.upper()}[{art_id[:3].title()}]"

        if len(art_name) < 7 or len(art_id) < 4:
            messagebox.showinfo(
                title="Article Error",
                message="Please enter a descriptive and simple Article name/ID that will distinguish it from similar materials\nAlso ensure the ARTICLEID is not empty"
            )
        elif len(art_unit) < 1 or not art_unit.isalpha():
            messagebox.showinfo(
                title="Modify Unit box",
                message="Please enter a more descriptive Units to distinguish it from similar materials\nOnly use alphabetic characters"
            )
        elif not art_qty.isdecimal() or int(art_qty) < 1 :
            messagebox.showinfo(
                title="Invalid quantity",
                message="Quantities must be numerical and cannot be less than 1"
            )
        else:

            tran_validate = messagebox.askokcancel(
                title="Confirm Entry",
                message=f"Article: {art_name.upper()}\nArticleID: {art_id.title()}\nUnit: {art_unit}\nQuantity: {art_qty}"
                )

            if tran_validate is True:
                new_data = {
                    "Date" : [date],
                    "Time" : [f"{current_time.strftime('%H:%M:%S')}"],
                    "ArticleID": [art_id.title()],
                    "Article" : [art_name.upper()],
                    "Unit" : [art_unit.lower()],
                    "Quantity" : [art_qty]
                }
                d_f = pandas.DataFrame(new_data)

                stk_data = {
                    "ArticleID": [art_id.title()],
                    "Article" : [stock_name],
                    "Unit" : [art_unit.lower()],
                    "Quantity" : [art_qty]
                }
                new_stk_df = pandas.DataFrame(stk_data)

                try:
                    pandas.read_csv("./data/Entries.csv")
                    pandas.read_csv("./data/General_ledger.csv")
                    stock_data = pandas.read_csv("./data/Stock_level.csv")
                except FileNotFoundError:
                    d_f.to_csv("./data/Entries.csv", mode='a', index=False)
                    d_f.to_csv("./data/General_ledger.csv", mode='a', index=False)
                    new_stk_df.to_csv("./data/Stock_level.csv", mode='a', index=False)
                    old_art_list = []
                else:
                    stk_df = pandas.DataFrame(stock_data)
                    d_f.to_csv("./data/Entries.csv", mode='a', index=False, header=False)
                    d_f.to_csv("./data/General_ledger.csv", mode='a', index=False, header=False)

                    old_art_list = stock_data.Article.to_list()
                    stock_lenght = len(stock_data.Article.to_list())

                    for (i, row) in stk_df.iterrows():

                        if row.Article == stock_name and row.ArticleID == art_id:

                            stk_df = stk_df.drop(stk_df.index[i], axis=0)
                            stk_df.to_csv("./data/Stock_level.csv", index=False)

                            updated_data = {
                                "ArticleID": [art_id.title()],
                                "Article" : [stock_name],
                                "Unit" : [art_unit.lower()],
                                "Quantity" : [int(art_qty) + row.Quantity]
                            }
                            updated_stk_df = pandas.DataFrame(updated_data)
                            updated_stk_df.to_csv("./data/Stock_level.csv", mode='a', index=False, header=False)
                            stock_lenght -= 1

                    #This line of code checks to see if a new record was created to avoid duplicating entries
                    if stock_lenght == len(stock_data.Article.to_list()):
                        new_stk_df.to_csv("./data/Stock_level.csv", mode='a', index=False, header=False)

                clear(self.article_entry_entry, self.id_entry, self.unit_entry, self.qty_entry)


                update(self.update.article_listbox, self.update.ID_listbox, self.update.date_listbox, self.update.quatity_listbox, file="Entries")

                update_input(self.article_listbox, self.id_listbox, self.exit_updates.article_listbox, self.exit_updates.id_listbox, name=stock_name, old_data=old_art_list)

                forget(self.current_label, self.current_qlabel)
