# Functions
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import os
import numpy as np
import pandas as pd
import squarify
import matplotlib.patches as patches

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import os

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import os

def platform_distribution(df, icon_path='icons'):
    # Map source names to icon files
    source_icon_map = {
        "Steam": "steam.png",
        "Epic": "epic.png",
        "PlayStation": "psn.png",
        "Battle.net": "battlenet.png",
        "Riot Games": "riot.png"
    }
    zoom_levels = {
        "Steam": 0.03,
        "Epic": 0.04,
        "PlayStation": 0.02,
        "Battle.net": 0.035,
        "Riot Games": 0.035
    }

    df_sources = df.dropna(subset=["Sources"])
    df_sources = df_sources.assign(Sources=df_sources["Sources"].str.split(', '))
    source_counts = df_sources.explode("Sources")["Sources"].value_counts()
    total = source_counts.sum()

    fig, ax = plt.subplots(figsize=(16, 1.8), dpi=1000)
    left = 0
    colors = plt.cm.Dark2.colors

    for i, (source, count) in enumerate(source_counts.items()):
        bar_color = colors[i % len(colors)]
        ax.barh(0, count, left=left, label=source, color=bar_color, edgecolor='white', linewidth=0.5)

        icon_file = source_icon_map.get(source)
        if icon_file:
            icon_path_full = os.path.join(icon_path, icon_file)
            if os.path.exists(icon_path_full):
                img = plt.imread(icon_path_full)
                zoom = zoom_levels.get(source, 0.05)
                imagebox = OffsetImage(img, zoom=zoom)
                ab = AnnotationBbox(imagebox, (left + count / 2, 0), frameon=False)
                ax.add_artist(ab)

        label = f"{(count / total * 100):.0f}%" if source not in ["Battle.net", "Riot Games"] else f"{(count / total * 100):.0f}"
        ax.text(left + count / 2, -0.25, label, ha='center', va='top', color='white', fontsize=10, fontweight='bold')

        left += count

    ax.xaxis.set_visible(True)
    ax.tick_params(axis='x', colors='white')
    ax.set_yticks([])
    ax.set_xlim(0, left)

    fig.patch.set_facecolor('#262730')
    ax.set_facecolor('#262730')

    # Add thin white border around the plot area
    border = patches.Rectangle(
        (0, 0), 1, 1,
        transform=ax.transAxes,
        fill=False,
        edgecolor='white',
        linewidth=1.2,
        zorder=10
    )
    ax.add_patch(border)

    leg = ax.legend(
        loc='upper center',
        bbox_to_anchor=(0.5, -0.2),
        ncol=len(source_counts),
        frameon=False,
    )
    leg.get_frame().set_facecolor('#262730')
    for text in leg.get_texts():
        text.set_color('white')

    plt.subplots_adjust(bottom=0.3)
    plt.tight_layout()

    return fig



def plot_top_5_genres_with_custom_title(game_df, unique_genres_df, top_n=10):
    genre_counts = []
    for genre in unique_genres_df['Genre']:
        count = game_df['Genres'].dropna().str.contains(genre, case=False, na=False).sum()
        genre_counts.append((genre, count))

    genre_counts = sorted(genre_counts, key=lambda x: x[1], reverse=True)[:top_n]
    labels = [f"{genre}\n{count} Games" for genre, count in genre_counts]
    counts = [count for _, count in genre_counts]

    fig, ax = plt.subplots(figsize=(8, 5))
    fig.patch.set_facecolor('#262730')
    ax.set_facecolor('#262730')

    # ✅ Vertical bars with white outlines
    bars = ax.bar(labels, counts, color='#1b73ad', edgecolor='white', linewidth=1)

    # Axis formatting
    ax.tick_params(axis='x', colors='white', labelsize=10, rotation=20)
    ax.tick_params(axis='y', colors='white', labelsize=12)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('white')
    ax.spines['bottom'].set_color('white')
    ax.yaxis.label.set_color('white')
    ax.grid(axis='y', color='white', linestyle='--', alpha=0.2)

    return fig



def plot_games_over_time(game_df):
    # Ensure Release Date is datetime
    game_df['Release Date'] = pd.to_datetime(game_df['Release Date'], errors='coerce')
    
    # Drop rows with invalid dates
    game_df = game_df.dropna(subset=['Release Date'])
    
    # Extract year
    game_df['Year'] = game_df['Release Date'].dt.year
    
    # Count games per year
    counts_per_year = game_df.groupby('Year').size().reset_index(name='Count')
    
    # Create full range of years for x-ticks
    all_years = list(range(counts_per_year['Year'].min(), counts_per_year['Year'].max() + 1))
    
    fig, ax = plt.subplots(figsize=(18, 4))
    fig.patch.set_facecolor('#262730')   # figure background color
    ax.set_facecolor('#262730')          # axes background color
    
    # Plot line graph
    ax.plot(counts_per_year['Year'], counts_per_year['Count'], 
            color='#1b73ad', linewidth=2.5, marker='o')
    
    # Set x-ticks to every year
    ax.set_xticks(all_years)
    ax.set_xticklabels(all_years, rotation=45, color='white', fontsize=10)
    
    # Style y-ticks
    ax.tick_params(axis='y', colors='white')

    # Style spines
    for spine in ['top', 'right']:
        ax.spines[spine].set_visible(False)
    for spine in ['left', 'bottom']:
        ax.spines[spine].set_color('white')
    
    # Remove all gridlines
    ax.grid(False)
    
    plt.tight_layout()
    return fig




def plot_top_10_games_by_time_played(game_df, top_n=10):
    # Drop rows with missing Time Played or Name
    df = game_df.dropna(subset=['Time Played', 'Name'])
    
    # Sort descending by Time Played and select top N
    top_games = df.sort_values(by='Time Played', ascending=False).head(top_n)
    
    # Format labels with spaces between game name and time played (in hours for readability)
    labels = [f"{name}         {time_played/3600:.1f} hrs" for name, time_played in zip(top_games['Name'], top_games['Time Played'])]
    counts = top_games['Time Played'].tolist()
    
    fig, ax = plt.subplots(figsize=(8, 5))
    fig.patch.set_facecolor('#262730')
    ax.set_facecolor('#262730')
    
    # ✅ Add bar edge color
    ax.barh(labels, counts, color='#1b73ad', edgecolor='white', linewidth=1, height=0.2)
    ax.invert_yaxis()
    
    ax.tick_params(axis='y', colors='white', labelsize=12)
    ax.xaxis.set_visible(False)
    for spine in ['top', 'right', 'bottom', 'left']:
        ax.spines[spine].set_visible(False)
    ax.grid(axis='y', visible=False)
    
    return fig


def plot_top_10_genres_treemap(game_df, unique_genres_df, top_n=10):
    genre_counts = []
    for genre in unique_genres_df['Genre']:
        count = game_df['Genres'].dropna().str.contains(genre, case=False).sum()
        if count > 0:
            genre_counts.append((genre, count))

    genre_counts = sorted(genre_counts, key=lambda x: x[1], reverse=True)[:top_n]
    labels = [f"{genre}\n{count} games" for genre, count in genre_counts]
    sizes = [count for _, count in genre_counts]

    fig, ax = plt.subplots(figsize=(8, 3))
    fig.patch.set_facecolor('#262730')
    ax.set_facecolor('#262730')

    # Use same background color for boxes and white lines for separation
    squarify.plot(
        sizes=sizes,
        label=labels,
        color=['#262730'] * len(sizes),
        edgecolor='#1b73ad',
        linewidth=2,
        text_kwargs={'color': 'white', 'fontsize': 8}
    )
    

    plt.axis('off')
    return fig


def plot_user_score_distribution(df):
    fig, ax = plt.subplots()
    counts = df['User Score'].value_counts().sort_index()
    bars = ax.bar(counts.index, counts.values, color='#1b73ad', edgecolor='white', linewidth=1)
    ax.set_xlabel("User Score")
    ax.set_ylabel("Number of Games")
    ax.set_title("Distribution of User Scores")
    ax.set_xticks([1, 2, 3, 4, 5])
    ax.spines['bottom'].set_color('white')
    ax.spines['left'].set_color('white')
    ax.tick_params(colors='white')
    ax.set_facecolor('#262730')
    fig.patch.set_facecolor('#262730')
    return fig


def plot_total_playtime_card(df):
    total_seconds = df['Time Played'].sum(skipna=True)
    total_hours = total_seconds / 3600

    fig, ax = plt.subplots(figsize=(2.8, 1.8), dpi=100)
    fig.patch.set_facecolor('#262730')
    ax.set_facecolor('#262730')
    ax.axis('off')

    # Card background
    card = patches.FancyBboxPatch(
        (0, 0), 1, 1,
        boxstyle="round,pad=0.02",
        linewidth=2,
        edgecolor='white',
        facecolor='#1e1e1e',
        transform=ax.transAxes,
        clip_on=False
    )
    ax.add_patch(card)

    # Title
    ax.text(0.5, 0.7, "Total Play Time", ha='center', va='center',
            fontsize=12, color='white', weight='bold', transform=ax.transAxes)

    # Value in hours
    ax.text(0.5, 0.35, f"{total_hours:,.1f} hrs", ha='center', va='center',
            fontsize=18, color='#1b73ad', weight='bold', transform=ax.transAxes)

    return fig


def plot_game_count_card(df):
    total_games = len(df)

    fig, ax = plt.subplots(figsize=(2.8, 1.8), dpi=100)
    fig.patch.set_facecolor('#262730')
    ax.set_facecolor('#262730')
    ax.axis('off')

    # Card background with white border
    card = patches.FancyBboxPatch(
        (0, 0), 1, 1,
        boxstyle="round,pad=0.02",
        linewidth=2,
        edgecolor='white',
        facecolor='#1e1e1e',
        transform=ax.transAxes,
        clip_on=False
    )
    ax.add_patch(card)

    # Title
    ax.text(0.5, 0.7, "Game Count", ha='center', va='center',
            fontsize=12, color='white', weight='bold', transform=ax.transAxes)
    
    # Value
    ax.text(0.5, 0.35, f"{total_games:,}", ha='center', va='center',
            fontsize=18, color='#1b73ad', weight='bold', transform=ax.transAxes)

    return fig