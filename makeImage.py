import matplotlib.pyplot as plt
import pandas as pd
from PIL import Image
import io
import cairosvg
from matplotlib.gridspec import GridSpec
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

logo_colors = {
    'ATL': '#cc0033',  # Atlanta Hawks
    'BKN': '#343434',  # Brooklyn Nets (adjusted for better contrast)
    'BOS': '#007A33',  # Boston Celtics
    'CHA': '#1D1160',  # Charlotte Hornets
    'CHI': '#CE1141',  # Chicago Bulls
    'CLE': '#6F263D',  # Cleveland Cavaliers (adjusted for uniqueness)
    'DAL': '#007DC5',  # Dallas Mavericks (adjusted for better contrast and uniqueness)
    'DEN': '#041E42',  # Denver Nuggets (adjusted for better contrast)
    'DET': '#C8102E',  # Detroit Pistons
    'GSW': '#FDB927',  # Golden State Warriors (adjusted for better contrast)
    'HOU': '#CE1141',  # Houston Rockets
    'IND': '#FFC633',  # Indiana Pacers (adjusted for better contrast)
    'LAC': '#ED174C',  # LA Clippers (adjusted for better contrast)
    'LAL': '#552583',  # Los Angeles Lakers
    'MEM': '#6189B9',  # Memphis Grizzlies (adjusted for better contrast)
    'MIA': '#98002E',  # Miami Heat
    'MIL': '#00471B',  # Milwaukee Bucks
    'MIN': '#236192',  # Minnesota Timberwolves (adjusted for uniqueness)
    'NOP': '#B4975A',  # New Orleans Pelicans (adjusted for better contrast)
    'NYK': '#F58426',  # New York Knicks (adjusted for better contrast)
    'OKC': '#EF3B24',  # Oklahoma City Thunder (adjusted for better contrast)
    'ORL': '#0077C0',  # Orlando Magic
    'PHI': '#ED174C',  # Philadelphia 76ers (adjusted for uniqueness)
    'PHX': '#E56020',  # Phoenix Suns (adjusted for better contrast)
    'POR': '#E03A3E',  # Portland Trail Blazers
    'SAC': '#5A2D81',  # Sacramento Kings
    'SAS': '#2B2B2B',  # San Antonio Spurs (darker color)
    'TOR': '#A6192E',  # Toronto Raptors (adjusted for uniqueness)
    'UTA': '#00471B',  # Utah Jazz
    'WAS': '#002B5C',  # Washington Wizards
}

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

def make_image(data):
    df = pd.DataFrame(data)

    # Data
    total_spending = df['Spending'].sum()
    team_a_spending = df['Spending'][0]
    team_b_spending = df['Spending'][1]
    date = df['Date'].iloc[0]

    # Calculate the proportion of spending
    team_a_ratio = team_a_spending / total_spending
    team_b_ratio = team_b_spending / total_spending

    font_title = {'family': 'Arial Black', 'weight': 'bold', 'size': 16}
    font_heading = {'family': 'Arial Black', 'weight': 'bold', 'size': 12}
    font_score = {'family': 'Arial Black', 'weight': 'bold', 'size': 15}
    font_body = {'family': 'Arial Black', 'size': 10}

    

    # Create the plot with GridSpec
    fig = plt.figure(figsize=(12, 10), facecolor='#c9c9c9')  # Set the background color and figure size here
    gs = GridSpec(6, 1, height_ratios=[0.1, 0.08, 0.03, 0.25, 0.10, 0.30])  # Adjust height ratios

    # Create an axis to place the main logo
    logo_ax = fig.add_subplot(gs[0])
    logo_ax.axis('off')  # Hide the axes for the logo

    # Place the main logo in the top left corner
    place_logo(logo_ax, './nba_logos/logo.png', zoom=0.08, position=(0, 0.9))  # Adjust zoom and position to place the main logo in the top left corner

    # Add date to the top right corner
    logo_ax.text(0.99, 0.3, date, ha='right', va='top', fontdict=font_title, transform=logo_ax.transAxes)

    # Title subplot
    title_ax = fig.add_subplot(gs[1])
    title_ax.axis('off')  # Hide the axes for the title
    title = 'Bench Money Spending'
    title_ax.text(0.5, 0.1, title, ha='center', va='center', fontdict=font_title)

    # Score subplot
    score_ax = fig.add_subplot(gs[2])
    score_ax.axis('off')
    team_a_score = df['Score'][0]
    team_b_score = df['Score'][1]

    # Get the coordinates to place the logos
    logo_team_a_x = 0.25
    logo_team_b_x = 0.75

    team_a_color = '#00820d' #green
    team_b_color = '#e62727' #red

    if(team_a_score < team_b_score):
        temp = team_a_color
        team_a_color = team_b_color
        team_b_color = temp

    # Add the scores with respective colors
    score_ax.text(logo_team_a_x, 0.001, str(team_a_score), ha='center', va='bottom', fontdict=font_score, color=team_a_color)
    score_ax.text(logo_team_b_x, 0.001, str(team_b_score), ha='center', va='bottom', fontdict=font_score, color=team_b_color)

    # Logos subplot
    logos_ax = fig.add_subplot(gs[3])
    logos_ax.axis('off')  # Hide the axes for the logos

    # Convert SVG logos to high-resolution PNG
    teama_png = f'./nba_logos/{df["Team"][0]}.svg'
    teamb_png = f'./nba_logos/{df["Team"][1]}.svg'

    logo_team_a = svg_to_png(teama_png, dpi=300)
    logo_team_b = svg_to_png(teamb_png, dpi=300)

    # Convert logos to arrays without resizing
    def get_image(image, zoom=0.3):  # Adjust the zoom to control display size
        return OffsetImage(image, zoom=zoom)  # Adjust zoom to fit the preset image size

    # Place the team logos in the logos subplot
    ab_team_a = AnnotationBbox(get_image(logo_team_a, zoom=0.3), (logo_team_a_x, 0.5), frameon=False, box_alignment=(0.5, 0.5))
    ab_team_b = AnnotationBbox(get_image(logo_team_b, zoom=0.3), (logo_team_b_x, 0.5), frameon=False, box_alignment=(0.5, 0.5))

    logos_ax.add_artist(ab_team_a)
    logos_ax.add_artist(ab_team_b)

    # Bar graph subplot
    ax = fig.add_subplot(gs[4])

    # Centering the bar
    bar_height = 0.3

    # Draw the bar
    total = team_a_ratio + team_b_ratio

    # Adjust the bars to ensure they are centered and properly layered
    ax.barh(0, team_a_ratio, color=logo_colors[df["Team"][0]], edgecolor='none', height=bar_height, align='center')
    ax.barh(0, team_b_ratio, left=team_a_ratio, color=logo_colors[df["Team"][1]], edgecolor='none', height=bar_height, align='center')

    # Center the bars by adjusting x-limits
    ax.set_xlim(0, total)

    # Add annotations
    ax.text(team_a_ratio / 2, 0, f'${team_a_spending:,}', ha='center', va='center', color='white', fontweight='bold', fontdict=font_body)
    ax.text(team_a_ratio + team_b_ratio / 2, 0, f'${team_b_spending:,}', ha='center', va='center', color='white', fontweight='bold', fontdict=font_body)

        # Customize plot
    ax.set_yticks([])
    ax.set_xticks([])
    ax.axis('off')

    # Text subplot
    ax_text = fig.add_subplot(gs[5])
    ax_text.axis('off')  # Hide the axes

        # Add text underneath the bar graph
    heading = 'Top 3 Bench Expenses'
    team_a_players = '\n\n'.join(df['Players'][0])
    team_b_players = '\n\n'.join(df['Players'][1])

    # Add heading
    ax_text.text(0.5, 0.9, heading, ha='center', va='top', fontdict=font_heading)

    # Add bullet points for Team A
    ax_text.text(0.05, 0.60, team_a_players, ha='left', va='top', fontdict=font_body)

    # Add bullet points for Team B
    ax_text.text(0.55, 0.60, team_b_players, ha='left', va='top', fontdict=font_body)

    # Adjust layout to increase space between subplots
    plt.subplots_adjust(hspace=0.3)  # Decrease horizontal space between subplots

    # Save the figure with a specific size
    output_size = (1920, 2700)  # Width and height in pixels
    dpi = 300
    fig.set_size_inches(output_size[0] / dpi, output_size[1] / dpi)

    saveName = f'{df["Team"][0]}_vs_{df["Team"][1]}:{df["Date"][0]}'
    print(saveName)
    plt.savefig(saveName, dpi=dpi, bbox_inches='tight')