"""This module generates the GUI Interface of this software"""
from tkinter import Tk, Frame
from tkinter import ttk
from entry import Input, RecentEntries
from exit import Exit, RecentExits
from stk_check import StockLook
from filter import Filter


BACKGROUND_COLOR = "#FFFDD1"
BACKGROUND_COLOR2 = "#D3D3D3"
ATL_COLOR = "#949494"

root = Tk()
root.title("Inventory Manager 3.0")
root.geometry("1280x820")
root.config(bg=BACKGROUND_COLOR)

main_tab = ttk.Notebook(root)
main_tab.pack(fill="both")




##########-----EXIT TAB-----###############
#main frame for the EXIT Tab
exit_frame = Frame(master=main_tab, height=820, width=1280, bg=BACKGROUND_COLOR)
exit_frame.pack(fill="both", expand=1)

#frame for the recent exit section of the tab.
exit_info_frame = Frame(master=exit_frame, height=820, width=720, bg=BACKGROUND_COLOR)
exit_info_frame.grid(column=1, row=0)
exit_info_sec = RecentExits(frame=exit_info_frame)

#frame for the withdraw section of the Tab
output_frame = Frame(master=exit_frame, height=820, width=550, bg=BACKGROUND_COLOR)
output_frame.grid(column=0, row=0)
exit_sec = Exit(frame=output_frame, updates=exit_info_sec)

#making frame screen responsive
EX_COLUMNS = 2
for i in range(EX_COLUMNS):
    exit_frame.grid_columnconfigure(i,  weight = 1)




###########-------ENTRY TAB-----################
#main frame for the ENTRY Tab
entry_frame = Frame(master=main_tab, height=820, width=1280, bg=BACKGROUND_COLOR)
entry_frame.pack(fill="both", expand=1)

#frame for the recent entries section of the tab.
info_frame = Frame(master=entry_frame, height=820, width=720, bg=BACKGROUND_COLOR)
info_frame.grid(column=1, row=0)
info_sec = RecentEntries(frame=info_frame)

#frame for the input section of the Entry Tab
input_frame = Frame(master=entry_frame, height=820, width=550, bg=BACKGROUND_COLOR)
input_frame.grid(column=0, row=0)
entry_sec = Input(frame=input_frame, updates=info_sec, exit_up=exit_sec)

#making frame screen responsive
EN_COLUMNS = 2
for i in range(EN_COLUMNS):
    entry_frame.grid_columnconfigure(i,  weight = 1)




##########-------INSIGHT TAB-------##############
#main frame for the ENTRY Tab
advanced_frame = Frame(master=main_tab, height=820, width=1280, bg=BACKGROUND_COLOR2)
advanced_frame.pack(fill="both", expand=1)

#frame for the verify and reports section of the tab.
check_report_frame = Frame(master=advanced_frame, height=820, width=500, bg=ATL_COLOR)
check_report_frame.grid(column=0, row=0)
stock_check = StockLook(frame=check_report_frame, entry_update=entry_sec, exit_update=exit_sec)

#frame for the filter section of the tab.
filter_frame = Frame(master=advanced_frame, height=820, width=780, bg=ATL_COLOR)
filter_frame.grid(column=1, row=0)
filter_sec = Filter(frame=filter_frame)

IN_COLUMNS = 2
for i in range(IN_COLUMNS):
    advanced_frame.grid_columnconfigure(i,  weight = 1)


################################################
main_tab.add(entry_frame, text="     ENTRY     ")
main_tab.add(exit_frame, text="     EXIT     ")
main_tab.add(advanced_frame, text="     ADVANCED     ")

root.mainloop()
