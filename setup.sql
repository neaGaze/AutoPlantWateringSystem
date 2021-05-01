use WateringSystem;
create table IF NOT EXISTS Plant(
	plant_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    plant_name varchar(128),
    plant_type varchar(128)
    );

create table IF NOT EXISTS Channel (
	channel_id INT NOT NULL PRIMARY KEY,
    plant_id INT NOT NULL,
    water_start_trigger double,
    water_end_trigger double,
    foreign key(plant_id)  REFERENCES Plant (plant_id)
        ON UPDATE RESTRICT ON DELETE CASCADE
);


create table IF NOT EXISTS Activity(
	activity_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    transaction_id INT,
    created_at datetime,
    channel_id INT,
    activity_type varchar(100),
    foreign key(channel_id)  REFERENCES Channel (channel_id)
        ON UPDATE RESTRICT ON DELETE CASCADE
);

# INSERT PLANT
INSERT INTO Plant(plant_name, plant_type) VALUES ("Flame Tree (Tall)", "Tropical");
INSERT INTO Plant(plant_name, plant_type) VALUES ("Assorted Jade Trees", "Tropical");
INSERT INTO Plant(plant_name, plant_type) VALUES ("Colorado Blue Spruces", "Tundra");
INSERT INTO Plant(plant_name, plant_type) VALUES ("Black Spruce", "Tundra");
INSERT INTO Plant(plant_name, plant_type) VALUES ("Apple Trees", "Alpine");
INSERT INTO Plant(plant_name, plant_type) VALUES ("Pomegranate Tree", "Decidious");
INSERT INTO Plant(plant_name, plant_type) VALUES ("Aloe Vera", "Desert");
INSERT INTO Plant(plant_name, plant_type) VALUES ("Lavender", "Perennial/Desert");

# INERT INTO Channel
INSERT INTO Channel(channel_id, plant_id, water_start_trigger, water_end_trigger) 
	VALUES (1, 17, 2.5, 2.0);
INSERT INTO Channel(channel_id, plant_id, water_start_trigger, water_end_trigger) 
	VALUES (2, 18, 3.0, 2.75);
INSERT INTO Channel(channel_id, plant_id, water_start_trigger, water_end_trigger) 
	VALUES (3, 19, 2.0, 1.60);
INSERT INTO Channel(channel_id, plant_id, water_start_trigger, water_end_trigger) 
	VALUES (4, 20, 3.0, 2.75);

# insert Activity
#INSERT INTO Channel(channel_id, plant_id, water_start_trigger, water_end_trigger) 
#	VALUES (1, 1, "2021-04-26 19:59:00", "2021-04-26 19:59:30");