"""This module contains functions and Classes that is repeatedly used by all the other scripts"""

from tkinter import Frame, Listbox, Label, Entry, END, Button
import customtkinter
import pandas

FG = "white"
BACKGROUND_COLOR = "#282828"
SKY_BLUE = "#87CEEB"
FONT1=("Century Gothic", 12, "bold")
FONT2=("Century Gothic", 10, "bold")
FONT3 = ("Century Gothic", 8, "bold")


def clear(*args):
    """Clears the text in any entry widget that is passed as an argument"""
    for n in args:
        n.delete(0, END)

def forget(*args):
    """automatically hides any widget"""
    for n in args:
        n.place_forget()

def get_values(*args):
    """
    gets the values from any entry widget, stores it in a list 
    and returns a tuple containing all the results that can easily be unpacked
    """
    result = []
    for n in args:
        result.append(n.get())
    return tuple(result)


def bind_box(*args, func):
    """Binds mouse scroll to listboxes"""
    for n in args:
        n.bind("<MouseWheel>", func)


def get_details(listbox):
    """
    :param listbox - Listbox to get Article metadata

    Gets the Article, Article ID, Unit and Quantity of the selected material and returns them.
    """

    stock_data = pandas.read_csv("./data/Stock_level.csv")
    selected = ""

    for i in listbox.curselection():
        selected = listbox.get(i)

    for (_ , row) in stock_data.iterrows():

        if row.Article[:-5] == selected:
            return row.Article, row.ArticleID, row.Unit, row.Quantity
    return None


def list_box(frame:Frame, x_cor:int, y_cor:int, l_height:int, l_width:int):
    """
    :param frame - The frame the listbox will be created in
    :param x_cor - The x coordinate of the listbox
    :param y_cor - The y coordinate of the listbox
    :param l_height - The desired lenght of the listbox
    :param l_width - The desired width of the listbox


    This function lets you create a listbox and also define the height and width you desire
    """
    listbox = Listbox(master=frame, height=l_height, width=l_width)
    listbox.place(x=x_cor, y=y_cor)

    return listbox


def style_bg(box, length:int):
    """
    :param box - listbox to be modified
    :param lenght - number of times to iterate
    
    Styles the background of a listbox
    """
    for line in box:
        for i in range(0, length):
            line.itemconfigure(i, bg="white")

    for line in box:
        for i in range(0, length, 2):
            line.itemconfigure(i, bg=SKY_BLUE)


def listboxin(*box):
    """
    :param *box - listbox to be modified

    This function is responsible for inserting data into the Article and Article ID listbox
    """

    try:
        stock_data = pandas.read_csv("./data/Stock_level.csv")
    except FileNotFoundError:
        print("No data")
    else:

        article_list = stock_data.Article.to_list()
        article_id_list = stock_data.ArticleID.to_list()

        rev_index = len(article_list)

        if len(box)<2:
            for item in article_list:
                box[0].insert(0, item)
        else:
            for item in article_list:
                box[0].insert(0, item[:-5])

            for item in article_id_list:
                box[1].insert(0, item)

        style_bg(box, length=rev_index)


def insert_info(*box, file):
    """
    :param *box - listbox to be modified
    :param file - File to upload data that will be used by the listboxes

    This function is responsible for inserting data into all Recent Transaction listbox
    """
    try:

        data = pandas.read_csv(f"./data/{file}.csv")
    except FileNotFoundError:
        print("No data")
    else:

        entries_article_list = data.Article.to_list()
        entries_article_id_list = data.ArticleID.to_list()
        entries_date_list = data.Date.to_list()
        entries_qty_list = data.Quantity.to_list()

        rev_index = len(entries_date_list)

        for item in entries_article_list:
            box[0].insert(0, item)

        for item in entries_article_id_list:
            box[1].insert(0, item)

        for item in entries_date_list:
            box[2].insert(0, item)

        for item in entries_qty_list:
            box[3].insert(0, item)

        style_bg(box, length=rev_index)


def update(*box, file):

    """
    :param *box - listbox to be modified
    :param file - File to upload data that will be used by the listboxes
    This function is responsible for updating data Recent Transactions listboxes
    """
    try:

        data = pandas.read_csv(f"./data/{file}.csv")
    except FileNotFoundError:
        print("No data")
    else:

        entries_article_list = data.Article.to_list()
        entries_article_id_list = data.ArticleID.to_list()
        entries_date_list = data.Date.to_list()
        entries_qty_list = data.Quantity.to_list()
        rec_rev_index = len(entries_article_list)

        box[0].insert(0, entries_article_list[-1])
        box[1].insert(0, entries_article_id_list[-1])
        box[2].insert(0,  entries_date_list[-1])
        box[3].insert(0,  entries_qty_list[-1])

        style_bg(box, length=rec_rev_index)


def update_input(*box, name:str, old_data:list):
    """
    :param *box - listbox to be updated
    :param name - name of Article to be inserted
    :param old_data - old Article List obtained from Stock_level before entry
    
    Updates the Article and ArticleID listboxes across all TABS
    """

    try:
        stock_data = pandas.read_csv("./data/Stock_level.csv")
    except FileNotFoundError:
        print("No data")
    else:

        article_list = stock_data.Article.to_list()
        article_id_list = stock_data.ArticleID.to_list()

        if name not in old_data:
            box[0].insert(0, article_list[-1][:-5])
            box[1].insert(0, article_id_list[-1])
            box[2].insert(0, article_list[-1][:-5])
            box[3].insert(0, article_id_list[-1])

        style_bg(box, length=len(article_list))


class RecentTransactions():
    """
    This class responsible for creating listboxes that display recent transactions
    """

    def __init__(self, frame:Frame, file):

        self.frame = frame
        self.file_name = file

        self.des_label = Label(master=self.frame, text="", font=FONT2, fg="white", bg=BACKGROUND_COLOR)
        self.des_label.place(x=320, y=10)

        self.article_label= Label(master=self.frame, text="Article", font=FONT3, bg=BACKGROUND_COLOR, fg=FG)
        self.article_label.place(x=155, y=45)

        self.id_label= Label(master=self.frame, text="Article ID", font=FONT3, bg=BACKGROUND_COLOR, fg=FG)
        self.id_label.place(x=355, y=45)

        self.date_label= Label(master=self.frame, text="Date", font=FONT3, bg=BACKGROUND_COLOR, fg=FG)
        self.date_label.place(x=530, y=45)

        self.qty_label= Label(master=self.frame, text="QTY", font=FONT3, bg=BACKGROUND_COLOR, fg=FG)
        self.qty_label.place(x=640, y=45)

        self.article_listbox = list_box(frame=self.frame, x_cor=80, y_cor=70, l_height=40, l_width=35)

        self.ID_listbox = list_box(frame=self.frame, x_cor=300, y_cor=70, l_height=40, l_width=30)

        self.date_listbox = list_box(frame=self.frame, x_cor=490, y_cor=70, l_height=40, l_width=20)

        self.quatity_listbox = list_box(frame=self.frame, x_cor=620, y_cor=70, l_height=40, l_width=10)

        bind_box(self.article_listbox, self.ID_listbox, self.date_listbox, self.quatity_listbox, func=self.mousewheel)
        insert_info(self.article_listbox, self.ID_listbox, self.date_listbox, self.quatity_listbox, file=self.file_name)

    def mousewheel(self, event):
        """Responsible for binding all listboxes to mousewheel"""
        self.article_listbox.yview_scroll(-2 * int(event.delta / 120), "units")
        self.ID_listbox.yview_scroll(-2 * int(event.delta / 120), "units")
        self.date_listbox.yview_scroll(-2 * int(event.delta / 120), "units")
        self.quatity_listbox.yview_scroll(-2 * int(event.delta / 120), "units")



class DataInput():

    def __init__(self, frame:Frame, updates):

        self.frame = frame
        self.update = updates

        self.article_listbox = ""

        self.article_label = Label(master=self.frame, text="ARTICLE", font=FONT1, fg=FG, bg=BACKGROUND_COLOR)
        self.article_label.place(x=120, y=35)

        self.articleid_label = Label(master=self.frame, text="ARTICLE ID", font=FONT1, fg=FG, bg=BACKGROUND_COLOR)
        self.articleid_label.place(x=350, y=35)

        self.select_btn = customtkinter.CTkButton(master=self.frame, text="Select", font=FONT3)

        self.text_label = Label(master=self.frame, text="[Select existing ARTICLE]", font=FONT3, fg="red", bg=BACKGROUND_COLOR)

        self.article_entry_label= Label(master=self.frame, text="ARTICLE", font=FONT3, fg=FG, bg=BACKGROUND_COLOR)

        self.article_entry_entry = Entry(master=self.frame, width=50)

        self.id_label = Label(master=self.frame, text="ARTICLE ID", font=FONT3, fg=FG, bg=BACKGROUND_COLOR)

        self.id_entry = Entry(master=self.frame, width=50)

        self.article_unit_label = Label(master=self.frame, text="UNIT", font=FONT3, fg=FG, bg=BACKGROUND_COLOR)

        self.unit_entry = Entry(master=self.frame, width=50)

        self.article_qty_label = Label(master=self.frame, text="QUANTITY", font=FONT3, fg=FG, bg=BACKGROUND_COLOR)

        self.qty_entry = Entry(master=self.frame, width=50)

        self.current_label = Label(master=self.frame, text="Current Qty: ", font=FONT3, fg="red", bg=BACKGROUND_COLOR)

        self.current_qlabel = Label(master=self.frame, text="we", font=FONT3, fg="red", bg=BACKGROUND_COLOR)

        self.current_qty_entry = Entry(master=self.frame, width=60)

        self.exit_qty_label = Label(master=self.frame, text="EXIT QTY", font=FONT3, fg=FG, bg=BACKGROUND_COLOR)

        self.exit_qty_entry = Entry(master=self.frame, width=60)

        self.cancel_btn = customtkinter.CTkButton(master=self.frame, text="Cancel transaction",  font=FONT3, width=26)

        self.validate_btn= customtkinter.CTkButton(master=self.frame, text="Confirm", font=FONT1, width=20)
