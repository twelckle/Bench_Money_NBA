import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import pandas as pd
from PIL import Image, ImageOps, ImageDraw
import io
import cairosvg
from matplotlib.gridspec import GridSpec
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.font_manager as fm
import requests
import os
import colorsys
import numpy as np
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color

logo_colors = {
    'ATL': {'primary': '#C8102E', 'secondary': '#FFFFFF'},  # Atlanta Hawks
    'BKN': {'primary': '#000000', 'secondary': '#FFFFFF'},  # Brooklyn Nets  
    'BOS': {'primary': '#008348', 'secondary': '#BB9753'},  # Boston Celtics
    'CHA': {'primary': '#1D1160', 'secondary': '#00788C'},  # Charlotte Hornets
    'CHI': {'primary': '#CE1141', 'secondary': '#000000'},  # Chicago Bulls
    'CLE': {'primary': '#860038', 'secondary': '#BC945C'},  # Cleveland Cavaliers  
    'DAL': {'primary': '#0064B1', 'secondary': '#BBC4CA'},  # Dallas Mavericks 
    'DEN': {'primary': '#0D2240', 'secondary': '#FFC627'},  # Denver Nuggets  
    'DET': {'primary': '#C8102E', 'secondary': '#1D428A'},  # Detroit Pistons
    'GSW': {'primary': '#FDB903', 'secondary': '#00408C'},  # Golden State Warriors  
    'HOU': {'primary': '#CB1040', 'secondary': '#000000'},  # Houston Rockets
    'IND': {'primary': '#FDBB30', 'secondary': '#002D62'},  # Indiana Pacers  
    'LAC': {'primary': '#0B2140', 'secondary': '#CA0E2D'},  # LA Clippers  
    'LAL': {'primary': '#542C81', 'secondary': '#FAB624'},  # Los Angeles Lakers
    'MEM': {'primary': '#5D76A9', 'secondary': '#12173F'},  # Memphis Grizzlies 
    'MIA': {'primary': '#98002E', 'secondary': '#000000'},  # Miami Heat
    'MIL': {'primary': '#00471B', 'secondary': '#EEE1C6'},  # Milwaukee Bucks
    'MIN': {'primary': '#0D2240', 'secondary': '#77BC1F'},  # Minnesota Timberwolves 
    'NOP': {'primary': '#B4975A', 'secondary': '#0A2240'},  # New Orleans Pelicans 
    'NYK': {'primary': '#F38223', 'secondary': '#006CB4'},  # New York Knicks 
    'OKC': {'primary': '#007AC1', 'secondary': '#F05133'},  # Oklahoma City Thunder 
    'ORL': {'primary': '#0B77BD', 'secondary': '#000000'},  # Orlando Magic
    'PHI': {'primary': '#006BB6', 'secondary': '#EC174C'},  # Philadelphia 76ers
    'PHX': {'primary': '#E56020', 'secondary': '#000000'},  # Phoenix Suns 
    'POR': {'primary': '#CE092B', 'secondary': '#FEFEFE'},  # Portland Trail Blazers
    'SAC': {'primary': '#592D81', 'secondary': '#63717A'},  # Sacramento Kings
    'SAS': {'primary': '#C0C9D0', 'secondary': '#000000'},  # San Antonio Spurs
    'TOR': {'primary': '#BD1B21', 'secondary': '#000000'},  # Toronto Raptors 
    'UTA': {'primary': '#904DCB', 'secondary': '#A04949'},  # Utah Jazz
    'WAS': {'primary': '#0D2240', 'secondary': '#CF0A2C'},  # Washington Wizards
}

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_lab(rgb):
    srgb = sRGBColor(rgb[0]/255, rgb[1]/255, rgb[2]/255)
    lab = convert_color(srgb, LabColor)
    return lab

def color_difference(lab1, lab2):
    delta_e = np.sqrt((lab1.lab_l - lab2.lab_l) ** 2 + 
                      (lab1.lab_a - lab2.lab_a) ** 2 + 
                      (lab1.lab_b - lab2.lab_b) ** 2)
    return delta_e

def are_colors_too_similar(color1_hex, color2_hex, threshold=20):
    rgb1 = hex_to_rgb(color1_hex)
    rgb2 = hex_to_rgb(color2_hex)
    lab1 = rgb_to_lab(rgb1)
    lab2 = rgb_to_lab(rgb2)
    delta_e = color_difference(lab1, lab2)
    return (delta_e < threshold)

def download_image(url, filename):
    response = requests.get(url)
    img = Image.open(io.BytesIO(response.content))
    img = img.convert('RGBA')  # Ensure the image is in RGB format
    img.save(filename)
    return img

def crop_top(img, crop_height_ratio=0.7):
    width, height = img.size
    crop_height = int(height * crop_height_ratio)
    return img.crop((0, 0, width, crop_height))

# Function to convert SVG to high-resolution PNG for matplotlib
def svg_to_png(svg_path, dpi=300):
    png_image = cairosvg.svg2png(url=svg_path, dpi=dpi)
    return Image.open(io.BytesIO(png_image))

# Function to place the logo using OffsetImage and AnnotationBbox
def place_logo(ax, logo_path, zoom=1.0, position=(0, 1)):
    logo_img = Image.open(logo_path)
    imagebox = OffsetImage(logo_img, zoom=zoom)
    ab = AnnotationBbox(imagebox, position, frameon=False, xycoords='axes fraction', boxcoords="axes fraction", pad=0, box_alignment=(0, 1))
    ax.add_artist(ab)

def get_dynamic_font_size(text, max_width, font_properties, renderer, fig):
    font_size = font_properties.get_size_in_points()
    prop = font_properties  # The FontProperties object
    ismath = False  # Whether the text is a math expression

    text_width = renderer.get_text_width_height_descent(text, prop, ismath)[0] / fig.dpi

    while text_width > max_width and font_size > 1:
        font_size -= 1
        font_properties.set_size(font_size)
        text_width = renderer.get_text_width_height_descent(text, prop, ismath)[0] / fig.dpi

    return font_properties


def make_image(data):
    df = pd.DataFrame(data)

    # Data
    total_spending = df['Spending'].sum()
    team_a_spending = df['Spending'][0]
    team_b_spending = df['Spending'][1]
    date = df['Date'].iloc[0]
    dateSave= df['DateSave'].iloc[0]
    team_a_ids = df['PlayerIDs'][0]
    team_b_ids = df['PlayerIDs'][1]
    team_a_money = df['Money'][0]
    team_b_money = df['Money'][1]

    # Calculate the proportion of spending
    team_a_ratio = team_a_spending / total_spending
    team_b_ratio = team_b_spending / total_spending

     # Load custom font
    font_path = '/Users/twelckle/Library/Fonts/entsans.ttf'
    font_prop = fm.FontProperties(fname=font_path)

    font_title = font_prop.copy()
    font_title.set_size(37)
    font_title.set_weight('bold')

    font_score = font_prop.copy()
    font_score.set_size(34)
    font_score.set_weight('bold')

    font_minutes = font_prop.copy()
    font_minutes.set_size(6)
    # font_names.set_weight('bold')

    font_heading = font_prop.copy()
    font_heading.set_size(18)
    # font_names.set_weight('bold')

    font_subText = font_prop.copy()
    font_subText.set_size(10)
    
    font_names = fm.FontProperties(family='Arial', size=12)
    font_money = fm.FontProperties(family='Arial Black', size=12)
    # font_heading = fm.FontProperties(family='Arial Black', weight='bold', size=18)
    font_body = fm.FontProperties(family='Arial Black', size=12)

    # Create the plot with GridSpec
    fig = plt.figure(figsize=(12, 10), facecolor='#c9c9c9')  # Set the background color and figure size here c9c9c9

    gs = GridSpec(5, 1, height_ratios=[0.07, 0.13, 0.20, 0.10, 0.30])  # Adjust height ratios

    # Create an axis to place the main logo
    logo_ax = fig.add_subplot(gs[0])
    logo_ax.axis('off')  # Hide the axes for the logo

    # Place the main logo in the top left corner
    place_logo(logo_ax, './nba_logos/logo.png', zoom=0.08, position=(0, 0.9))  # Adjust zoom and position to place the main logo in the top left corner

    # Add date to the top right corner
    logo_ax.text(0.99, 0, date, ha='right', va='top', fontproperties=font_heading, transform=logo_ax.transAxes)

    # Title subplot
    title_ax = fig.add_subplot(gs[1])
    title_ax.axis('off')  # Hide the axes for the title
    title = 'Bench Money'
    title_ax.text(0.5, 0.25, title, ha='center', va='center', fontproperties=font_title)

    # Logos subplot
    logos_ax = fig.add_subplot(gs[2])
    logos_ax.axis('off')  # Hide the axes for the logos

    # Convert SVG logos to high-resolution PNG
    teama_png = f'./nba_logos/{df["Team"][0]}.svg'
    teamb_png = f'./nba_logos/{df["Team"][1]}.svg'

    logo_team_a = svg_to_png(teama_png, dpi=300)
    logo_team_b = svg_to_png(teamb_png, dpi=300)

    team_a_score = df['Score'][0]
    team_b_score = df['Score'][1]

    logo_team_a_x = 0.15
    logo_team_b_x = 0.85
    # Add the scores with respective colors
    logos_ax.text(logo_team_a_x+0.25, 0.4, str(team_a_score), ha='center', va='bottom', fontproperties=font_score)
    logos_ax.text(logo_team_b_x-0.25, 0.4, str(team_b_score), ha='center', va='bottom', fontproperties=font_score)

    # Convert logos to arrays without resizing
    def get_image(image, zoom=0.9):  # Adjust the zoom to control display size
        return OffsetImage(image, zoom=zoom)  # Adjust zoom to fit the preset image size

    # Place the team logos in the logos subplot
    ab_team_a = AnnotationBbox(get_image(logo_team_a, zoom=0.18), (logo_team_a_x, 0.5), frameon=False, box_alignment=(0.5, 0.5))
    ab_team_b = AnnotationBbox(get_image(logo_team_b, zoom=0.18), (logo_team_b_x, 0.5), frameon=False, box_alignment=(0.5, 0.5))

    logos_ax.add_artist(ab_team_a)
    logos_ax.add_artist(ab_team_b)

    # Bar graph subplot
    ax = fig.add_subplot(gs[3])

    # Centering the bar
    bar_height = 0.3

    # Draw the bar
    total = team_a_ratio + team_b_ratio
    teamOneColor = logo_colors[df["Team"][0]]['primary']
    teamTwoColor = logo_colors[df["Team"][1]]['primary']
    teamOneTextColor = 'white'
    teamTwoTextColor = 'white'
    if(are_colors_too_similar(teamOneColor, teamTwoColor)):
        teamTwoColor = logo_colors[df["Team"][1]]['secondary']
        print('similar')
    if(are_colors_too_similar(teamOneColor,'#FFFFFF', threshold=35)):
        teamOneTextColor = 'black'
    if(are_colors_too_similar(teamTwoColor,'#FFFFFF', threshold=35)):
        teamTwoTextColor = 'black'
    
    # Adjust the bars to ensure they are centered and properly layered
    bar_height = 0.3
        
    lineThickness = 2 #1.5 small -- 2.5 large
    ax.barh(0, team_a_ratio, color=teamOneColor, edgecolor='black', linewidth=lineThickness, height=bar_height, align='center')
    ax.barh(0, team_b_ratio, left=team_a_ratio, color=teamTwoColor, edgecolor='black', linewidth=lineThickness, height=bar_height, align='center')
 
    ax.set_xlim(-0.01, 1.01)
    # ax.set_ylim(-1, 1)
    # Center the bars by adjusting x-limits
    # ax.set_xlim(0, total)

    # Add annotations
    ax.text(team_a_ratio / 2, 0, f'${team_a_spending:,}', ha='center', va='center', color=teamOneTextColor, fontweight='bold', fontproperties=font_body)
    ax.text(team_a_ratio + team_b_ratio / 2, 0, f'${team_b_spending:,}', ha='center', va='center', color=teamTwoTextColor, fontweight='bold', fontproperties=font_body)

    # Customize plot
    ax.set_yticks([])
    ax.set_xticks([])
    ax.axis('off')

    # Text subplot
    ax_text = fig.add_subplot(gs[4])
    ax_text.axis('off')

        # Add text underneath the bar graph
    heading = 'Top 3 Bench Expenses'
    subText = '(Time Spent on Bench)'
    team_a_players = df['Players'][0]
    team_b_players = df['Players'][1]

    team_a_bench = df['BenchMin'][0]
    team_b_bench = df['BenchMin'][1]

    x_pos_A = 0.07
    y_start_A = 0.63
    
    x_pos_B = 0.93
    y_start_B = 0.63

    y_step = 0.25
    renderer = ax_text.figure.canvas.get_renderer()

    for i in range(3):
        playerA = team_a_ids[i]
        playerB = team_b_ids[i]
        img_url_a = f"https://ak-static.cms.nba.com/wp-content/uploads/headshots/nba/latest/260x190/{playerA}.png"
        img_url_b = f"https://ak-static.cms.nba.com/wp-content/uploads/headshots/nba/latest/260x190/{playerB}.png"
        playerA_fileName = f"teamA_{i}.png"
        playerB_fileName = f"teamB_{i}.png"
        playerA = download_image(img_url_a, playerA_fileName)
        playerB = download_image(img_url_b, playerB_fileName)

        playerA = crop_top(playerA)
        playerB = crop_top(playerB)

        # Image for Team A
        imageboxA = OffsetImage(playerA, zoom=0.28)
        ab_A = AnnotationBbox(imageboxA, (x_pos_A, y_start_A - i * y_step), frameon=False)
        ax_text.add_artist(ab_A)

        # Image for Team B
        imageboxB = OffsetImage(playerB, zoom=0.28)
        ab_B = AnnotationBbox(imageboxB, (x_pos_B, y_start_B - i * y_step), frameon=False)
        ax_text.add_artist(ab_B)

        # Dynamically adjust the font size for player names
        name_font_a = get_dynamic_font_size(team_a_players[i], 0.82, font_names.copy(), renderer, fig)
        name_font_b = get_dynamic_font_size(team_b_players[i], 0.82, font_names.copy(), renderer, fig)

        # Calculate text width for right-aligned text
        fig_width_in_pixels = fig.get_size_inches()[0] * fig.dpi
        player_a_name_width = renderer.get_text_width_height_descent(f"{team_a_players[i]}", name_font_a, False)[0]
        player_a_money_width = renderer.get_text_width_height_descent(f"{team_a_money[i]}", font_money, False)[0]
        player_a_bench_width = renderer.get_text_width_height_descent(f"{team_a_bench[i]}", font_minutes, False)[0]

        player_b_name_width = renderer.get_text_width_height_descent(f"{team_b_players[i]}", name_font_b, False)[0]
        player_b_money_width = renderer.get_text_width_height_descent(f"{team_b_money[i]}", font_money, False)[0]
        player_b_bench_width = renderer.get_text_width_height_descent(f"{team_b_bench[i]}", font_minutes, False)[0]

        player_a_name_width_fraction = player_a_name_width / fig_width_in_pixels
        player_a_money_width_fraction = player_a_money_width / fig_width_in_pixels
        player_a_bench_width_fraction = player_a_bench_width / fig_width_in_pixels

        player_b_name_width_fraction = player_b_name_width / fig_width_in_pixels
        player_b_money_width_fraction = player_b_money_width / fig_width_in_pixels
        player_b_bench_width_fraction = player_b_bench_width / fig_width_in_pixels

        offset = 0.05  # Increased this value to move the text further right

        # Adjust y position offsets for Team A (center-aligned)
        ax_text.text(x_pos_A + 0.13, y_start_A - i * y_step, f"{team_a_players[i]}", va='center', ha='center', color='black', fontproperties=name_font_a)
        ax_text.text(x_pos_A + 0.29, y_start_A - i * y_step + 0.02, f"{team_a_money[i]}", va='center', ha='center', color='black', fontproperties=font_money)
        ax_text.text(x_pos_A + 0.293, y_start_A - i * y_step - 0.04, f"{team_a_bench[i]}", va='center', ha='center', color='black', fontproperties=font_minutes)

        # Adjust y position offsets for Team B (center-aligned)
        ax_text.text(x_pos_B - 0.08 - player_b_name_width_fraction - offset, y_start_B - i * y_step, f"{team_b_players[i]}", va='center', ha='left', color='black', fontproperties=name_font_b)
        ax_text.text(x_pos_B - 0.24 - player_b_money_width_fraction - offset, y_start_B - i * y_step + 0.02, f"{team_b_money[i]}", va='center', ha='left', color='black', fontproperties=font_money)
        ax_text.text(x_pos_B - 0.237 - player_b_bench_width_fraction - offset, y_start_B - i * y_step - 0.04, f"{team_b_bench[i]}", va='center', ha='left', color='black', fontproperties=font_minutes)

    
   

















   
    #add a vertical line between the y_start_A and y_start_B
    #add here
    x_mid = (x_pos_A + x_pos_B) / 2

    # Add the vertical line
    ax_text.axvline(x=x_mid, ymin=0.05, ymax=0.7, color='black', linestyle='--', linewidth=1)
    
   
    # Add heading
    ax_text.text(0.5, 0.97, heading, ha='center', va='top', fontproperties=font_heading)
    ax_text.text(0.5, 0.87, subText, ha='center', va='top', fontproperties=font_subText)



    # Adjust layout to increase space between subplots
    plt.subplots_adjust(hspace=0.3)  # Decrease horizontal space between subplots

    # Save the figure with a specific size
    output_size = (2300, 3300)  # Width and height in pixels
    dpi = 300
    fig.set_size_inches(output_size[0] / dpi, output_size[1] / dpi)

    saveName = f'{df["Team"][0]}_vs_{df["Team"][1]}'
    outputDir = f'/Users/twelckle/Documents/GitHub/Bench_Money_NBA/Images/{dateSave}'
    if not os.path.exists(outputDir):
        os.makedirs(outputDir)
    
    savePath = os.path.join(outputDir, saveName)
    plt.savefig(savePath, dpi=dpi, bbox_inches='tight', pad_inches=0.1)
    plt.close(fig)
    return savePath
    