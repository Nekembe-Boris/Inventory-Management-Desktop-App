"""
Module tasked with Filtering on the ADVANCED TAB
- It will filter the data based on preferences.
- Filtered data can be transformed to an MS Excel sheet
"""

import os
from tkinter import StringVar, Frame
from tkinter import messagebox
import customtkinter
import pandas
from modules.functions import clear, forget, insert_info, RecentTransactions


FG = "white"
BACKGROUND_COLOR = "#212121"
FONT1 = ("Century Gothic", 10, "bold")
FONT3 = ("Century Gothic", 8, "bold")
records = ["Entries", "Exit", "General_ledger"]
ad_filter = ["Article", "ArticleID", "Date"]


class Filter(RecentTransactions):
    """
    Filters data and displays filtered data in listboxes
    """
    def __init__(self, frame:Frame, path):
        self.frame = frame
        self.file_path = path
        self.file_name = "filtered"

        super().__init__(self.frame, file=self.file_name)

        self.des_label.config(text="FILTER RECORDS")
        self.des_label.place(x=350, y=30)


        self.article_label.place(x=240, y=250)
        self.id_label.place(x=480, y=250)
        self.date_label.place(x=700, y=250)
        self.qty_label.place(x=790, y=250)
        self.time_label.place(x=865, y=250)

        self.article_listbox.place(x=100, y=280)
        self.ID_listbox.place(x=405, y=280)
        self.date_listbox.place(x=650, y=280)
        self.quatity_listbox.place(x=775, y=280)
        self.time_listbox.place(x=840, y=280)


        self.rec_var = StringVar()
        self.filter_var = StringVar()

        self.record_type = customtkinter.CTkComboBox(master=self.frame, width=250, variable=self.rec_var, values=records, font=FONT3)
        self.record_type.set("Select Record")
        self.record_type.place(x=50, y=70)

        self.filter_record_param = customtkinter.CTkComboBox(master=self.frame, width=250, variable=self.filter_var, values=ad_filter, font=FONT3)
        self.filter_record_param.set("Filter By")
        self.filter_record_param.place(x=50, y=130)

        self.select_btn = customtkinter.CTkButton(master=self.frame, text="Apply", width=80, font=FONT3, command=self.get_info)
        self.select_btn.place(x=280, y=100)

        self.filter_btn = customtkinter.CTkButton(master=self.frame, text="Filter", width=80, font=FONT3, command=self.filter_data)

        self.print_btn = customtkinter.CTkButton(master=self.frame, text="To Excel", width=80, font=FONT3, command=self.print_data)

        self.cancel_filter_btn = customtkinter.CTkButton(master=self.frame, text="Cancel", width=80, font=FONT3, hover_color="red", command=self.reset_filter)

        self.fil_details_box = customtkinter.CTkComboBox(master=self.frame, width=250, font=FONT3)


    def get_info(self):
        """Function fills the Select combobox based on the Record and Filter param selected"""

        if (sheet := self.record_type.get()) not in records or (filter_param := self.filter_record_param.get()) not in ad_filter:
            messagebox.showinfo(
                title="Error",
                message="Verify filter inputs"
            )
        else:

            self.fil_details_box.set(f"Select {filter_param}:")
            self.fil_details_box.place(x=400, y=70)
            self.filter_btn.place(x=565, y=100)
            self.cancel_filter_btn.place(x=565, y=130)

            try:
                data = pandas.read_csv(f"{self.file_path}/data/{sheet}.csv")
            except FileNotFoundError:
                messagebox.showinfo(
                title="Error",
                message=f"{sheet} data does not exist yet"
                )
            else:
                # filtering the rrecord type by the filter param
                new_box_data = data.loc[:, f"{filter_param}"].to_list()
                fil_box_data = []
                for item in new_box_data:
                    if item not in fil_box_data:
                        fil_box_data.append(item)

                self.fil_details_box.configure(values=fil_box_data)


    def filter_data(self):
        """
        - Gets filtered data based on the inputs and displayes these data in the listboxes
        """
        clear(self.article_listbox, self.ID_listbox, self.date_listbox, self.time_listbox)

        sheet = self.record_type.get()
        filter_param = self.filter_record_param.get()
        filter_key = self.fil_details_box.get()

        if not sheet or not filter_param or not filter_key:
            messagebox.showinfo(
                title="Error",
                message="Check for empty Fields"
                )
        else:
            data = pandas.read_csv(f"{self.file_path}/data/{sheet}.csv")

            filtered_df = data.loc[data[f'{filter_param}'] == filter_key]

            if filtered_df.empty:
                messagebox.showinfo(
                    title="Error",
                    message="Data does not exist\nVerify filter parameters"
                    )
            else:
                filtered_df.to_csv(f"{self.file_path}/data/filtered.csv", index=False)

                insert_info(self.article_listbox, self.ID_listbox, self.date_listbox, self.quatity_listbox, self.time_listbox, path=self.file_path, file="filtered")

                forget(self.fil_details_box, self.filter_btn, self.cancel_filter_btn)
                self.record_type.set("Select Record")
                self.filter_record_param.set("Filter By")

                self.print_btn.place(x=700, y=170)

                
    def reset_filter(self):
        """
        Cancels the ongoing filter
        """
        forget(self.fil_details_box, self.filter_btn, self.cancel_filter_btn)

    def print_data(self):
        """
        Generates Excel sheet of the filtered data
        """
        data = pandas.read_csv(f"{self.file_path}/data/filtered.csv")
        data.to_excel(f"{self.file_path}/reports/Filtered_data.xlsx", index=False)
        os.system(f'start "excel" "{self.file_path}/reports/Filtered_data.xlsx"')

        forget(self.print_btn)