import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from PIL import Image
import plotly.express as px

st.set_page_config(layout="wide")

header = st.container()
dataset = st.container()
features = st.container()
image = Image.open('../img/profile.jpg')

st.markdown(
    """"
    <style>
    .main {
        background-color: #F5F5F5;
        color: #e08882;
    }
    </style>
    """,
    unsafe_allow_html=True
)


with st.sidebar:
    st.subheader('About')
    st.markdown('Visualization & Analyze data about e-commerce customer behavior.')
    st.write("Data source: [Kaggle](https://www.kaggle.com/datasets/mkechinov/ecommerce-behavior-data-from-multi-category-store)")

with header:
    st.title('ECommerce_behavior')
    st.image(image)
    
with dataset:
    st.header('eCommerce behavior data from multi category store') 

    # Loading data
    df = pd.read_csv('../data/2019-Nov.csv', nrows=10000000, error_bad_lines=False)
    st.write(df.head(10))

    # Data Cleaning
    # Drop Duplicate Values and columns of no use
    # check for deplicate rows
    df.duplicated().sum()
    df = df.drop_duplicates()
    df = df.dropna()

    # Data type
    df_event_type = df['event_type'].value_counts().rename_axis('event_type_group').reset_index(name='counts')
    fig = px.pie(df_event_type, values='counts', names='event_type_group')
    fig.update_traces(
        textinfo='percent+label')
    st.plotly_chart(fig)

with features:

    # Customer behavior
    # Top 10 brand that most customer purchased vs. view
    st.subheader('Top 10 brand that most customer purchased vs. view')

    # most customer purchased
    purchased = df.loc[df.event_type == 'purchase']
    purchases_with_brands = purchased.loc[purchased.brand.notnull()]

    purchased_top_sellers = purchases_with_brands.groupby('brand').brand.agg([len]).sort_values(by="len", ascending=False)
    purchased_top_sellers.reset_index(inplace=True)
    purchased_top_sellers.rename(columns={"len" : "# sales"}, inplace=True)

    # most customer view
    view = df.loc[df.event_type == 'view']
    view_with_brands = view.loc[view.brand.notnull()]

    view_top_sellers = view_with_brands.groupby('brand').brand.agg([len]).sort_values(by="len", ascending=False)
    view_top_sellers.reset_index(inplace=True)
    view_top_sellers.rename(columns={"len" : "# sales"}, inplace=True)


    # Create subplots: use 'domain' type for Pie subplot
    fig = make_subplots(column_widths=[400,400], rows=1, cols=2,
            subplot_titles = ["Purchased", "Viewed"], 
            specs=[[{'type':'domain'}, {'type':'domain'}]])
    fig.add_trace(go.Pie(labels=purchased_top_sellers["brand"].head(10), values=purchased_top_sellers["# sales"].head(10), name="Purchased"),
              1, 1)
    fig.add_trace(go.Pie(labels=view_top_sellers["brand"].head(10), values=view_top_sellers["# sales"].head(10), name="Viewed"),
              1, 2)

    # Use `hole` to create a donut-like pie chart
    fig.update_traces(hole=.4, hoverinfo="label+percent+name", textinfo='percent+label')

    fig.update_layout(
        width=1000, height=500)

    st.plotly_chart(fig)
