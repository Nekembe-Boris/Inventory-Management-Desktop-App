"""
- This module creates a new project or opens an existing project 
- It also automatically changes the working directory to the created or selected project
"""

from tkinter import Frame, messagebox, StringVar, Label
import os
import datetime
from tktooltip import ToolTip
import customtkinter
from modules.functions import forget, listboxin, insert_info
from modules.entry import Input, RecentEntries
from modules.exit import Exit, RecentExits
from modules.filter import Filter
from modules.stk_check import StockLook


class Project:

    """
    This class is responsible for all the functionalities of the HOME TAB
    """

    def __init__(
            self,
            frame:Frame,
            entry_tab:Input,
            recent_entries:RecentEntries,
            exit_tab:Exit,
            recent_exit : RecentExits,
            filter_sec:Filter,
            stock:StockLook

        ):

        self.frame = frame
        self.project_var = StringVar
        self.entry_tab = entry_tab
        self.recent_entries = recent_entries
        self.exit_tab = exit_tab
        self.recent_exit = recent_exit
        self.filter_sec = filter_sec
        self.stock_tab = stock

        self.project_list = os.listdir("./projects")
        self.project_folders = []

        self.descrip_label = Label(master=self.frame, text="[NEW PROJECT]", font=("Century Gothic", 25, "bold"), background="#212121", foreground="white")
        self.descrip_label.place(x=300, y=250)

        self.create_project_btn = customtkinter.CTkButton(master=self.frame, text="Create New", width=200, height=80, command=self.new_project)
        self.create_project_btn.place(x=240, y=300)

        ToolTip(self.create_project_btn, msg="Create a directory for a new:\n- PROJECT\n- STORE\n- WAREHOUSE")

        self.descrip_cc_label = Label(master=self.frame, text="Open Existing Project", font=("Century Gothic", 20, "bold"), background="#212121", foreground="white")
        self.descrip_cc_label.place(x=880, y=250)

        self.project_box = customtkinter.CTkComboBox(master=self.frame, width=250, variable=self.project_var, values=self.project_list)
        self.project_box.set("Select Project")
        self.project_box.place(x=700, y=300)

        self.pro_files_btn = customtkinter.CTkButton(master=self.frame, text="View Folders", width=150, command=self.select_project)
        self.pro_files_btn.place(x=900, y=340)

        self.project_open_btn = customtkinter.CTkButton(master=self.frame, text="Open", width=150)

        self.project_year = customtkinter.CTkComboBox(master=self.frame, width=250, variable=self.project_var, values=self.project_folders)
        self.project_year.set("Year")


    def new_project(self):
        """
        - Creates a new project and automatically changes the directory path
        """

        new_proj_name = customtkinter.CTkInputDialog(text="Insert project name:", title="NEW PROJECT")
        project_name = str(new_proj_name.get_input())
        year = str(datetime.datetime.today().year)
        all_projects = os.listdir("./projects")

        # checks if chosen project name already exists or the validity of the name
        if project_name in all_projects or not project_name or project_name is None:
            messagebox.showerror(
                title="Error",
                message="Project name already exists\nOR\nInvalid Project name"
            )
        else :
            os.makedirs(f"./projects/{project_name}/{year}/reports")
            os.mkdir(f"./projects/{project_name}/{year}/data")
            
            self.entry_tab.file_path = f"./projects/{project_name}/{year}"

            self.exit_tab.file_path  = f"./projects/{project_name}/{year}"

            self.filter_sec.file_path = f"./projects/{project_name}/{year}"

            self.stock_tab.file_path = f"./projects/{project_name}/{year}"


    def select_project (self):
        """
        Fills the project year ComboBox with the all the available projects
        """

        if (selected_project := self.project_box.get()) not in self.project_list:

            messagebox.showinfo(
                title="Empty Field",
                message="Select desired project to proceed"
            )
        else:
            self.project_folders = os.listdir(f"./projects/{selected_project}")

            self.project_year.configure(values=self.project_folders)
            self.project_year.place(x=700, y=380)

            forget(self.pro_files_btn)

            self.project_open_btn.configure(command=self.open)
            self.project_open_btn.place(x=900, y=340)


    def open(self):
        """
        Opens the Year of the selected project when the "Open" button is clicked
        """

        if (selected_project := self.project_box.get()) not in self.project_list or (selected_year := self.project_year.get()) not in self.project_folders:

            messagebox.showinfo(
                title="Error",
                message="Verify parameters"
            )
        else:
            self.entry_tab.file_path = f"./projects/{selected_project}/{selected_year}"

            self.exit_tab.file_path  = f"./projects/{selected_project}/{selected_year}"

            self.filter_sec.file_path = f"./projects/{selected_project}/{selected_year}"

            self.stock_tab.file_path = f"./projects/{selected_project}/{selected_year}"



            # updating the entry tab
            listboxin(self.entry_tab.article_listbox,  self.entry_tab.id_listbox, path=self.entry_tab.file_path)

            insert_info(self.recent_entries.article_listbox, self.recent_entries.ID_listbox, self.recent_entries.date_listbox, self.recent_entries.quatity_listbox, file=self.recent_entries.file_name, path=self.entry_tab.file_path)
            
            #updating the exit tab
            listboxin(self.exit_tab.article_listbox, self.exit_tab.id_listbox, path=self.exit_tab.file_path)

            insert_info(self.recent_exit.article_listbox, self.recent_exit.ID_listbox, self.recent_exit.date_listbox, self.recent_exit.quatity_listbox, file=self.recent_exit.file_name, path=self.exit_tab.file_path)

            # updating the listbox on the advanced_tab
            listboxin(self.stock_tab.ch_listbox, path=self.stock_tab.file_path)