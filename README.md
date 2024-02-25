# XERXES - Inventory Management App

This GUI inventory management system can be used by any individual to manage stock and it is 'Database-less' and was built solely with the Python **Tkinter GUI Toolkit**, **CustomTkinter Toolkit**, **Pandas Library** and CSV files. It can also be used in filtering your data based on certain preferences chosen.  



## Interface

1. HOME Tab
   - Create a new directory for a new Project / Warehouse / Store by clicking the **Create New** button
     ![create_project_img](https://github.com/Nekembe-Boris/user-content/blob/main/Screenshot%202024-02-25%20150248.png)

   - Open an already project by selecting from the **Select Project** entry box and also selecting the **Year** to succesfully open this project
     ![open_project_img](https://github.com/Nekembe-Boris/user-content/blob/main/Screenshot%202024-02-25%20152247.png)
     ![open_img](https://github.com/Nekembe-Boris/user-content/blob/main/Screenshot%202024-02-25%20152314.png)

   - For an existing Project, click the **New Year** button record transactions for the current year
   - The **Title Bar** will reflect the name of the opened project
     ![title_img](https://github.com/Nekembe-Boris/user-content/blob/main/Screenshot%202024-02-25%20154225.png)

2. ENTRY & EXIT Tab
   - For **Entry Tab** select article from **ARTICLE** box if article already exists or Enter new article data in corresponding fields
   - For **Exit Tab** select article from **ARTICLE** box
   - See recent Entries / Exits right side of the respective Tab
     ![entry_img](https://github.com/Nekembe-Boris/user-content/blob/main/Screenshot%202024-02-25%20155954.png)
     ![exit_img](https://github.com/Nekembe-Boris/user-content/blob/main/Screenshot%202024-02-25%20160657.png)

3. ADVANCED Tab
   - Easily verify the quantity of any article by selecting the article
   - Print any record from the options available
   - Filter record data based on the available preferences
     ![advanced_tab](https://github.com/Nekembe-Boris/user-content/blob/main/Screenshot%202024-02-25%20170744.png)

## Project Setup

This project requiresPython >=3.7. To get started, follow the steps below:

1. **Clone the Repository:** Begin by cloning this repository to your local machine using the following command:  
   ```git clone https://github.com/Nekembe-Boris/XERXES.git```


2. **Install Requirements:**  
```
pip3 install -r requirements.txt
```

3. Run **main.py**

### Consideration while running the application
   - This application should not be opened on a screen larger than 19 inches as it will change the UI. CustomTkinter (a modern and customizable python UI-library based on Tkinter) is yet to be fully able to integrate with Tkinter
