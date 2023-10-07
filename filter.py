"""Module tasked with Filtering on the ADVANCED TAB"""
from tkinter import Label, StringVar, Button, Frame
from tkinter import ttk, messagebox
import pandas
from functions import  list_box, bind_box, clear, style_bg, forget


BACKGROUND_COLOR = "#949494"
FONT1 = ("Century Gothic", 10, "bold")
FONT3 = ("Century Gothic", 8, "bold")
records = ["Entries", "Exit", "General_ledger"]
ad_filter = ["Article", "ArticleID", "Date"]


class Filter():
    """
    Filters data and displays filtered data in listboxes
    """
    def __init__(self, frame:Frame):
        self.frame = frame

        self.rec_var = StringVar()
        self.filter_var = StringVar()

        self.rec_select = Label(master=self.frame, text="SELECT RECORD", font=FONT1,  bg=BACKGROUND_COLOR)
        self.rec_select.place(x=50, y=50)

        self.rec_typebox = ttk.Combobox(master=self.frame, width=25, textvariable=self.rec_var, values=records, font=FONT3)
        self.rec_typebox.place(x=50, y=70)

        self.ad_select = Label(master=self.frame, text="Filter By:", font=FONT1,  bg=BACKGROUND_COLOR)
        self.ad_select.place(x=50, y=100)

        self.ad_typebox = ttk.Combobox(master=self.frame, width=25, textvariable=self.filter_var, values=ad_filter, font=FONT3)
        self.ad_typebox.place(x=50, y=120)

        self.select_btn = Button(master=self.frame, text="Apply", font=FONT3, command=self.get_info)
        self.select_btn.place(x=250, y=90)

        self.filter_btn = Button(master=self.frame, text="Filter", font=FONT3, bg="#D7E5F0", command=self.filter_data)

        self.fil_details_label= Label(master=self.frame, text="Select:", font=FONT1,  bg=BACKGROUND_COLOR)

        self.fil_details_box = ttk.Combobox(master=self.frame, width=25, font=FONT3)

        self.article_label= Label(master=self.frame, text="Article", font=FONT3, bg=BACKGROUND_COLOR)
        self.article_label.place(x=155, y=180)

        self.id_label= Label(master=self.frame, text="Article ID", font=FONT3, bg=BACKGROUND_COLOR)
        self.id_label.place(x=355, y=180)

        self.date_label= Label(master=self.frame, text="Date", font=FONT3, bg=BACKGROUND_COLOR)
        self.date_label.place(x=530, y=180)

        self.qty_label= Label(master=self.frame, text="QTY", font=FONT3, bg=BACKGROUND_COLOR)
        self.qty_label.place(x=640, y=180)

        self.fil_art_listbox = list_box(frame=self.frame, x_cor=80, y_cor=200, l_height=30, l_width=35)

        self.fil_id_listbox = list_box(frame=self.frame, x_cor=300, y_cor=200, l_height=30, l_width=30)

        self.fil_date_listbox = list_box(frame=self.frame, x_cor=490, y_cor=200, l_height=30, l_width=20)

        self.fil_quatity_listbox = list_box(frame=self.frame, x_cor=620, y_cor=200, l_height=30, l_width=10)

        bind_box(self.fil_art_listbox, self.fil_id_listbox, self.fil_date_listbox, self.fil_quatity_listbox, func=self.mousewheel)

    def mousewheel(self, event):
        """Responsible for binding all listboxes to mousewheel"""
        self.fil_art_listbox.yview_scroll(-2 * int(event.delta / 120), "units")
        self.fil_id_listbox.yview_scroll(-2 * int(event.delta / 120), "units")
        self.fil_date_listbox.yview_scroll(-2 * int(event.delta / 120), "units")
        self.fil_quatity_listbox.yview_scroll(-2 * int(event.delta / 120), "units")


    def get_info(self):
        """Function fills the Select combobox based on the Record and Filter param selected"""
        sheet = self.rec_typebox.get()
        filter_param = self.ad_typebox.get()
        clear(self.fil_details_box)

        if not sheet or not filter_param:
            messagebox.showinfo(
                title="Error",
                message="Select Record or Filter By field empty!"
            )
        else:
            self.fil_details_label.config(text=f"Select {filter_param}:")
            self.fil_details_label.place(x=300, y=70)
            self.fil_details_box.place(x=300, y=90)
            self.filter_btn.place(x=510, y=90)

            try:
                data = pandas.read_csv(f"./data/{sheet}.csv")
            except FileNotFoundError:
                messagebox.showinfo(
                title="Error",
                message=f"{sheet} data does not exist yet"
                )
            else:

                new_box_data = data.loc[:, f"{filter_param}"].to_list()
                fil_box_data = []
                for item in new_box_data:
                    if item not in fil_box_data:
                        fil_box_data.append(item)

                self.fil_details_box.config(values=fil_box_data)


    def filter_data(self):
        """
        - Gets filtered data based on the inputs and displayes these data in the listboxes
        """
        clear(self.fil_art_listbox, self.fil_id_listbox, self.fil_date_listbox, self.fil_quatity_listbox)

        sheet = self.rec_typebox.get()
        filter_param = self.ad_typebox.get()
        filter_key = self.fil_details_box.get()

        if not sheet or not filter_param or not filter_key:
            messagebox.showinfo(
                title="Error",
                message="Check for empty Fields"
                )
        else:
            data = pandas.read_csv(f"./data/{sheet}.csv")

            filtered_df = data.loc[data[f'{filter_param}'] == filter_key]

            if filtered_df.empty:
                messagebox.showinfo(
                    title="Error",
                    message="Data does not exist\nVerify filter parameters"
                    )
            else:
                filtered_df.to_csv("./data/filtered.csv", index=False)

                filtered_data = pandas.read_csv("./data/filtered.csv")
                entries_article_list = filtered_data.Article.to_list()
                entries_article_id_list = filtered_data.ArticleID.to_list()
                entries_date_list = filtered_data.Date.to_list()
                entries_qty_list = filtered_data.Quantity.to_list()

                rev_index = len(entries_date_list)

                for item in entries_article_list:
                    self.fil_art_listbox.insert(0, item)

                for item in entries_article_id_list:
                    self.fil_id_listbox.insert(0, item)

                for item in entries_date_list:
                    self.fil_date_listbox.insert(0, item)

                for item in entries_qty_list:
                    self.fil_quatity_listbox.insert(0, item)


                box_list = (self.fil_art_listbox, self.fil_id_listbox, self.fil_date_listbox, self.fil_quatity_listbox)

                style_bg(box=box_list, length=rev_index)

                forget(self.fil_details_label, self.fil_details_box, self.filter_btn)
                clear(self.fil_details_box, self.ad_typebox, self.rec_typebox)
