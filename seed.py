from core.database import StorageManager
db = StorageManager("database.json")
phy = db.list_items("physics")
print(phy["a1b2c3d4"])