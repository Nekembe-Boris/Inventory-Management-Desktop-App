"""
Contains functions and Classes that are repeatedly used by all the other modules
"""

from tkinter import Frame, Listbox, Label, END
import customtkinter
import pandas


FG = "white"
BACKGROUND_COLOR = "#212121"
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


def get_details(listbox, path):
    """
    :param listbox - Listbox to get Article metadata
    :param path - file path to load data

    Gets the Article, Article ID, Unit and Quantity of the selected article and returns them.
    """

    stock_data = pandas.read_csv(f"{path}/data/Stock_level.csv")
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


def listboxin(*box, path):
    """
    :param *box - listbox to be modified
    :param path - file path to load data

    - This function is responsible for inserting data into the Article and Article ID listbox
    """
    #clears previous items in the listbox
    for bo_x in box:
        clear(bo_x)
    try:
        stock_data = pandas.read_csv(f"{path}/data/Stock_level.csv")
    except FileNotFoundError:
        print("No data")
    else:

        rev_index = len(stock_data.ArticleID.to_list())

        # Line 119 handles a situation where there is just 01 listbox
        if len(box)<2:
            for item in stock_data.Article.to_list():
                box[0].insert(0, item)
        else:
            for item in stock_data.Article.to_list():
                box[0].insert(0, item[:-5])

            for item in stock_data.ArticleID.to_list():
                box[1].insert(0, item)

        style_bg(box, length=rev_index)


def insert_info(*box, path, file):
    """
    :param *box - listbox to be modified
    :param file - File to upload data that will be used by the listboxes
    :param path - file path to load data

    - This function is responsible for inserting data into all Recent Transaction listboxes
    - Runs only once; when a project is selected
    """
    #clears previous items in the listbox
    for bo_x in box:
        clear(bo_x)
    try:

        data = pandas.read_csv(f"{path}/data/{file}.csv")
    except FileNotFoundError:
        print("No data")
    else:

        rev_index = len(data.Date.to_list())

        for item in data.Article.to_list():
            box[0].insert(0, item)

        for item in data.ArticleID.to_list():
            box[1].insert(0, item)

        for item in data.Date.to_list():
            box[2].insert(0, item)

        for item in data.Quantity.to_list():
            box[3].insert(0, item)

        style_bg(box, length=rev_index)


def update(*box, file, path):

    """
    :param *box - listbox to be modified
    :param path - file path to load data
    :param file - File to upload data that will be used by the listboxes
    
    This function is responsible for updating the Recent Transactions listboxes for every new transaction
    """
    try:

        data = pandas.read_csv(f"{path}/data/{file}.csv")
    except FileNotFoundError:
        print("No data")
    else:

        box[0].insert(0, data.Article.to_list()[-1])
        box[1].insert(0, data.ArticleID.to_list()[-1])
        box[2].insert(0,  data.Date.to_list()[-1])
        box[3].insert(0,  data.Quantity.to_list()[-1])

        style_bg(box, length=len(data.Article.to_list()))


def update_input(*box, name:str, old_data:list, path):
    """
    :param *box - listbox to be updated
    :param path - file path to load data
    :param name - name of Article to be inserted
    :param old_data - old Article List obtained from Stock_level before entry
    
    - Updates the Article and ArticleID listboxes across TABS for every new transaction
    - Adds article if it is recorded for the first time
    """

    try:
        stock_data = pandas.read_csv(f"{path}/data/Stock_level.csv")
    except FileNotFoundError:
        print("No data")
    else:


        if name not in old_data:
            box[0].insert(0, stock_data.Article.to_list()[-1][:-5])
            box[1].insert(0, stock_data.ArticleID.to_list()[-1])
            box[2].insert(0, stock_data.Article.to_list()[-1][:-5])
            box[3].insert(0, stock_data.ArticleID.to_list()[-1])

        style_bg(box, length=len(stock_data.Article.to_list()))


class RecentTransactions():
    """
    This class is a blueprint for creating all the Recent transactions listboxes
    """

    def __init__(self, frame:Frame, file):

        self.frame = frame
        self.file_name = file

        self.des_label = Label(master=self.frame, text="", font=FONT2, fg="red", bg=BACKGROUND_COLOR)
        self.des_label.place(x=380, y=10)

        self.article_label= Label(master=self.frame, text="Article", font=FONT3, bg=BACKGROUND_COLOR, fg=FG)
        self.article_label.place(x=155, y=45)

        self.id_label= Label(master=self.frame, text="Article ID", font=FONT3, bg=BACKGROUND_COLOR, fg=FG)
        self.id_label.place(x=470, y=45)

        self.date_label= Label(master=self.frame, text="Date", font=FONT3, bg=BACKGROUND_COLOR, fg=FG)
        self.date_label.place(x=670, y=45)

        self.qty_label= Label(master=self.frame, text="QTY", font=FONT3, bg=BACKGROUND_COLOR, fg=FG)
        self.qty_label.place(x=760, y=45)

        self.article_listbox = list_box(frame=self.frame, x_cor=75, y_cor=70, l_height=40, l_width=50)

        self.ID_listbox = list_box(frame=self.frame, x_cor=380, y_cor=70, l_height=40, l_width=40)

        self.date_listbox = list_box(frame=self.frame, x_cor=625, y_cor=70, l_height=40, l_width=20)

        self.quatity_listbox = list_box(frame=self.frame, x_cor=750, y_cor=70, l_height=40, l_width=10)

        bind_box(self.article_listbox, self.ID_listbox, self.date_listbox, self.quatity_listbox, func=self.mousewheel)
        # insert_info(self.article_listbox, self.ID_listbox, self.date_listbox, self.quatity_listbox, file=self.file_name)

    def mousewheel(self, event):
        """Responsible for binding all listboxes to mousewheel"""
        self.article_listbox.yview_scroll(-2 * int(event.delta / 120), "units")
        self.ID_listbox.yview_scroll(-2 * int(event.delta / 120), "units")
        self.date_listbox.yview_scroll(-2 * int(event.delta / 120), "units")
        self.quatity_listbox.yview_scroll(-2 * int(event.delta / 120), "units")



class DataInput():

    """
    This class is a blueprint for the widgets, labels and listboxes for entries or exits
    """

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

        self.article_entry_entry = customtkinter.CTkEntry(master=self.frame, fg_color="white", text_color="black", width=250)

        self.id_label = Label(master=self.frame, text="ARTICLE ID", font=FONT3, fg=FG, bg=BACKGROUND_COLOR)

        self.id_entry = customtkinter.CTkEntry(master=self.frame, fg_color="white", text_color="black", width=250)

        self.article_unit_label = Label(master=self.frame, text="UNIT", font=FONT3, fg=FG, bg=BACKGROUND_COLOR)

        self.unit_entry = customtkinter.CTkEntry(master=self.frame, fg_color="white", text_color="black", width=250)

        self.article_qty_label = Label(master=self.frame, text="QUANTITY", font=FONT3, fg=FG, bg=BACKGROUND_COLOR)

        self.qty_entry = customtkinter.CTkEntry(master=self.frame, fg_color="white", text_color="black", placeholder_text="Insert quantity", width=250)

        self.current_label = Label(master=self.frame, text="Current Qty: ", font=FONT3, fg="red", bg=BACKGROUND_COLOR)

        self.current_qlabel = Label(master=self.frame, text="we", font=FONT3, fg="red", bg=BACKGROUND_COLOR)

        self.current_qty_entry = customtkinter.CTkEntry(master=self.frame, text_color="black", fg_color=FG, width=60)

        self.exit_qty_label = Label(master=self.frame, text="EXIT QTY", font=FONT3, fg=FG, bg=BACKGROUND_COLOR)

        self.exit_qty_entry = customtkinter.CTkEntry(master=self.frame, width=60, text_color="black", fg_color=FG, placeholder_text="Insert quantity")

        self.cancel_btn = customtkinter.CTkButton(master=self.frame, text="Cancel transaction",  font=FONT3, width=180)

        self.validate_btn= customtkinter.CTkButton(master=self.frame, text="Confirm", font=FONT1, width=180)
