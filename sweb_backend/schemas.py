from marshmallow_sqlalchemy import SQLAlchemyAutoSchema


class Tree(SQLAlchemyAutoSchema):
    class Meta:
        fields = (
            "BaumNr",
            "BaumID",
            "Pflanzreihe",
            "PflanzreihePosition",
            "SortenID",
            "Sorte",
            "Frucht",
            "PatenID",
            "Longitude",
            "Latitude",
        )


class Sorts(SQLAlchemyAutoSchema):
    class Meta:
        fields = (
            "id",

            "frucht",
            "sorte",
            "andereNamen",
            "herkunft",
            "groesse",
            "beschreibung",

            "reifezeit",
            "lager",
            "lagerfaehigkeit",

            "geschmack",
            "geschmackID",

            "verbreitung",
            "verwendung",

            # Boolean fruit usage fields
            "tafelobst",
            "essen",
            "trinken",
        )


class Treecoordinates(SQLAlchemyAutoSchema):
    class Meta:
        fields = ("BaumNr", "Longitude", "Latitude")


class Admin(SQLAlchemyAutoSchema):
    class Meta:
        fields = ("id", "email")


class Image(SQLAlchemyAutoSchema):
    class Meta:
        fields = ("id", "uri")
