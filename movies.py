import streamlit as st  
import pandas as pd
import plotly.express as px

# Load the dataset
df = pd.read_csv("movies_dataset.csv")  # Replace with your actual dataset file

# Streamlit Page Config
st.set_page_config(page_title="Movie Insights Dashboard", layout="wide")

# Sidebar Filters
st.sidebar.header("Filters")
year_range = st.sidebar.slider("Select Year Range", int(df['Year'].min()), int(df['Year'].max()), (2000, 2023))
genre_filter = st.sidebar.multiselect("Select Genre", df['Genre'].unique())

# Apply Filters
filtered_df = df[(df['Year'] >= year_range[0]) & (df['Year'] <= year_range[1])]
if genre_filter:
    filtered_df = filtered_df[filtered_df['Genre'].isin(genre_filter)]

# Main Title
st.title("🎬 Movie Insights Dashboard")
st.markdown("Explore movie trends, box office insights, and more!")

# Genre Distribution Chart
st.subheader("Genre Distribution")
genre_counts = filtered_df['Genre'].value_counts().reset_index()
genre_counts.columns = ["Genre", "Count"]
fig1 = px.bar(genre_counts, x="Genre", y="Count", color="Genre", title="Movie Count by Genre")
st.plotly_chart(fig1, use_container_width=True)

# Box Office vs. Budget Scatter Plot
st.subheader("Box Office vs. Budget")
fig2 = px.scatter(filtered_df, x="Budget_Million", y="Box_Office_Million", color="Genre", 
                   hover_data=["Movie_Title", "Director"], title="Budget vs. Box Office")
st.plotly_chart(fig2, use_container_width=True)

# Yearly Movie Trends
st.subheader("Movies Released Over Time")
yearly_counts = filtered_df.groupby("Year").size().reset_index(name="Count")
fig3 = px.line(yearly_counts, x="Year", y="Count", markers=True, title="Number of Movies Released per Year")
st.plotly_chart(fig3, use_container_width=True)

# Director Impact
st.subheader("Top Directors by Box Office")
director_earnings = filtered_df.groupby("Director")['Box_Office_Million'].sum().reset_index()
director_earnings = director_earnings.sort_values(by="Box_Office_Million", ascending=False).head(10)
fig4 = px.bar(director_earnings, x="Director", y="Box_Office_Million", title="Top 10 Directors by Box Office")
st.plotly_chart(fig4, use_container_width=True)

# Footer
st.markdown("---")
#st.markdown("Built with using Streamlit & Plotly")
