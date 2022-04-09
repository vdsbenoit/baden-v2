import controller.initialization
import main
import settings
from controller.badges import generate_badges

settings.parse()
db = main.init_db()


CSV_PATH = "data/repartition2022.csv"
# controller.initialization.create_new_db(db, 17, CSV_PATH)

generate_badges(db, "badges.pdf")
