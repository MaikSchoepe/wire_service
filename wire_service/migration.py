from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.sql import text

from wire_service.persistency.connection import DbConnection
from wire_service.persistency.model.area import AreaDb
from wire_service.persistency.model.cable import CableDb
from wire_service.persistency.model.cable_type import CableTypeDb
from wire_service.persistency.model.face import FaceDb
from wire_service.persistency.model.outlet import OutletDb, OutletKind
from wire_service.persistency.model.place import PlaceDb
from wire_service.settings import settings

OUTLET_KIND_MATCH = {
    "Dose1fach": OutletKind.SINGLE,
    "Dose2fach": OutletKind.DOUBLE,
    "Misc": OutletKind.OTHER,
}

CABLE_MATCH = {
    "NYM-J 3x1,5": "NYM-J 3x1,5",
    "NYM-J 4x1,5": "NYM-J 4x1,5",
    "NYM-J 5x1,5": "NYM-J 5x1,5",
    "NYM-J 5x2,5": "NYM-J 5x2,5",
    "NYM-O 3x1,5": "NYM-O 3x1,5",
    "NYM-O 4x1,5": "NYM-O 4x1,5",
    "NYM-O 7x1,5": "NYM-O 7x1,5",
    "KNX": "KNX",
    "1-Wire": "1Wire",
    "Reed": "Reed",
    "Brandmeldekabel": "Brandmelde",
    "CAT7": "CAT7",
    "Sound": "Audio",
    "SAT": "SAT",
    "Telefon": "Telefon",
}


class Migration:
    def migrate(self):
        with DbConnection.Session.begin() as new:
            old_db = create_engine(settings.OLD_DB_PATH, echo=False, future=True)
            self.old = Session(old_db)
            self.new = new
            self.migrate_areas()
            self.migrate_wirings()

    def migrate_areas(self):
        sql = text("SELECT * FROM area;")
        all_areas = self.old.execute(sql)

        for a in all_areas:
            new_area = self.new.query(AreaDb).filter_by(name=a["name"]).first()
            if new_area is None:
                print(f'migrating area {a["name"]}')
                new_area = AreaDb(
                    name=a["name"], short_name=a["short_name"], description=""
                )
                self.new.add(new_area)
            else:
                print(f'area {a["name"]} already present')

            self.migrate_places(a, new_area)

    def migrate_places(self, old_area, new_area):
        sql = text("SELECT * FROM places AS p WHERE p.area_id=:area_uid;").bindparams(
            area_uid=old_area["uid"]
        )
        all_places = self.old.execute(sql)

        for p in all_places:
            new_place = self.new.query(PlaceDb).filter_by(name=p["name"]).first()
            if new_place is None:
                print(f'migrating place {p["name"]}')
                new_place = PlaceDb(
                    name=p["name"], short_name=p["id"], description=p["description"]
                )
                new_area.places.append(new_place)
            else:
                print(f'place {p["name"]} already present')

            self.create_faces(p, new_place)

    def create_faces(self, old_place, new_place):
        sql = text(
            "SELECT wall_direction FROM outlets AS o WHERE o.place_uid=:place_uid GROUP BY wall_direction ORDER BY o.no_in_room;"
        ).bindparams(place_uid=old_place["uid"])
        all_directions = self.old.execute(sql)
        for d, index in zip(all_directions, range(10, 1000, 10)):
            wd = d["wall_direction"]
            new_face = (
                self.new.query(FaceDb).filter_by(place_id=new_place.id, name=wd).first()
            )
            if new_face is None:
                print(f"creating face {wd}")
                new_face = FaceDb(
                    name=wd,
                    short_name=new_place.short_name + "." + wd[0],
                    description="",
                    order_index=index,
                    height=290,
                    width=400,
                )
                new_place.faces.append(new_face)
            else:
                print(f"face {wd} already present")

            self.migrate_outlets(old_place, new_face)

    def migrate_outlets(self, old_place, new_face):
        sql = text(
            "SELECT * FROM outlets AS o WHERE o.place_uid=:place_uid AND o.wall_direction=:wall_direction ORDER BY o.no_in_room;"
        ).bindparams(place_uid=old_place["uid"], wall_direction=new_face.name)
        all_outlets = self.old.execute(sql)
        for o in all_outlets:
            outlet_short_name = new_face.short_name + "." + str(o["no_in_room"])
            new_outlet = (
                self.new.query(OutletDb)
                .filter_by(face_id=new_face.id, short_name=outlet_short_name)
                .first()
            )
            if new_outlet is None:
                print(f"migrating outlet {o}")
                new_outlet = OutletDb(
                    short_name=outlet_short_name,
                    name=o["comment"] or outlet_short_name,
                    description=o["vertical_position"],
                    kind=OUTLET_KIND_MATCH[o["type"]],
                )
                new_face.outlets.append(new_outlet)
            else:
                print(f"outlet {o} already present")

    def migrate_wirings(self):
        cable_match = {}
        for k, v in CABLE_MATCH.items():
            cable_match[k] = self.new.query(CableTypeDb).filter_by(name=v).first()

        sql = text(
            "SELECT "
            "p1.id AS place1, o1.wall_direction AS wd1, o1.no_in_room as no1, "
            "p2.id AS place2, o2.wall_direction AS wd2, o2.no_in_room as no2, "
            "wire_type, w.uid as uid "
            "FROM wirings AS w "
            "INNER JOIN outlets AS o1 ON w.start_uid=o1.uid "
            "INNER JOIN outlets AS o2 ON w.end_uid=o2.uid "
            "INNER JOIN places AS p1 ON o1.place_uid=p1.uid "
            "INNER JOIN places AS p2 ON o2.place_uid=p2.uid "
        )
        all_wirings = self.old.execute(sql)
        for w in all_wirings:
            print(f'adding cable {w["uid"]}')
            start_short_name = w["place1"] + "." + w["wd1"][0] + "." + str(w["no1"])
            end_short_name = w["place2"] + "." + w["wd2"][0] + "." + str(w["no2"])
            start = (
                self.new.query(OutletDb).filter_by(short_name=start_short_name).first()
            )
            end = self.new.query(OutletDb).filter_by(short_name=end_short_name).first()
            ct = cable_match[w["wire_type"]]
            new_cable = CableDb()
            new_cable.start_outlet = start
            new_cable.end_outlet = end
            new_cable.cable_type = ct
            self.new.add(new_cable)


Migration().migrate()
