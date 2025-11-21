import sqlite3

conn = sqlite3.connect('safehome.db')
cursor = conn.cursor()

print("=" * 50)
print("System Settings:")
print("=" * 50)
cursor.execute('SELECT * FROM system_settings')
for row in cursor.fetchall():
    print(f"Setting ID: {row[0]}")
    print(f"Monitoring Phone: {row[1]}")
    print(f"Homeowner Phone: {row[2]}")
    print(f"Lock Time: {row[3]}s")
    print(f"Alarm Delay: {row[4]}s")
    print(f"Updated At: {row[5]}")
    print("-" * 50)

conn.close()
