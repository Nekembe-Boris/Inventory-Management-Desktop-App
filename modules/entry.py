"""
This module is responsible for all the functionalities of the ENTRY TAB;
- Recording the entry of articles whether new or already existing
- Displays the all recent entries
"""

from tkinter import Frame, END
from tkinter import messagebox
import datetime
import pandas
from modules.functions import clear, forget, get_values, bind_box, list_box, listboxin, update, update_input, RecentTransactions, DataInput
from modules.exit import Exit


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
    def __init__(self, frame:Frame, updates:RecentEntries,  exit_up:Exit, path):

        self.frame = frame
        self.update = updates
        self.exit_updates = exit_up
        self.file_path = path

        super().__init__(frame=self.frame, updates=self.update)

        self.article_listbox = list_box(frame=self.frame, x_cor=10, y_cor=60, l_height=25, l_width=45)

        self.id_listbox = list_box(frame=self.frame, x_cor=300, y_cor=60, l_height=25, l_width=30)

        self.text_label.place(x=150, y=465)

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

        listboxin(self.article_listbox, self.id_listbox, path=self.file_path)

        bind_box(self.article_listbox, self.id_listbox, func=self.mousewheel)
        self.article_listbox.bind("<<ListboxSelect>>", self.callback)


    def mousewheel(self, event):
        """This function causes the listbox to scroll together"""
        self.article_listbox.yview_scroll(-2 * int(event.delta / 120), "units")
        self.id_listbox.yview_scroll(-2 * int(event.delta / 120), "units")


    def callback(self, event):
        """
        Based on the article selected:
        - It auto insert the article name, ID, unit into their respective entry boxes
        - Displays the current quantity at the bottom of the tab
        """
        clear(self.article_entry_entry, self.id_entry, self.unit_entry, self.qty_entry)
        selected = event.widget.curselection()
        if selected:
            # art_index = selected[0]
            art_data = event.widget.get(selected[0])
            stock_data = pandas.read_csv(f"{self.file_path}/data/Stock_level.csv")

            for (_ , row) in stock_data.iterrows():
                if row.Article[:-5] == art_data:
                    self.article_entry_entry.insert(END, row.Article[:-5])
                    self.id_entry.insert(END, row.ArticleID)
                    self.unit_entry.insert(END, row.Unit)
      


    def cancel_tran(self):
        """Clears all entries for the entry tab and also hides Current quantity Labels"""

        clear(self.article_entry_entry, self.id_entry, self.unit_entry, self.qty_entry)
        forget(self.current_label, self.current_qlabel)


    def validate_entry(self):
        """
        - Gets all Article details and the date
        - Ensure a descriptive Article name and ID 
        - Ensures that only integers are entered as quantity
        - Appends the transaction data to the Entries, General ledger and 
        Stock level csv files if all conditions have been fulfilled 
        and the file exists otherwise, it creates the files and appends the data
        - If the Article is already in stock and the Article to be stored has the same ARTICLEID 
        as the Article in stock, it deletes the previous Article data 
        and inserts a new data with an updated quantity (adds current quantity to new quantity)
        - Uses the UPDATE and UPDATE_INPUT functions to update all the Article and Article ID on the Exit and Entry Tabs
        """

        current_time = datetime.datetime.now()
        date = current_time.strftime("%d-%b-%Y")
        fiscal_year = int(self.file_path[-4:])
        old_art_list = []

        if fiscal_year < int(current_time.year):
            messagebox.showinfo(
                title="Not Allowed!!",
                message= "Transactions can't be registered after the year is has ended\nCreate a new directory (for the year) for this project and start recording"
            )
        else:
            art_name, art_id, art_unit, art_qty, *_ = get_values(self.article_entry_entry, self.id_entry, self.unit_entry, self.qty_entry)
            stock_name = f"{art_name.upper()}[{art_id[:3].title()}]"

            # line 136 - 146 checks the validity of inputs
            if len(art_name) < 7 or len(art_id) < 4:
                messagebox.showinfo(
                    title="Article Error",
                    message="Please enter a descriptive and simple Article name/ID that will distinguish it from similar materials\nAlso ensure the ARTICLEID is not empty"
                )
            elif len(art_unit) < 1 or not art_unit.isalpha():
                messagebox.showinfo(
                    title="Modify Unit box",
                    message="Please enter a more descriptive Units\nOnly use alphabetic characters"
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

                if tran_validate:

                    # creating a dataframe for registration in Entries and General ledger
                    new_data = {
                        "Date" : [date],
                        "Time" : [f"{current_time.strftime('%H:%M:%S')}"],
                        "ArticleID": [art_id.title()],
                        "Article" : [art_name.upper()],
                        "Unit" : [art_unit.lower()],
                        "Quantity" : [art_qty]
                    }
                    d_f = pandas.DataFrame(new_data)

                    # dataframe for Stockfile
                    stk_data = {
                        "ArticleID": [art_id.title()],
                        "Article" : [stock_name],
                        "Unit" : [art_unit.lower()],
                        "Quantity" : [art_qty]
                    }
                    new_stk_df = pandas.DataFrame(stk_data)

                    try:
                        pandas.read_csv(f"{self.file_path}/data/Stock_level.csv")
                    except FileNotFoundError:
                        new_stk_df.to_csv(f"{self.file_path}/data/Stock_level.csv", mode='a', index=False)
        
                    try:
                        pandas.read_csv(f"{self.file_path}/data/Entries.csv")
                    except FileNotFoundError:
                        d_f.to_csv(f"{self.file_path}/data/Entries.csv", mode='a', index=False)
                        d_f.to_csv(f"{self.file_path}/data/General_ledger.csv", mode='a', index=False)
                    else: # only appends relevent new data to the existing file
                        stock_data = pandas.read_csv(f"{self.file_path}/data/Stock_level.csv")
                        stk_df = pandas.DataFrame(stock_data)
                        d_f.to_csv(f"{self.file_path}/data/Entries.csv", mode='a', index=False, header=False)
                        d_f.to_csv(f"{self.file_path}/data/General_ledger.csv", mode='a', index=False, header=False)

                        old_art_list.extend(stock_data.Article.to_list())
                        stock_lenght = len(stock_data.Article.to_list())

                        for (i, row) in stk_df.iterrows():

                            if row.Article == stock_name and row.ArticleID == art_id:  # checks if Article and ArticleID are the same

                                stk_df = stk_df.drop(stk_df.index[i], axis=0) # deletes the row with the old article info if it is match
                                stk_df.to_csv(f"{self.file_path}/data/Stock_level.csv", index=False) # saves new file

                                #creates a dataframe that with new quantity for the article and appends to stockfile
                                updated_data = {
                                    "ArticleID": [art_id.title()],
                                    "Article" : [stock_name],
                                    "Unit" : [art_unit.lower()],
                                    "Quantity" : [int(art_qty) + row.Quantity]
                                }
                                updated_stk_df = pandas.DataFrame(updated_data)
                                updated_stk_df.to_csv(f"{self.file_path}/data/Stock_level.csv", mode='a', index=False, header=False)

                                #an indicator for a succesfull procedure
                                stock_lenght -= 1

                        #This line of code checks to see if a new record was created to avoid duplicating entries in case the article is being recorded for the 1st time
                        if stock_lenght == len(stock_data.Article.to_list()):
                            new_stk_df.to_csv(f"{self.file_path}/data/Stock_level.csv", mode='a', index=False, header=False)

                    clear(self.article_entry_entry, self.id_entry, self.unit_entry, self.qty_entry)
                    update(self.update.article_listbox, self.update.ID_listbox, self.update.date_listbox, self.update.quatity_listbox, self.update.time_listbox, file="Entries", path=self.file_path)
                    update_input(self.article_listbox, self.id_listbox, self.exit_updates.article_listbox, self.exit_updates.id_listbox, name=stock_name, old_data=old_art_list, path=self.file_path)
                    forget(self.current_label, self.current_qlabel)
