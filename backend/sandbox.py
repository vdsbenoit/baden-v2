import controller.initialization
import main
import settings

settings.parse()
db = main.init_db()


CSV_PATH = "repartition2022.csv"
controller.initialization.create_new_db(db, 17, CSV_PATH)
