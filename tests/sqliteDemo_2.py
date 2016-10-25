#!/usr/bin/python

import sqlite3

conn = sqlite3.connect('test.db')
print "Opened database successfully"

# conn.execute('''INSERT INTO messages (id, createAt, source, hum,
#   temp_01, temp_02, temp_03, temp_04, temp_05, temp_06, temp_07, temp_08,
#   temp_09, temp_10, temp_11, temp_12, temp_13, temp_14, temp_15, temp_16,
#   quat_w, quat_x, quat_y, quat_z,
#   temp_s, hum_s) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''')
# conn.execute(
#     "INSERT INTO messages (id, createAt, source, temp_01, temp_02, temp_03, temp_04, temp_05,temp_06,temp_07,temp_08,temp_09 ,temp_10,temp_11,temp_12,temp_13,temp_14,temp_15,temp_16,hum,quat_w,quat_x ,quat_y ,quat_z,temp_s,hum_s) VALUES (2, 'Allen', 25, 'Texas', 15000.00 )")
# conn.execute(
#     "INSERT INTO messages (id, createAt, source, temp_01, temp_02, temp_03, temp_04, temp_05,temp_06,temp_07,temp_08,temp_09 ,temp_10,temp_11,temp_12,temp_13,temp_14,temp_15,temp_16,hum,quat_w,quat_x ,quat_y ,quat_z,temp_s,hum_s) VALUES (3, 'Teddy', 23, 'Norway', 20000.00 )")
# conn.execute(
#     "INSERT INTO messages (id, createAt, source, temp_01, temp_02, temp_03, temp_04, temp_05,temp_06,temp_07,temp_08,temp_09 ,temp_10,temp_11,temp_12,temp_13,temp_14,temp_15,temp_16,hum,quat_w,quat_x ,quat_y ,quat_z,temp_s,hum_s) VALUES (4, 'Mark', 25, 'Rich-Mond ', 65000.00 )")

conn.commit()

print "Records created successfully"

conn.close()
