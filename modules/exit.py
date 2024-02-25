"""
Module responsible for all the functionalities of the EXIT TAB;
- Records the exit of articles and also displays recent exits recorded.
"""

from tkinter import END, Frame, messagebox
import datetime
import pandas
from modules.functions import clear, get_values, bind_box, list_box, update, update_input, RecentTransactions, DataInput


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

    def __init__(self, frame:Frame, updates:RecentExits, path):

        self.frame = frame
        self.update = updates
        self.file_path = path

        super().__init__(frame=self.frame, updates=self.update)

        self.article_listbox = list_box(frame=self.frame, x_cor=10, y_cor=60, l_height=15, l_width=45)

        self.id_listbox = list_box(frame=self.frame, x_cor=300, y_cor=60, l_height=15, l_width=30)

        self.text_label.config(text="[Select Articles above]")
        self.text_label.place(x=150, y=300)


        self.article_entry_label.place(x=200, y=380)

        self.article_entry_entry.configure(width=300)
        self.article_entry_entry.place(x=50, y=320)

        self.id_label.place(x=190, y=460)

        self.id_entry.configure(width=300)
        self.id_entry.place(x=50, y=385)

        self.article_unit_label.place(x=205, y=555)

        self.unit_entry.configure(width=300)
        self.unit_entry.place(x=50, y=460)

        self.current_label.place(x=185, y=635)

        self.current_qty_entry.configure(width=300)
        self.current_qty_entry.place(x=50, y=525)

        self.exit_qty_label.place(x=200, y=710)

        self.exit_qty_entry.place(x=50, y=590)
        self.exit_qty_entry.configure(width=300)

        self.cancel_btn.configure(hover_color="red", command=self.cancel_tran)
        self.cancel_btn.place(x=340, y=640)

        self.validate_btn.configure(hover_color="green",text="Confirm Exit", command=self.validate_exit)
        self.validate_btn.place(x=340, y=700)

        bind_box(self.article_listbox, self.id_listbox, func=self.mousewheel)
        self.article_listbox.bind("<<ListboxSelect>>", self.callback)


    def mousewheel(self, event):
        """This function causes the listbox to scroll together"""

        self.article_listbox.yview_scroll(-2 * int(event.delta / 120), "units")
        self.id_listbox.yview_scroll(-2 * int(event.delta / 120), "units")

    def callback(self, event):
        """
        Auto insert the article name, ID, unit and display the current quantity into their respective entry boxes
        """
        clear(self.article_entry_entry, self.id_entry, self.unit_entry, self.qty_entry, self.current_qty_entry)
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
                    self.current_qty_entry.insert(END, row.Quantity)


    def cancel_tran(self):
        """Clears all entries for the EXIT Tab"""
        clear(self.article_entry_entry, self.id_entry, self.unit_entry, self.qty_entry, self.current_qty_entry)


    def validate_exit(self):
        """
        - Gets all Article details and ensures that the name, ID and unit of the outbound 
        article is an exact match to any article in stock for the exit to be accepted
        - Appends the transaction data to the Exit, General ledger and Stock level csv 
        files if all conditions have been fulfilled and the file exits (for the Exit file) otherwise, it creates the file and appends the data
        - For the Stock file, it deletes any data relating to the specific article 
        and inserts a new data with an updated quantity (subtracts exit quantity from quantity in stock)
        - For the General Ledger, it registers the quantity with a minus(-) sign to indicate an exit.
        """

        art_name, art_id, art_unit, cur_qty, exit_qty, *_ = get_values( self.article_entry_entry, self.id_entry, self.unit_entry, self.current_qty_entry, self.exit_qty_entry)

        current_time = datetime.datetime.now()
        date = current_time.strftime("%d-%b-%Y")
        stock_name = f'{art_name}[{art_id[:3]}]'

        try:
            stock_data = pandas.read_csv(f"{self.file_path}/data/Stock_level.csv")
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

            # line 149 - 162 checks the validity of collected data
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

                    #  General ledger needs a seperate dataframe since it records digit with a (-) in front
                    gl_data = {
                        "Date" : [date],
                        "Time" : [f"{current_time.strftime('%H:%M:%S')}"],
                        "ArticleID": [art_id],
                        "Article" : [art_name],
                        "Unit" : [art_unit],
                        "Quantity" : [-int(exit_qty)]                
                    }
                    gl_df = pandas.DataFrame(gl_data)

                    #dataframe for stockfile
                    new_stk_data = {
                        "Article": [art_id],
                        "ArticleID" : [stock_name],
                        "Unit" : [art_unit],
                        "Quantity" : [qty_left] 
                    }
                    new_stk_df = pandas.DataFrame(new_stk_data)

                    try:
                        pandas.read_csv(f"{self.file_path}/data/Exit.csv")
                    except FileNotFoundError:
                        exit_df.to_csv(f"{self.file_path}/data/Exit.csv", mode='a', index=False)
                    else:
                        exit_df.to_csv(f"{self.file_path}/data/Exit.csv", mode='a', index=False, header=False)

                    finally:
                        gl_df.to_csv(f"{self.file_path}/data/General_ledger.csv", mode='a', index=False, header=False)

                        #updating the article qty in Stock csv file
                        for (i, row) in stk_df.iterrows():
                            if row.Article == stock_name:
                                stk_df = stk_df.drop(stk_df.index[i], axis=0)
                                stk_df.to_csv(f"{self.file_path}/data/Stock_level.csv", index=False)
                                new_stk_df.to_csv(f"{self.file_path}/data/Stock_level.csv", mode='a', index=False, header=False)

                    clear(self.article_entry_entry, self.id_entry, self.unit_entry, self.current_qty_entry, self.exit_qty_entry)

                    update(self.update.article_listbox, self.update.ID_listbox, self.update.date_listbox, self.update.quatity_listbox, self.update.time_listbox, file="Exit", path=self.file_path)

                    update_input(self.article_listbox, self.id_listbox, name=stock_name, old_data=old_art_list, path=self.file_path)
