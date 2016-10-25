CREATE TABLE IF NOT EXISTS messages (
    ts INTEGER PRIMARY KEY DESC,
    
    hum REAL,
    
    temp_01 REAL,
    temp_02 REAL,
    temp_03 REAL,
    temp_04 REAL,
    temp_05 REAL,
    temp_06 REAL,
    temp_07 REAL,
    temp_08 REAL,
    temp_09 REAL,
    temp_10 REAL,
    temp_11 REAL,
    temp_12 REAL,
    temp_13 REAL,
    temp_14 REAL,
    temp_15 REAL,
    temp_16 REAL,

    quat_w REAL,
    quat_x REAL,
    quat_y REAL,
    quat_z REAL,

    hum_s REAL,
    light_s REAL,
    temp_s REAL
);