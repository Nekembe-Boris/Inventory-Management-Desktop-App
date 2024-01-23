"""This module is responsible for all the functionalities of the EXIT TAB"""

from tkinter import END, Frame
from tkinter import messagebox
import datetime
import pandas
import customtkinter
from functions import clear, get_values, bind_box, get_details, list_box, listboxin, update, update_input, RecentTransactions, DataInput


class RecentExits(RecentTransactions):
    """
    Displays listboxes that contain recent transactions for the EXIT Tab
    """

    def __init__(self, frame:Frame):

        self.frame = frame
        self.file_name = "Exit"

        super().__init__(self.frame, file=self.file_name)

        self.des_label.config(text="[Recent EXITS]")


class Exit(DataInput):
    """
    - This class displays the Article and Article ID listboxes
    - Also responsible for withdrawing Articles from Stock
    """

    def __init__(self, frame:Frame, updates:RecentExits):
        self.frame = frame
        self.update = updates

        super().__init__(frame=self.frame, updates=self.update)

        self.article_listbox = list_box(frame=self.frame, x_cor=10, y_cor=60, l_height=15, l_width=45)

        self.id_listbox = list_box(frame=self.frame, x_cor=300, y_cor=60, l_height=15, l_width=30)

        self.text_label.config(text="[Select Articles above]")
        self.text_label.place(x=150, y=300)

        self.select_btn.configure(command=self.selected)
        self.select_btn.place(x=10, y=305)

        self.article_entry_label.place(x=200, y=350)

        self.article_entry_entry.config(width=60)
        self.article_entry_entry.place(x=50, y=370)

        self.id_label.place(x=190, y=400)

        self.id_entry.config(width=60)
        self.id_entry.place(x=50, y=420)

        self.article_unit_label.place(x=205, y=450)

        self.unit_entry.config(width=60)
        self.unit_entry.place(x=50, y=470)

        self.current_qlabel.config(text="CURRENT QTY", fg="black")
        self.current_qlabel.place(x=185, y=500)

        self.current_qty_entry.place(x=50, y=520)

        self.exit_qty_label.place(x=200, y=550)
        self.exit_qty_entry.place(x=50, y=570)

        self.cancel_btn.configure(command=self.cancel_tran)
        self.cancel_btn.place(x=340, y=640)

        self.validate_btn.configure(text="Confirm Exit", command=self.validate_exit)
        self.validate_btn.place(x=340, y=700)

        listboxin(self.article_listbox, self.id_listbox)

        bind_box(self.article_listbox, self.id_listbox, func=self.mousewheel)


    def mousewheel(self, event):
        """This function causes the listbox to scroll together"""

        self.article_listbox.yview_scroll(-2 * int(event.delta / 120), "units")
        self.id_listbox.yview_scroll(-2 * int(event.delta / 120), "units")


    def selected(self):
        """
        Uses the get_details function to auto insert the article name, ID, unit and display the current quantity
        """
        clear(self.article_entry_entry, self.id_entry, self.unit_entry, self.qty_entry, self.current_qty_entry)

        try:
            art_name, art_id, art_unit, art_qty = get_details(self.article_listbox)
        except TypeError:
            messagebox.showinfo(
            title="Error",
            message="No ARTICLE was selected\n--\nOnly select from the ARTICLE list"
            )
        else:

            self.article_entry_entry.insert(END, art_name[:-5])
            self.id_entry.insert(END, art_id)
            self.unit_entry.insert(END, art_unit)
            self.current_qty_entry.insert(END, art_qty)


    def cancel_tran(self):
        """Clears all entries for the EXIT Tab"""
        clear(self.article_entry_entry, self.id_entry, self.unit_entry, self.qty_entry, self.current_qty_entry)


    def validate_exit(self):
        """
        - Gets all Article details and ensures that the name, domain and unit of the outbound 
        article is an exact match to any article in stock for the exit to be accepted
        - Appends the transaction data to the Exit, General ledger and Stock level csv 
        files if all conditions have been fulfilled and the file exits (for the Exit file) otherwise, it creates the file and appends the data
        - For the Stock file, it deletes any data relating to the specific article 
        and inserts a new data with an updated quantity (subtracts exit quantity from quantity in stock)
        - For the General Ledger, it registers the quantity with a minus(-) sign to indicate an exit.
        - Uses the Inventory_check function to update the quantity displayed in the Stock Check section
        """

        art_name, art_id, art_unit, cur_qty, exit_qty, *_ = get_values( self.article_entry_entry, self.id_entry, self.unit_entry, self.current_qty_entry, self.exit_qty_entry)

        current_time = datetime.datetime.now()
        date = current_time.strftime("%d-%b-%Y")
        stock_name = f'{art_name}[{art_id[:3]}]'

        try:
            stock_data = pandas.read_csv("./data/Stock_level.csv")
            qty_left = int(cur_qty) - int(exit_qty)
        except (FileNotFoundError, ValueError):
            messagebox.showinfo(
                title="Error",
                message="You do not have any inventory\nOR\nVerify for empty fields"
                )
        else:
            stk_df = pandas.DataFrame(stock_data)
            chosen_article = stock_data[stock_data.Article == stock_name]
            article_dict = chosen_article.to_dict(orient="records")
            old_art_list = stock_data.Article.to_list()

            if art_id != article_dict[0]["ArticleID"] or stock_name != article_dict[0]["Article"] or art_unit != article_dict[0]["Unit"] or int(cur_qty) != article_dict[0]["Quantity"]:
                messagebox.showinfo(
                title="Error",
                message="Do not change any ARTICLE data for the transaction to be successfull"
            )
            
            elif  not exit_qty.isdecimal() or int(exit_qty) < 1:
                messagebox.showinfo(
                    title="Invalid quantity",
                    message="Quantities must be numerical and cannot be less than 1"
                )
            
            elif qty_left < 0:
                messagebox.showinfo(
                    title="Error",
                    message="Insufficient stock"
                )

            else:

                tran_validate = messagebox.askokcancel(
                    title="Confirm Exit",
                    message=f"Article: {art_name}\nArticleID: {art_id}\nUnit: {art_unit}\nQuantity: {exit_qty}"
                )

                if tran_validate is True:

                    exit_data = {
                        "Date" : [date],
                        "Time" : [f"{current_time.strftime('%H:%M:%S')}"],
                        "ArticleID": [art_id],
                        "Article" : [art_name],
                        "Unit" : [art_unit],
                        "Quantity" : [exit_qty]
                    }
                    exit_df = pandas.DataFrame(exit_data)

                    gl_data = {
                        "Date" : [date],
                        "Time" : [f"{current_time.strftime('%H:%M:%S')}"],
                        "ArticleID": [art_id],
                        "Article" : [art_name],
                        "Unit" : [art_unit],
                        "Quantity" : [-int(exit_qty)]                
                    }
                    gl_df = pandas.DataFrame(gl_data)

                    new_stk_data = {
                        "Article": [art_id],
                        "ArticleID" : [stock_name],
                        "Unit" : [art_unit],
                        "Quantity" : [qty_left] 
                    }
                    new_stk_df = pandas.DataFrame(new_stk_data)

                    try:
                        pandas.read_csv("./data/Exit.csv")
                    except FileNotFoundError:
                        exit_df.to_csv("./data/Exit.csv", mode='a', index=False)
                    else:
                        exit_df.to_csv("./data/Exit.csv", mode='a', index=False, header=False)

                    finally:
                        gl_df.to_csv("./data/General_ledger.csv", mode='a', index=False, header=False)

                        for (i, row) in stk_df.iterrows():
                            if row.Article == stock_name:
                                stk_df = stk_df.drop(stk_df.index[i], axis=0)
                                stk_df.to_csv("./data/Stock_level.csv", index=False)
                                new_stk_df.to_csv("./data/Stock_level.csv", mode='a', index=False, header=False)

                    clear(self.article_entry_entry, self.id_entry, self.unit_entry, self.current_qty_entry, self.exit_qty_entry)

                    update(self.update.article_listbox, self.update.ID_listbox, self.update.date_listbox, self.update.quatity_listbox, file="Exit")

                    update_input(self.article_listbox, self.id_listbox, name=stock_name, old_data=old_art_list)
