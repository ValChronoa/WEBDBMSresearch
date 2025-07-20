from auth.models import User
User('student1', 'pass123', 'user').save()
User('tech_phy',  'te123',   'technician', lab='physics').save()
User('tech_chem', 'tc123',   'technician', lab='chemistry').save()
User('tech_bio',  'tb123',   'technician', lab='biology').save()
User('admin',     'admin123','admin').save()
print('Accounts seeded!')