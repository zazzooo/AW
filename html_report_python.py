import dominate
from dominate.tags import *
import pandas as pd

table_headers = ['index','value']

def create_page(df_stats):
    doc = dominate.document(title = 'Tabble')

    with doc.head:
        link(rel = 'stylesheet', href = 'style.css')
        style("""table, th, td {border:1px solid black;) """)
    with doc:
        with div(cls='container', style='display:inline-block;vertical-align:top;margin-top: 20px;'):
            with table(id = 'stats', cls = 'table of statistics', style="width:100%"):
                caption(h3('Stastic'))
                with thead():
                    with tr():
                        for table_head in table_headers:
                            th(table_head)
                with tbody():
                    for i in range(len(df_stats)):
                        with tr():
                            td(df_stats.iloc[i]['index'])
                            td(round(df_stats.iloc[i]['value'],4))

        with div(cls='container', style='display:inline-block;margin-top: 50px;'):
            img(src = "./img/table_montly_returns.png", alt = 'Distribution plot' ,width="550", height="330")

        with div(cls='container', style='display:inline-block;margin-top: 50px;'):
            img(src = "./img/distribution_returns.png", alt = 'Distribution plot' ,width="420", height="288")

        with div(cls='container', style='display:inline-block;vertical-align:top;margin-top: 50px;margin-left: 50px;'):
            img(src = "./img/drawdowns_period.png", alt = 'Distribution plot', width="576", height="288")

        with div(cls='container', style='display:inline-block;margin-top: 50px;'):
            img(src = "./img/under_water_plot.png", alt = 'Distribution plot' ,width="576", height="288")



    print(doc)

df = pd.read_csv('./data/statistics_all_weather.csv')
create_page(df)


#To create the html file call from the shell (in the right directory) $pyhton3 html_with_python.py >> report.html  This command will create a report.html file in the same directory with the report of the strategy