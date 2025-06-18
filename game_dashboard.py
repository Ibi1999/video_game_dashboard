import streamlit as st
import pandas as pd
import squarify
import os
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from function_utils import *

st.set_page_config(layout="wide")

def load_data():
    my_game_data = pd.read_csv('my_game_data.csv')
    unique_genres_df = pd.read_csv('unique_genres_df.csv')
    unique_features_df = pd.read_csv('unique_features_df.csv')
    return my_game_data, unique_genres_df, unique_features_df

def normalize_genres(genres_str):
    if pd.isna(genres_str):
        return genres_str
    normalized = genres_str
    normalized = normalized.replace("Hack and slash/Beat 'em up", "Hack & Slash")
    normalized = normalized.replace("Hack and Slash", "Hack & Slash")
    return normalized

def section_title(title):
    st.markdown(f"""
        <h3 style="display: flex; align-items: center; text-align: center; font-size: 36px;">
            <span style="flex: 1; height: 3px; background: #ccc;"></span>
            <span style="padding: 0 10px;">{title}</span>
            <span style="flex: 1; height: 3px; background: #ccc;"></span>
        </h3>
    """, unsafe_allow_html=True)

def main():

    from PIL import Image

    # Load and display logo in the top-left
    logo = Image.open("logo.png")

    col1, col2 = st.columns([1, 6])
    with col1:
        st.image(logo, width=80)  # Adjust width as needed
        st.markdown("<small>Created by Ibrahim Oksuzoglu</small>", unsafe_allow_html=True)
    with col2:
        pass
    
    section_title("🎮 Video Game Dashboard")

    my_game_data, unique_genres_df, unique_features_df = load_data()

    # Normalize genres as before
    my_game_data['Genres'] = my_game_data['Genres'].apply(normalize_genres)
    unique_genres_df['Genre'] = unique_genres_df['Genre'].replace({
        "Hack and slash/Beat 'em up": "Hack & Slash",
        "Hack and Slash": "Hack & Slash"
    })

    # Map User Score to rating labels
    rating_map = {
        1: "😞 Bad",
        2: "😐 Meh",
        3: "😊 Good",
        4: "🌟 Exceptional"
    }
    my_game_data['My Ratings'] = my_game_data['User Score'].map(rating_map)

    # Available filter options
    genres_available = unique_genres_df['Genre'].dropna().unique().tolist()
    platforms_available = my_game_data['Sources'].dropna().str.split(', ').explode().unique().tolist()
    features_available = unique_features_df['Feature'].dropna().unique().tolist()
    ratings_available = ["😞 Bad", "😐 Meh", "😊 Good", "🌟 Exceptional"]

    # Filter UI: 4 columns for Platforms, Genres, Features, My Ratings
    col1, col2, col3, col4 = st.columns(4)
    with col2:
        selected_platforms = st.multiselect("🕹️ Select By Platforms", platforms_available, default=[])
    with col4:
        selected_genres = st.multiselect("🎯 Select By Genres", genres_available, default=[])
    with col3:
        selected_features = st.multiselect("🛠️ Select By Features", features_available, default=[])
    with col1:
        selected_ratings = st.multiselect("⭐ Select ByMy Ratings", ratings_available, default=[])

    df_filtered = my_game_data.copy()

    # Filter by genres
    if selected_genres:
        df_filtered = df_filtered[
            df_filtered['Genres'].apply(
                lambda x: any(genre.lower() in str(x).lower() for genre in selected_genres)
            )
        ]

    # Filter by platforms
    if selected_platforms:
        df_filtered = df_filtered[
            df_filtered['Sources'].apply(
                lambda x: any(platform in str(x).split(', ') for platform in selected_platforms)
            )
        ]

    # Filter by features
    if selected_features:
        df_filtered = df_filtered[
            df_filtered['Features'].apply(
                lambda x: any(feature in str(x).split(', ') for feature in selected_features)
            )
        ]

    # Filter by ratings
    if selected_ratings:
        df_filtered = df_filtered[
            df_filtered['My Ratings'].isin(selected_ratings)
        ]

    if df_filtered.empty:
        st.info("❗ No games found that match the selected filters.")
        return

    # Section: Platform Distribution
    section_title("🕹️ Platform Distribution")

    # Create columns for count, plot, and playtime
    col1, col2, col3 = st.columns([1, 6, 1])

    with col1:
        fig = plot_game_count_card(df_filtered)
        st.pyplot(fig)

    with col2:
        fig = platform_distribution(df_filtered)
        st.pyplot(fig)

    with col3:
        fig = plot_total_playtime_card(df_filtered)
        st.pyplot(fig)

    # Two-column layout for other plots
    col1, col2 = st.columns(2)

    with col1:
        section_title("🏆 Top 10 games by time played")
        fig = plot_top_10_games_by_time_played(df_filtered)
        st.pyplot(fig)

    with col2:
        section_title("🎨 Top 10 Genres in Library")
        fig = plot_top_10_genres_treemap(df_filtered, unique_genres_df)
        st.pyplot(fig)

    # Games released over time section
    section_title("📅 Games released over time")
    fig = plot_games_over_time(df_filtered)
    st.pyplot(fig)

    # Show the filtered dataframe with scroll
    section_title("📋 Game Output")
    st.dataframe(df_filtered[['Name','My Ratings','Developers','Features','Genres','Release Date','Sources','Time Played']], height=400)


if __name__ == "__main__":
    main()
