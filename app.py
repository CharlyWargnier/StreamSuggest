import base64

import suggests
import json

import streamlit as st
import csv
import json
import pandas as pd
import time

from pyecharts import options as opts
from pyecharts.charts import Tree
from streamlit_echarts import st_echarts


#region Top area ############################################################

c30, c31, c32 = st.beta_columns(3)

with c30:
  #st.image('streamEASmaller2.jpg', width = 275 )
  #st.image('Images\logo.png', width = 275 )
  st.image('StreamSuggestLogo.png', width = 275 )

with c32:
  #st.image('streamEASmaller2.jpg', width = 275 )
  #st.markdown("---")
  st.header('')
  st.header('')
  st.markdown('###### Made in [![this is an image link](https://i.imgur.com/iIOA6kU.png)](https://www.streamlit.io/)&nbsp, with :heart: by [@DataChaz](https://twitter.com/DataChaz) &nbsp [![this is an image link](https://i.imgur.com/thJhzOO.png)](https://www.buymeacoffee.com/cwar05)')


#with c3:
#      st.write("")

with st.beta_expander("ℹ️ - About this app ", expanded=True):
  st.write("""
	    
-   StreamEA leverages the power of [Google Natural Language API](https://cloud.google.com/natural-language/docs/basics#entity_analysis) to extract entities from web pages!
-   It retrieves entities' salience scores - their overall relevance to the supplied text
-   It also highlights missing entities between pages

	    """)
      
  st.markdown("")

with st.beta_expander("🛠️ - Beta release & Support ", expanded=True):
	    st.write("""
	    
-   StreamEA is still in Beta. Feedback & bug spotting are welcome! DM me on [Twitter](https://twitter.com/DataChaz) :)
-   This app is free. If it's useful to you, you can [buy me a coffee](https://www.buymeacoffee.com/cwar05) to support my work! 🙏
	    """)

#st.markdown("---")


#endregion Top area ############################################################


def _max_width_():
    #max_width_str = f"max-width: 2000px;"
    max_width_str = f"max-width: 1300px;"
    st.markdown(
        f"""
    <style>
    .reportview-container .main .block-container{{
        {max_width_str}
    }}
    </style>    
    """,
        unsafe_allow_html=True,
    )

_max_width_()

###############################

#st.sidebar.image('Images\logo.png', use_column_width=True)
#st.sidebar.markdown("---")

keyword = st.text_input('Type a keyword')

c2, c3  = st.beta_columns(2)

#with c1:

import datetime

#    selectbox = st.selectbox('select date', [
#        'Past 5 years','Past day','Past 7 days','Past 30 days','Past 90 days'])
#
#    if selectbox == 'Past day':
#        timeframeTest = 'now 1-d'
#    elif selectbox == 'Past 7 days':
#        timeframeTest = 'now 7-d'
#    elif selectbox == 'Past 30 days':
#        timeframeTest = 'today 1-m'
#    elif selectbox == 'Past 90 days':
#        timeframeTest = 'today 3-m'
#    else:
#        timeframeTest = 'today 5-y'

with c2:
    SearchEngine = st.selectbox('Which Search Engine?',('google', 'bing'))
    #st.write("1")
#    df = pd.read_csv('countryCodes.csv')
#
#    values = df['country'].tolist()
#    options = df['code'].tolist()
#    dic = dict(zip(options, values))
#    countrycode = st.selectbox('Choose a country', options, format_func=lambda x: dic[x])

with c3:
    maxDepth = st.number_input('How many levels in tree map - deep? (2 leafs MAX for now)', min_value=1, max_value=2, value=2, step=1, key=None)

#    df2 = pd.read_csv('categorycodes.csv')
#
#    values = df2['category'].tolist()
#    options = df2['code'].tolist()
#    dic = dict(zip(options, values))
#    categorycode = st.selectbox('Choose a category', options, format_func=lambda x: dic[x])

st.header("")
button1 = st.button('Fetch Suggestions!🔥')
#button1 = st.button('🔎 Fetch suggestions! 🤘')

st.header("")
st.write("*~1 sec between queries to avoid IP blocks*")


if not keyword and not button1:  

    st.warning('⬅️ Type a keyword first.')
#   st.warning('s') #st.markdown("---")
    st.stop()

if not keyword:
    
    st.markdown("---")
    st.warning('↙️ Type a keyword first.')
    st.stop()

if keyword and not button1:
    
    st.markdown("---")
    st.warning("↙️ Press 'Fetch suggestions'")
    st.stop()

import time

@st.cache()
def suggests_function():
    return suggests.get_suggests_tree(keyword, source=SearchEngine, max_depth= maxDepth)
    #my_bar = st.progress(0)
    return st.write('Fetching Google Suggest data ...')

tree = suggests_function()

st.success('✅ Nice! Your suggestions have now been retrieved!')

st.markdown("---")

edges = suggests.to_edgelist(tree)
edges = suggests.add_parent_nodes(edges)
edges = edges.apply(suggests.add_metanodes, axis=1)

show_restricted_colsFullDF = ['root', 'edge', 'rank', 'depth', 'search_engine', 'datetime', 'parent','source_add','target_add']
#show_restricted_cols2levels = ['root', 'edge', 'rank', 'depth', 'search_engine', 'datetime', 'source_add','parent','target_add']
edges = edges[show_restricted_colsFullDF]
edges = edges.dropna()


show_restricted_cols1level = ['source_add','target_add']
show_restricted_cols2levels = ['parent','source_add','target_add']

if maxDepth == 2:
    dflimitedcolumns = edges[show_restricted_cols2levels]
    dfNoneRemoved = dflimitedcolumns.dropna()
else:
    dflimitedcolumns = edges[show_restricted_cols1level]
    dfNoneRemoved = dflimitedcolumns.dropna()

edges['datetime'] =  pd.to_datetime(edges['datetime'])

#Rename columns
edges = edges.rename({
    'root': 'Root Keyword',
    'edge': 'Full GSuggest String',
    'rank': 'Rank (Lvl 03)',
     #'depth': 'Depth',
    'search_engine': 'Search Engine',
    'datetime': 'Date & Time scraped',
    'parent': 'Level 01',
    'source_add': 'Level 02',
    'target_add': 'Level 03'

    }, axis=1)

#Re-arrange columns
edges = edges[[
    'Root Keyword',
    'Level 01',
    'Level 02',
    'Level 03',
    'Rank (Lvl 03)',
    #'Depth',
    'Full GSuggest String',
    'Search Engine',
    'Date & Time scraped',
    ]]

class Node(object):
    def __init__(self, name, size=None):
        self.name = name
        self.children = []
        self.size = size

    def child(self, cname, size=None):
        child_found = [c for c in self.children if c.name == cname]
        if not child_found:
            _child = Node(cname, size)
            self.children.append(_child)
        else:
            _child = child_found[0]
        return _child

    def as_dict(self):
        res = {'name': self.name}
        if self.size is None:
            res['children'] = [c.as_dict() for c in self.children]
        else:
            res['size'] = self.size
        return res

root = Node(keyword)

############################################

if maxDepth == 2:
    for index, row in dfNoneRemoved.iterrows():
        grp1, grp3, size = row
        root.child(grp1).child(grp3, size)
else:
    for index, row in dfNoneRemoved.iterrows():
        grp3, size = row
        root.child(grp3, size)

jsonString = json.dumps(root.as_dict(), indent=4)
jsonJSON = json.loads(jsonString)

opts = {
    "tooltip": {"trigger": "item", "triggerOn": "mousemove"},
    "series": [
        {
            "type": "tree",                  
                                    
            "data": [jsonJSON],
            "top": "1%",
            "left": "7%",
            "bottom": "1%",
            "right": "20%",
            "symbolSize": 9,
            "label": {
                "position": "left",
                "verticalAlign": "middle",
                "align": "right",
                "fontSize": 12,
            },
            "toolbox": {
                    
                    "show": True,
                    "feature": {
                        "dataZoom": {
                            "yAxisIndex": 'none'
                        },
                    "restore": {},
                    "saveAsImage": {}
                }

            },
            "leaves": {
                "label": {
                    "position": "right",
                    "verticalAlign": "middle",
                    "align": "left",
                }
            },
            "expandAndCollapse": True,
            "animationDuration": 550,
            "animationDurationUpdate": 750,
        }
    ],
}

st.markdown('### **⬇️ Interactive Tree View  **')
st.markdown('*Right-click to save Tree View as .jpeg* 📷')

st_echarts(opts, height=1000)

st.markdown('### **⬇️ Table View  **')

edges = edges.reset_index(drop=True)

st.dataframe(edges, width=1700, height=1000)

import matplotlib as plt
import seaborn as sns

cm = sns.light_palette("green", as_cmap=True)
#edgescoloured = edges.style.background_gradient(cmap=cm)
edgescoloured = edges.style.background_gradient(cmap='Blues')


#format_dictionary = { 
#'Ent. Count (1st URL)':'{:.0f}', 
#'Salience (1st URL)':'{:.1%}',
#'Salience Diff':'{:.1%}',
#'Ent. Count (2nd URL)':'{:.0f}', 
#'Salience (2nd URL)':'{:.1%}'
#}

st.table(edgescoloured)


try:
    
    csv = edges.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    #st.markdown('### ** ⬇️ Download the selected table to CSV **')
    st.markdown('### **⬇️ Export CSV file **')
    href = f'<a href="data:file/csv;base64,{b64}" download="filtered_table.csv">Click here to get your prize! 🎉</a>'
    st.markdown(href, unsafe_allow_html=True)


except NameError:
    print ('wait')


st.markdown("---")

with st.beta_expander("📝 - To-Do's ⯈", expanded=False):
  st.write("""
	    
st.markdown("•  Currently in Beta - See To-Do's* 📝")
st.markdown("•  StreamSuggets is currently in Beta - See To-Do's 📝")
st.markdown("•  ~1 sec between queries to avoid IP blocks - please be patient! :)")

- Very long articles (like [this one](https://en.wikipedia.org/wiki/COVID-19_pandemic_cases)) do not work work. I'm on it! :) 

 """)

  st.header("")

#st.markdown('*Made with* :heart: * by [@DataChaz](https://twitter.com/DataChaz)* &nbsp [![this is an image link](https://i.imgur.com/thJhzOO.png)](https://www.buymeacoffee.com/cwar05)')

#c30, c31, c32 = st.beta_columns(3)
#
#with c32:
#  #st.image('streamEASmaller2.jpg', width = 275 )
#  st.markdown("---")
#  st.markdown('###### Made in 🐍🔥, with :heart: by [@DataChaz](https://twitter.com/DataChaz) &nbsp [![this is an image link](https://i.imgur.com/thJhzOO.png)](https://www.buymeacoffee.com/cwar05)')


