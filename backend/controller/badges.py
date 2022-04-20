import os
import shutil
import tempfile

from fpdf import FPDF
import numpy as np
from PIL import Image, ImageColor, ImageDraw, ImageFont
from more_itertools import grouper

import settings

THIS_DIR = os.path.dirname(os.path.realpath(__file__))
BASE_IMAGE = os.path.join(os.path.dirname(THIS_DIR), "data", "badge-2022.png")
DIAMETER = 50  # mm
X_JUMP = DIAMETER + 2
Y_JUMP = DIAMETER - 3
SHIFT = 25
BLACK = 0, 0, 0
WHITE = 255, 255, 255

FONT = "calibri.ttf"
color_pair_index = 0
COLOR_PAIRS = (
    ("#949398", "#F4DF4E"), ("#FC766A", "#5B84B1"), ("#E69A8D", "#5F4B8B"), ("#FFFFFF", "#000000"),
    ("#F95700", "#00A4CC"), ("#00203F", "#ADEFD1"), ("#D6ED17", "#606060"), ("#2C5F2D", "#97BC62"),
    ("#EEA47F", "#00539C"), ("#0063B2", "#9CC3D5"), ("#EA738D", "#CBCE91"), ("#B1624E", "#5CC8D7"),
    ("#89ABE3", "#FCF6F5"), ("#F2AA4C", "#101820"), ("#195190", "#A2A2A1"), ("#603F83", "#C7D3D4"),
    ("#2BAE65", "#FCF6F5"), ("#6E6E6D", "#FAD0C9"), ("#2D2926", "#E94B3C"), ("#DAA03D", "#616247"),
    ("#990011", "#FCF6F5"), ("#76528B", "#CBCE91"), ("#FAEBEF", "#333D79"), ("#FDD20E", "#F93822"),
    ("#F2EDD7", "#755139"), ("#006B38", "#101820"), ("#FFFFFF", "#F95700"), ("#00539C", "#FFD662"),
    ("#2C5F2D", "#FFE77A"), ("#D01C1F", "#4B878B"), ("#1C1C1B", "#CE4A7E"), ("#00B1D2", "#FDDB27"),
    ("#A13941", "#BD7F37"), ("#E10600", "#00239C"), ("#90AFC5", "#2A3132"), ("#46211A", "#BA5536"),
    ("#68829E", "#505160"), ("#7D4427", "#2E4600"), ("#021C1E", "#2C7873"), ("#375E97", "#FB6542"),
    ("#4CB5F5", "#34675C"), ("#DE7A22", "#20948B"), ("#8D230F", "#1E434C"), ("#BCBABE", "#1995AD"),
    ("#E6DF44", "#011A27")
)


def replace_color(image: str, from_color: tuple, to_color: tuple):
    """
    Credits https://stackoverflow.com/a/17310029/7709964
    Args:
        image: path to the image to edit. Attention the image will be overwritten
        from_color: source color (rgb)
        to_color: target color (rgb
    """
    im = Image.open(image)
    im = im.convert('RGBA')
    data = np.array(im)

    r1, g1, b1 = from_color
    a1 = 255
    r2, g2, b2 = to_color
    a2 = 255  # when do not want it to be transparent

    red, green, blue, alpha = data[:, :, 0], data[:, :, 1], data[:, :, 2], data[:, :, 3]
    mask = (red == r1) & (green == g1) & (blue == b1) & (alpha == a1)
    data[:, :, :4][mask] = [r2, g2, b2, a2]

    im = Image.fromarray(data)
    im.save(image)


def create_design(name: str, colors=None):
    global color_pair_index
    tmpdir = tempfile.gettempdir()
    path = os.path.join(tmpdir, f"badge-{name}.png")
    shutil.copyfile(BASE_IMAGE, path)
    if colors:
        foreground_color = ImageColor.getcolor(colors[0], "RGB")
        background_color = ImageColor.getcolor(colors[1], "RGB")
    else:
        foreground_color = ImageColor.getcolor(COLOR_PAIRS[color_pair_index][0], "RGB")
        background_color = ImageColor.getcolor(COLOR_PAIRS[color_pair_index][1], "RGB")
    replace_color(path, WHITE, foreground_color)
    replace_color(path, BLACK, background_color)
    color_pair_index += 1
    if color_pair_index % len(COLOR_PAIRS) == 0:
        color_pair_index = 0
    return path, foreground_color


def add_team_id(image: str, team_id: str, text_color: tuple, index=0):
    """
    Credits https://stackoverflow.com/a/1970930/7709964
            https://stackoverflow.com/a/4902713/7709964
    Args:
        image: path to the source image
        team_id: the text to be added to the badge
        text_color: text foreground color (r,g,b)
        index: this value is used to name the target file
            it must be different every time the function is called if the team_id is the same

    Returns:

    """
    tmpdir = tempfile.gettempdir()
    path = os.path.join(tmpdir, f"badge-{team_id}-{index}.png")

    im = Image.open(image)
    im = im.convert('RGBA')
    W, H = im.size
    draw = ImageDraw.Draw(im)
    fontsize = 200  # starting font size

    # portion of image width you want text width to be
    img_fraction = 0.25

    font = ImageFont.truetype(FONT, fontsize)
    while font.getsize(team_id)[0] < img_fraction * im.size[0]:
        # iterate until the text size is just larger than the criteria
        fontsize += 1
        font = ImageFont.truetype(FONT, fontsize)
        if fontsize > 1000:
            raise Exception("starting font size is likely too high")

    # optionally de-increment to be sure it is less than criteria
    fontsize -= 1
    font = ImageFont.truetype(FONT, fontsize)

    w, h = draw.textsize(team_id, font=font)
    draw.text(((W-w)/2, (H-h)/3*2), team_id, font=font, fill=text_color)

    im.save(path, "PNG")
    return path


def create_pdf(badges: list, pdf_path):
    """
    Create a pdf with all the badges positioned in an optimized way
    Args:
        badges: a list of path to final badge images (colors + team id included)
                One path per player
        pdf_path: path were to write the pdf
    """
    # The badges are created by group of 6.
    # If the list of images is < 6, the list is stuff with template badges
    if len(badges) % 6 != 0:
        for i in range(6 - len(badges) % 6):
            badge, _ = create_design(f"empty-{i}")
            badges.append(badge)

    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.set_top_margin(7)
    pdf.add_page()

    for chunk in grouper(badges, 6):
        print(f"Generating page {pdf.page_no()}...")
        pdf.image(chunk[0], w=DIAMETER, h=DIAMETER)
        x = pdf.get_x()
        y = pdf.get_y() - DIAMETER
        pdf.image(chunk[1], w=DIAMETER, h=DIAMETER, x=x + X_JUMP, y=y)
        pdf.image(chunk[2], w=DIAMETER, h=DIAMETER, x=x + 2 * X_JUMP, y=y)
        pdf.image(chunk[3], w=DIAMETER, h=DIAMETER, x=x+SHIFT, y=y + Y_JUMP)
        pdf.image(chunk[4], w=DIAMETER, h=DIAMETER, x=x + X_JUMP + SHIFT, y=y + Y_JUMP)
        pdf.image(chunk[5], w=DIAMETER, h=DIAMETER, x=x + 2 * X_JUMP + SHIFT, y=y + Y_JUMP)
        pdf.set_y(y + 2 * Y_JUMP)

    pdf.output(pdf_path)


def generate_badges(db, target_pdf_path):
    badge_list = list()
    for section in db.collection(settings.firestore.sections_collection).stream():
        section_name = section.to_dict()["name"]
        section_nb_teams = section.to_dict()["nbTeams"]
        if not section_nb_teams:
            print(f"Skipping {section_name}, they are not players")
        print("Generating badges for {}".format(section_name))
        colored_badge, color = create_design(section.id)
        for team in db.collection(settings.firestore.teams_collection).order_by("id").where('sectionId', '==', section.id).stream():
            nb_players = team.to_dict()["nbPlayers"]
            team_badge = add_team_id(colored_badge, team.id, color)
            for i in range(nb_players):
                badge_list.append(team_badge)
    print("Let's put all this in a pdf")
    create_pdf(badge_list, target_pdf_path)
    print("Done!")


def generate_missing_badges(sections, target_pdf_path):
    """
    Generate the badge for section who added players after the deadline
    Args:
        sections: a list made of dict with the following keys: teams (list), colors (list), amount (int)
        target_pdf_path: target file
    """
    badge_list = list()
    for sectionId, section in enumerate(sections):
        colored_badge, color = create_design(str(sectionId), section["colors"])
        for teamId in section["teams"]:
            print("Generating badges for {}".format(teamId))
            team_badge = add_team_id(colored_badge, teamId, color)
            for i in range(section["amount"]):
                badge_list.append(team_badge)
    print("Let's put all this in a pdf")
    create_pdf(badge_list, target_pdf_path)
    print("Done!")


def generate_team_bb_badges(nb_design, nb_badge_per_design, target_pdf_path):
    """
    Generate the badge for section who added players after the deadline
    Args:
        nb_design: amount of different designs (int)
        nb_badge_per_design: amount of badge per designs (int)
        target_pdf_path: target file
    """
    badge_list = list()
    for design in range(nb_design):
        colored_badge, color = create_design(str(design))
        print("Generating badges {}".format(design))
        team_badge = add_team_id(colored_badge, "STAFF", color, design)
        for badge in range(nb_badge_per_design):
            badge_list.append(team_badge)
    print("Let's put all this in a pdf")
    create_pdf(badge_list, target_pdf_path)
    print("Done!")

