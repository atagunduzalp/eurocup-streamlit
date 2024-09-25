import matplotlib.pyplot as plt

from mplsoccer import Pitch
import numpy as np
from scipy.stats import gaussian_kde
from statsbombpy import sb
import streamlit as st


def avg_positions(team_name):
    all_matches = sb.matches(competition_id=55,
                             season_id=282)
    team_matches = all_matches[(all_matches['home_team'] == team_name) | (all_matches['away_team'] == team_name)]
    team_matches = team_matches.sort_values(by='match_date')
    match_id_list = []
    for match_id in team_matches['match_id']:
        match_id_list.append(match_id)


    for match_id in match_id_list:
        # Maçın tüm etkinliklerini al
        events = sb.events(match_id=match_id)

        # Rakip takımın adını 'Starting XI' olayına göre belirle
        starting_xi_events = events[events['type'] == 'Starting XI']

        # Rakip takımın adını belirle (Türkiye olmayan takım)
        opponent_name = starting_xi_events[starting_xi_events['team'] != team_name]['team'].iloc[0]

        # Oyuna sonradan giren oyuncuları 'Substitution' olayları ile belirle
        substitutions = events[(events['type'] == 'Substitution') & (events['team'] == team_name)]
        substituted_players = substitutions['substitution_replacement'].unique()  # Sonradan giren oyuncular

        # Topla oynanan pozisyonları filtrele (Pas, Şut, Dribling, vb.)
        on_ball_actions = events[
            (events['team'] == team_name) &
            (events['type'].isin(
                ['Pass', 'Carry', 'Shot', 'Dribble', 'Ball Receipt*', 'Tackle', 'Interception', 'Ball Recovery']))
            ]

        # 'location' alanı boş olmayanları filtrele ve geçerli olanları kontrol et
        on_ball_actions = on_ball_actions.dropna(subset=['location'])

        # 'location' sütununu iki ayrı sütun olan 'x' ve 'y' olarak ayır
        on_ball_actions['x'] = on_ball_actions['location'].apply(
            lambda loc: loc[0] if isinstance(loc, list) and len(loc) == 2 else None)
        on_ball_actions['y'] = on_ball_actions['location'].apply(
            lambda loc: loc[1] if isinstance(loc, list) and len(loc) == 2 else None)

        # 'x' ve 'y' sütunları boş olmayanları filtrele
        on_ball_actions = on_ball_actions.dropna(subset=['x', 'y'])

        # Saha üzerinde takımın topa temas ettiği tüm noktaların 2D histogramı (heatmap)
        x_positions = on_ball_actions['x'].values
        y_positions = on_ball_actions['y'].values

        # Kernel Density Estimation (KDE) ile yumuşak bir ısı haritası oluşturma
        xy = np.vstack([x_positions, y_positions])
        kde = gaussian_kde(xy, bw_method=0.1)  # bw_method: Bandwidth (daha küçük değer daha keskin yapar)

        # Saha boyutuna göre grid oluşturma (daha detaylı heatmap için 100x100 grid)
        xgrid, ygrid = np.mgrid[0:120:100j, 0:80:100j]
        z = kde(np.vstack([xgrid.ravel(), ygrid.ravel()])).reshape(xgrid.shape)

        # Futbol sahası çizimi
        pitch = Pitch(pitch_type='statsbomb', pitch_color='grass', line_color='white')
        fig, ax = pitch.draw(figsize=(10, 6))

        # KDE heatmap'i çizme (dairesel görünümlü ve yumuşak)
        pos = ax.imshow(z.T, extent=[0, 120, 0, 80], origin='lower', cmap='Reds', alpha=0.5, zorder=2)

        # Ortalama pozisyonları hesapla
        avg_positions = on_ball_actions.groupby('player')[['x', 'y']].mean().reset_index()

        # Ortalama pozisyonları sahanın üzerine çiz
        for i, row in avg_positions.iterrows():
            if row['player'] in substituted_players:
                # Oyuna sonradan girenler için farklı bir renk kullan
                ax.scatter(row['x'], row['y'], s=100, c='blue', edgecolors='black', zorder=3,
                           label='Substitute' if i == 0 else "")
            else:
                # Başlangıç oyuncuları için farklı bir renk kullan
                ax.scatter(row['x'], row['y'], s=100, c='red', edgecolors='black', zorder=3,
                           label='Starting XI' if i == 0 else "")

        # Oyuncu isimlerini pozisyonlarına yaz
        for i, row in avg_positions.iterrows():
            ax.text(row['x'], row['y'], row['player'], fontsize=10, ha='center', va='center', color='white', zorder=4)

        # Başlık ve görselleştirme
        plt.title(f'{team_name} vs {opponent_name} - Average Positions and Team Heatmap)',
                  fontsize=15)

        # Legend (Açıklama)
        ax.legend(loc='upper right')
        plt.colorbar(pos, ax=ax)
        plt.show()
        st.pyplot(plt.gcf())

# debugging
# match_id = 3942382  # Replace with the match ID you are interested in#
# match_id_list = []
# all_matches = sb.matches(competition_id=55,
#                              season_id=282)
# team_matches = all_matches[(all_matches['home_team'] == 'Turkey') | (all_matches['away_team'] == 'Turkey')]
# for match_id in team_matches['match_id']:
#     match_id_list.append(match_id)
#
# avg_positions(match_id_list, 'Turkey')

# area_counts, bins_x, bins_y = calculate_area_percentages(passes, player_name)
# plot_area_percentages(area_counts, bins_x, bins_y)