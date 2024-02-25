"""
- This module is tasked with creating a new project or open an existing project
- It also automatically changes the working directory based on the created or selected project
"""

from tkinter import Frame, messagebox, StringVar, Label
import os
import shutil
import datetime
from tktooltip import ToolTip
import customtkinter
from modules.functions import forget, listboxin, insert_info, clear
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
            stock:StockLook,
            title

        ):

        self.frame = frame
        self.project_var = StringVar
        self.entry_tab = entry_tab
        self.recent_entries = recent_entries
        self.exit_tab = exit_tab
        self.recent_exit = recent_exit
        self.filter_sec = filter_sec
        self.stock_tab = stock
        self.current_project = title

        self.project_list = os.listdir("./projects")
        self.project_folders = []
        self.time = datetime.datetime.today()

        self.descrip_label = Label(master=self.frame, text="[NEW PROJECT]", font=("Century Gothic", 25, "bold"), background="#212121", foreground="white")
        self.descrip_label.place(x=300, y=250)

        self.create_project_btn = customtkinter.CTkButton(master=self.frame, text="Create New", width=200, height=80, command=self.new_project)
        self.create_project_btn.place(x=240, y=300)

        self.descrip_cc_label = Label(master=self.frame, text="Open Existing Project", font=("Century Gothic", 20, "bold"), background="#212121", foreground="white")
        self.descrip_cc_label.place(x=880, y=250)

        self.project_box = customtkinter.CTkComboBox(master=self.frame, width=250, variable=self.project_var, values=self.project_list, command=self.select_project)
        self.project_box.set("Select Project")
        self.project_box.place(x=700, y=300)


        self.project_open_btn = customtkinter.CTkButton(master=self.frame, text="Open", width=150, command=self.open)
        self.project_open_btn.place(x=900, y=410)

        self.project_year = customtkinter.CTkComboBox(master=self.frame, width=250, variable=self.project_var, values=self.project_folders)
        self.project_year.set("Year")
        self.project_year.place(x=700, y=380)
        

        self.new_yr_btn = customtkinter.CTkButton(master=self.frame, text="New Year", width=150, command=self.new_year)
        self.new_yr_btn.place(x=900, y=440)

        ToolTip(self.create_project_btn, msg="Create a directory for a new:\n- PROJECT\n- STORE\n- WAREHOUSE")
        ToolTip(self.new_yr_btn, msg=f"Create a new directory for recordings for {self.time.year}\nif it is a new year")


    def new_project(self):
        """
        - Creates a new project and automatically changes the directory path
        """

        new_proj_name = customtkinter.CTkInputDialog(text="Insert project name:", title="NEW PROJECT")
        project_name = str(new_proj_name.get_input()).upper()
        current_yr = str(self.time.year)
        all_projects = os.listdir("./projects")

        # checks if chosen project name already exists or the validity of the name
        if project_name in all_projects:
            messagebox.showerror(
                title="Error",
                message="Project name already exists"
            )
        elif project_name == "NONE":
            pass
        else :
            os.makedirs(f"./projects/{project_name}/{current_yr}/reports")
            os.mkdir(f"./projects/{project_name}/{current_yr}/data")

            self.entry_tab.file_path = self.exit_tab.file_path = self.filter_sec.file_path = self.stock_tab.file_path = f"./projects/{project_name}/{current_yr}"

            self.current_project.title(f"XERXES - {project_name} [{current_yr}]")

            self.project_list.insert(-1, project_name)
            
            self.project_box.configure(values=self.project_list)


    def select_project (self, event):
        """
        Fills the project year ComboBox with the all the available projects
        """

        if  (selected_project := event) not in self.project_list:

            messagebox.showinfo(
                title="Empty Field",
                message="Select desired project to proceed"
            )
        else:
            self.project_folders = os.listdir(f"./projects/{selected_project}")

            self.project_year.configure(values=self.project_folders)

    def open(self):
        """
        Opens the Year of the selected project when the "Open" button is clicked
        """

        if (selected_project := self.project_box.get()) not in self.project_list or (selected_year := self.project_year.get()) not in self.project_folders:

            messagebox.showinfo(
                title="Error",
                message="Verify Project or Year"
            )
        else:

            # changes the working directory
            self.entry_tab.file_path = self.exit_tab.file_path = self.filter_sec.file_path = self.stock_tab.file_path = f"./projects/{selected_project}/{selected_year}"

            self.current_project.title(f"XERXES - {selected_project} [{selected_year}]")

            listboxin(self.entry_tab.article_listbox,  self.entry_tab.id_listbox, path=self.entry_tab.file_path)

            insert_info(self.recent_entries.article_listbox, self.recent_entries.ID_listbox, self.recent_entries.date_listbox, self.recent_entries.quatity_listbox, self.recent_entries.time_listbox, file=self.recent_entries.file_name, path=self.entry_tab.file_path)
            
            #updating the exit tab
            listboxin(self.exit_tab.article_listbox, self.exit_tab.id_listbox, path=self.exit_tab.file_path)

            insert_info(self.recent_exit.article_listbox, self.recent_exit.ID_listbox, self.recent_exit.date_listbox, self.recent_exit.quatity_listbox, self.recent_exit.time_listbox, file=self.recent_exit.file_name, path=self.exit_tab.file_path)

            # updating the listbox on the advanced_tab
            listboxin(self.stock_tab.ch_listbox, path=self.stock_tab.file_path)

            self.project_year.set("Year")
            self.project_box.set("Select Project")


    def new_year(self):
        """
        Creates a new directory for a new year [For the selected Project]
        """
        current_yr = str(self.time.year)
        previous_yr = self.project_folders[-1]

        if (selected_project := self.project_box.get()) not in self.project_list:

            messagebox.showinfo(
                title="Error",
                message="Select desired project to proceed"
            )
        elif current_yr in self.project_folders:
            messagebox.showinfo(
                title="Error",
                message="Year already exits"
            )
        else:
            os.makedirs(f"./projects/{selected_project}/{current_yr}/reports")
            os.mkdir(f"./projects/{selected_project}/{current_yr}/data")

            # Copy stock data from previous year to the next year
            shutil.copy2(f"./projects/{selected_project}/{previous_yr}/data/Stock_level.csv", f"./projects/{selected_project}/{current_yr}/data")
            
            self.project_year.set("Year")
            self.project_box.set("Select Project")

            # changes the working directory
            self.entry_tab.file_path = self.exit_tab.file_path = self.filter_sec.file_path = self.stock_tab.file_path = f"./projects/{selected_project}/{current_yr}"

            self.current_project.title(f"XERXES - {selected_project} [{current_yr}]")

            forget(self.project_open_btn, self.new_yr_btn)

            # clearing all entry boxes on ENTRY & EXIT Tabs
            clear(self.entry_tab.article_entry_entry, self.entry_tab.id_entry, self.entry_tab.unit_entry, self.entry_tab.qty_entry)
            clear(self.exit_tab.article_entry_entry, self.exit_tab.id_entry, self.exit_tab.unit_entry, self.exit_tab.qty_entry, self.exit_tab.current_qty_entry)

            listboxin(self.exit_tab.article_listbox, self.exit_tab.id_listbox, path=self.exit_tab.file_path)
            listboxin(self.entry_tab.article_listbox,  self.entry_tab.id_listbox, path=self.entry_tab.file_path)
            listboxin(self.stock_tab.ch_listbox, path=self.stock_tab.file_path)
