import settings


def print_stats_section(db, section_id, reporter_city):
    reported_by_city = {"win": 0, "loss": 0, "draw": 0}
    not_reported_by_city = {"win": 0, "loss": 0, "draw": 0}
    for match in db.collection(settings.firestore.matches_collection).stream():
        m = match.to_dict()
        reporter = m["reporter"]
        if not reporter:
            continue
        reporter_section = db.collection(settings.firestore.profiles_collection).document(reporter).get().to_dict()[
            "sectionId"]
        if not reporter_section:
            print(f"Reporter {reporter} has no section")
            continue
        reporter_city = \
        db.collection(settings.firestore.sections_collection).document(reporter_section).get().to_dict()["city"]
        if m["draw"]:
            players = m["player_ids"]
            p0_section = db.collection(settings.firestore.teams_collection).document(players[0]).get().to_dict()[
                "sectionId"]
            p1_section = db.collection(settings.firestore.teams_collection).document(players[1]).get().to_dict()[
                "sectionId"]
            if p0_section == section_id or p1_section == section_id:
                if reporter_city == reporter_city:
                    reported_by_city["draw"] += 1
                else:
                    not_reported_by_city["draw"] += 1
        else:
            winner_section = db.collection(settings.firestore.teams_collection).document(m["winner"]).get().to_dict()[
                "sectionId"]
            loser_section = db.collection(settings.firestore.teams_collection).document(m["loser"]).get().to_dict()[
                "sectionId"]
            if winner_section == section_id:
                if reporter_city == reporter_city:
                    reported_by_city["win"] += 1
                else:
                    not_reported_by_city["win"] += 1
            if loser_section == section_id:
                if reporter_city == reporter_city:
                    reported_by_city["loss"] += 1
                else:
                    not_reported_by_city["loss"] += 1

    print(f"Reported by {reporter_city}")
    print(reported_by_city)
    print(f"Not reported by {reporter_city}")
    print(not_reported_by_city)


def print_stats_city(db, city):
    reported_by_city = {"win": 0, "loss": 0, "draw": 0}
    not_reported_by_city = {"win": 0, "loss": 0, "draw": 0}
    for match in db.collection(settings.firestore.matches_collection).stream():
        m = match.to_dict()
        reporter = m["reporter"]
        if not reporter:
            continue
        reporter_section = db.collection(settings.firestore.profiles_collection).document(reporter).get().to_dict()["sectionId"]
        if not reporter_section:
            print(f"Reporter {reporter} has no section")
            continue
        reporter_city = db.collection(settings.firestore.sections_collection).document(reporter_section).get().to_dict()["city"]
        if m["draw"]:
            players = m["player_ids"]
            p0_city = db.collection(settings.firestore.teams_collection).document(players[0]).get().to_dict()["city"]
            p1_city = db.collection(settings.firestore.teams_collection).document(players[1]).get().to_dict()["city"]
            if p0_city == city or p1_city == city:
                if reporter_city == city:
                    reported_by_city["draw"] += 1
                else:
                    not_reported_by_city["draw"] += 1
        else:
            winner_city = db.collection(settings.firestore.teams_collection).document(m["winner"]).get().to_dict()["city"]
            loser_city = db.collection(settings.firestore.teams_collection).document(m["loser"]).get().to_dict()["city"]
            if winner_city == city:
                if reporter_city == city:
                    reported_by_city["win"] += 1
                else:
                    not_reported_by_city["win"] += 1
            if loser_city == city:
                if reporter_city == city:
                    reported_by_city["loss"] += 1
                else:
                    not_reported_by_city["loss"] += 1

    print("reporter_from_soignies")
    print(reported_by_city)
    print("reporter_not_soignies")
    print(not_reported_by_city)
