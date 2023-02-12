from marshmallow_sqlalchemy import SQLAlchemyAutoSchema


class Tree(SQLAlchemyAutoSchema):
    class Meta:
        fields = (
            "BaumNr", "BaumID", "Pflanzreihe", "PflanzreihePosition", "SortenID", "Sorte", "Frucht", "PatenID",
            "Longitude",
            "Latitude")


class Sorts(SQLAlchemyAutoSchema):
    class Meta:
        fields = ("id", "frucht", "sorte", "andereNamen", "herkunft", "groesse", "beschreibung", "reifezeit",
                  "geschmack", "verwendung", "lager", "verbreitung")


class Treecoordinates(SQLAlchemyAutoSchema):
    class Meta:
        fields = ("BaumNr", "Longitude", "Latitude")


class Admin(SQLAlchemyAutoSchema):
    class Meta:
        fields = ("id", "email")


class Image(SQLAlchemyAutoSchema):
    class Meta:
        fields = ("id", "uri")
