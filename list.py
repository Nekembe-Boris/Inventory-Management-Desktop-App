import random
import pandas
import datetime

sheet = "Entries"
fil = "ArticleID"
key = "Nido Choco[Mil]"
current_time = datetime.datetime.now()
date = current_time.strftime("%d-%b-%Y")
exits = [20, 30, 25, 15, 35]


try:
    st_data = pandas.read_csv(f"./new/{sheet}.csv")
    data = pandas.read_csv("./new/Stock_level.csv")
except FileNotFoundError:
    pass
else:
    stk_df = pandas.DataFrame(data)
    entries_article_list = data.Article.to_list()
    entries_article_id_list = data.ArticleID.to_list()
    entries_qty_list = data.Quantity.to_list()
    entries_unit_list = data.Unit.to_list()

    # for i in range(len(entries_article_list)):
    for i, info in enumerate(entries_qty_list, 1):

        art_id = entries_article_id_list[i]
        art_name = entries_article_list[i]
        art_unit = entries_unit_list[i]
        art_qty = entries_qty_list[i]
        stock_name = entries_article_list[i]
        exit_qty = random.choice(exits)

        qty_left = art_qty - exit_qty

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
            pandas.read_csv("./new/Exit.csv")
        except FileNotFoundError:
            exit_df.to_csv("./new/Exit.csv", mode='a', index=False)
        else:
            exit_df.to_csv("./new/Exit.csv", mode='a', index=False, header=False)

        finally:
            gl_df.to_csv("./new/General_ledger.csv", mode='a', index=False, header=False)

            for (i, row) in stk_df.iterrows():
                if row.Article == stock_name:
                    stk_df = stk_df.drop(stk_df.index[i], axis=0)
                    stk_df.to_csv("./new/Stock_level.csv", index=False)
                    new_stk_df.to_csv("./new/Stock_level.csv", mode='a', index=False, header=False)
