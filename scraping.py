import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

def scrape_data():
    url = "https://www.wscubetech.com/blog/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'lxml')
    posts = soup.find_all("div", class_="tmc-posts-card")

    categorylist = []
    titlelist = []
    authorlist = []
    datelist = []
    imagelist = []

    for post in posts:
        category = post.find("a", attrs={"rel": "category tag"})
        categorylist.append(category.text.strip() if category else None)

        title = post.find("h3", class_="tmc-posts-card-title")
        titlelist.append(title.a.text.strip() if title else None)

        author = post.find("a", class_="tmc-posts-card-author-link")
        authorlist.append(author.text.strip() if author else None)

        date = post.find("a", class_="tmc-posts-card-date-link")
        datelist.append(date.text.strip() if date else None)

        image = post.find("a", class_="tmc-posts-card-featured-img")
        if image:
            img_tag = image.find("img")
            imagelist.append(img_tag['src'] if img_tag else "https://via.placeholder.com/150")
        else:
            imagelist.append("https://via.placeholder.com/150")

    df = pd.DataFrame({
        "Category": categorylist,
        "Title": titlelist,
        "Author": authorlist,
        "Date": datelist,
        "Image": imagelist
    })
    
    df['Date'] = pd.to_datetime(df['Date'])
    return df

df = scrape_data()

st.set_page_config(
    layout="wide",  
    page_title="Blog News Articles", 
    page_icon="1.png", 
    initial_sidebar_state="auto" 
)



st.markdown("<div style='height:4px; margin-bottom:10px; border-radius:50px; background-color: blue; border: none;'></div>", unsafe_allow_html=True)  
col1, col2 = st.columns([1,4])
with col1:
    st.image("1.png")
with col2:
    st.markdown("<div style='height:8px; margin-bottom:10px; border-radius:50px; background-color: blue; border: none;'></div>", unsafe_allow_html=True)  
    st.markdown("<div style='height:6px; margin-bottom:10px; border-radius:50px; background-color: blue; border: none;'></div>", unsafe_allow_html=True)  
    st.markdown("<div style='height:6px; margin-bottom:10px; border-radius:50px; background-color: blue; border: none;'></div>", unsafe_allow_html=True)  
    st.markdown("<div style='height:6px; margin-bottom:10px; border-radius:50px; background-color: blue; border: none;'></div>", unsafe_allow_html=True)  
    st.markdown("<div style='height:6px; margin-bottom:10px; border-radius:50px; background-color: blue; border: none;'></div>", unsafe_allow_html=True)  
    st.markdown("<div style='height:4px; margin-bottom:10px; border-radius:50px; background-color: blue; border: none;'></div>", unsafe_allow_html=True)  
    st.markdown("<h1>Blog : Tech News App by Muhammad Usman</h1>", unsafe_allow_html=True)
    st.markdown("<div style='height:4px; margin-top:10px; border-radius:50px; background-color: blue; border: none;'></div>", unsafe_allow_html=True)  
    st.markdown("<div style='height:6px; margin-top:10px; border-radius:50px; background-color: blue; border: none;'></div>", unsafe_allow_html=True)  
    st.markdown("<div style='height:6px; margin-top:10px; border-radius:50px; background-color: blue; border: none;'></div>", unsafe_allow_html=True)  
    st.markdown("<div style='height:6px; margin-top:10px; border-radius:50px; background-color: blue; border: none;'></div>", unsafe_allow_html=True)  
    st.markdown("<div style='height:6px; margin-top:10px; border-radius:50px; background-color: blue; border: none;'></div>", unsafe_allow_html=True)  
    st.markdown("<div style='height:6px; margin-top:10px; border-radius:50px; background-color: blue; border: none;'></div>", unsafe_allow_html=True)  
    st.markdown("<div style='height:6px; margin-bottom:10px; border-radius:50px; background-color: blue; border: none;'></div>", unsafe_allow_html=True)  
    st.markdown("<div style='height:8px; margin-bottom:10px; border-radius:50px; background-color: blue; border: none;'></div>", unsafe_allow_html=True) 
st.markdown("<div style='height:4px; margin-bottom:10px; border-radius:50px; background-color: red; border: none;'></div>", unsafe_allow_html=True)  

# Filters
col1, col2, col3 = st.columns(3)
with col1:
    start_date = st.date_input("Start Date", value=df['Date'].min().date())
with col2:
    end_date = st.date_input("End Date", value=df['Date'].max().date())
with col3:
    categories = df['Category'].unique()
    selected_categories = st.multiselect("Select Categories", categories, default=categories)

st.markdown("<div style='height:4px; margin-bottom:10px; border-radius:50px; background-color: red; border: none;'></div>", unsafe_allow_html=True)  
# Filter data based on selections
filtered_df = df[
    (df['Date'].dt.date >= start_date) &
    (df['Date'].dt.date <= end_date) &
    (df['Category'].isin(selected_categories))
]

# Display data in two columns
for index, row in filtered_df.iterrows():
    col1, col2 = st.columns([2, 2])  

    with col1:
        st.image(row['Image'], use_column_width=True)
        
    with col2:
        st.header(row['Title'])
        st.write(f"**Category:** {row['Category']}")
        st.write(f"**Author:** {row['Author']}")
        st.write(f"**Date:** {row['Date'].strftime('%Y-%m-%d')}")

    st.markdown("<hr style='margin: 20px 0;'>", unsafe_allow_html=True)