CREATE TYPE WEAPON AS ENUM('cz','desert_eagle','dual_berettas','five_seven','glock','p2000','p250','r8','tec9','usp','mag7','nova','sawed_off','xm','mac10','mp5','mp7','mp9','p90','pp_bizon','ump','ak','aug','famas','galil','m4a1s','m4a4','sg','awp','g3sg1','scar','ssg','m249','negev','knife','zeus','he','fire','flash','smoke');
CREATE TABLE Videos(
	Id SERIAL PRIMARY KEY,
	Code VARCHAR(512) NOT NULL,
	Event VARCHAR(64) NULL,
	Map VARCHAR(32) NOT NULL,
	AvgCasting FLOAT CHECK (avgcasting >= 0.0 AND avgcasting <= 5.0),
	AvgSignificance FLOAT CHECK (avgsignificance >= 0.0 AND avgsignificance <= 5.0),
	AvgIntelligence FLOAT CHECK (avgintelligence >= 0.0 AND avgintelligence <= 5.0),
	AvgAtmosphere FLOAT CHECK (avgatmosphere >= 0.0 AND avgatmosphere <= 5.0),
	AvgAim FLOAT CHECK (avgaim >= 0.0 AND avgaim <= 5.0),
	AvgLuck FLOAT CHECK (avgluck >= 0.0 AND avgluck <= 5.0),
	Player VARCHAR(32) NOT NULL,
	Team VARCHAR(64) NULL,
	Grand_final BOOLEAN NOT NULL,
	Armor BOOLEAN NOT NULL,
	Crowd BOOLEAN NOT NULL,
	Kills INT CHECK (kills >= 0 AND kills <= 5),
	Clutch_kills INT CHECK (clutch_kills >= 0 AND clutch_kills <= 5),
	Weapon WEAPON ARRAY NOT NULL
);

INSERT INTO Videos VALUES(
	DEFAULT,
	'<iframe width="560" height="315" src="https://www.youtube.com/embed/AzeuySdai40" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>',
	'PGL Major Krakow 2017',
	'de_inferno',
	3.0,
	3.0,
	5.0,
	4.0,
	1.0,
	3.0,
	'Dosia',
	'Gambit Gaming',
	'1',
	'1',
	'1',
	0,
	0,
	'{"he"}'
);

INSERT INTO Videos VALUES(
	DEFAULT,
	'<iframe width="560" height="315" src="https://www.youtube.com/embed/yJifD2IEgx4" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>',
	'PGL Regional Minor Championship Europe - ELEAGUE Major 2017',
	'de_mirage',
	3.0,
	2.0,
	3.0,
	2.0,
	4.0,
	1.0,
	'BARBARR',
	'Epsilon',
	'0',
	'1',
	'0',
	4,
	4,
	'{"ak"}'
);

INSERT INTO Videos VALUES(
	DEFAULT,
	'<iframe width="560" height="315" src="https://www.youtube.com/embed/1NN1CjhH7rA" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>',
	'ESL One Katowice 2015',
	'de_inferno',
	5.0,
	3.0,
	2.0,
	5.0,
	5.0,
	1.5,
	'friberg',
	'Ninjas in Pyjamas',
	'1',
	'1',
	'1',
	2,
	2,
	'{"ak"}'
);

INSERT INTO Videos VALUES(
	DEFAULT,
	'<iframe width="560" height="315" src="https://www.youtube.com/embed/W9Jbo4Dv7vc" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>',
	'ESL One Cologne 2015',
	'de_dust2',
	4.5,
	5.0,
	2.5,
	4.5,
	5.0,
	2.0,
	'KRIMZ',
	'Fnatic',
	'1',
	'1',
	'1',
	3,
	3,
	'{"ak"}'
);

INSERT INTO Videos VALUES(
	DEFAULT,
	'<iframe width="560" height="315" src="https://www.youtube.com/embed/W9Jbo4Dv7vc" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>',
	'ESL One Cologne 2015',
	'de_dust2',
	5.0,
	4.0,
	3.5,
	5.0,
	1.0,
	2.5,
	'NBK',
	'Team EnVyUs',
	'1',
	'1',
	'1',
	1,
	0,
	'{"knife"}'
);

INSERT INTO Videos VALUES(
	DEFAULT,
	'<iframe width="560" height="315" src="https://www.youtube.com/embed/cjOVXdarUTs" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>',
	'MLG Major Championship: Columbus 2016',
	'de_mirage',
	5.0,
	5.0,
	2.0,
	4.0,
	2.0,
	5.0,
	'coldzera',
	'Luminosity Gaming',
	'0',
	'0',
	'1',
	4,
	0,
	'{"awp"}'
);

INSERT INTO Videos VALUES(
	DEFAULT,
	'<iframe width="560" height="315" src="https://www.youtube.com/embed/kUSN6u5CSRE" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>',
	'ESL One Cologne 2016',
	'de_cache',
	5.0,
	5.0,
	2.0,
	5.0,
	5.0,
	5.0,
	's1mple',
	'Team Liquid',
	'0',
	'1',
	'1',
	2,
	2,
	'{"awp"}'
);

INSERT INTO Videos VALUES(
	DEFAULT,
	'<iframe width="560" height="315" src="https://www.youtube.com/embed/PO1G0bmWurc" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>',
	'ESL One New York 2016',
	'de_dust2',
	4.0,
	2.5,
	3.0,
	3.0,
	3.0,
	1.5,
	's1mple',
	'Natus Vincere',
	'0',
	'1',
	'1',
	1,
	1,
	'{"awp","p250"}'
);

INSERT INTO Videos VALUES(
	DEFAULT,
	'<iframe width="560" height="315" src="https://www.youtube.com/embed/qLVIgyrRk28" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>',
	'ESL One New York 2016',
	'de_cbble',
	5.0,
	4.0,
	3.5,
	5.0,
	5.0,
	1.5,
	'Snax',
	'Virtus.pro',
	'1',
	'1',
	'1',
	4,
	4,
	'{"usp"}'
);

INSERT INTO Videos VALUES(
	DEFAULT,
	'<iframe width="560" height="315" src="https://www.youtube.com/embed/dmrIfz1TN00" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>',
	'MLG Major Championship: Columbus 2016',
	'de_cache',
	5.0,
	4.0,
	4.5,
	5.0,
	4.5,
	1.0,
	'Hiko',
	'Team Liquid',
	'0',
	'1',
	'1',
	4,
	4,
	'{"m4a4"}'
);

-- Enable the crypto for passwords
CREATE EXTENSION pgcrypto;

CREATE TABLE Users (
	Id SERIAL PRIMARY KEY,
	Name VARCHAR(64) NOT NULL,
  	Email TEXT NOT NULL UNIQUE,
	Password TEXT NOT NULL,
	SignUpDate DATE NOT NULL DEFAULT CURRENT_DATE,
	SignInDate DATE NULL,
	FavoriteWeapon WEAPON NULL
);

CREATE TYPE STORY_TYPE AS ENUM('Player', 'Team', 'Event');
CREATE TYPE STORY_SCOPE AS ENUM('Map', 'Series', 'Event', 'Epoch');
-- Note that the reltionships with primary keys in VideoIds are not maintained
CREATE TABLE Stories (
	Id SERIAL PRIMARY KEY,
	CreationDate DATE NULL,
	Title VARCHAR NOT NULL,
	VideoIds INT ARRAY NOT NULL,
	Type STORY_TYPE NOT NULL,
	Scope STORY_SCOPE NOT NULL
);

INSERT INTO Users VALUES(
	DEFAULT,
	'clipd',
	'robbie.a.freeman@gmail.com',
	crypt('pass', gen_salt('bf')),
	DEFAULT,
	NULL,
	'mag7'
);

-- 6 cats: Casting, Significance, Intelligence, Atmosphere, Aim, Luck
-- meant to range from 0-5
CREATE TABLE RatingCategories (
	Id SERIAL PRIMARY KEY,
	Name VARCHAR NOT NULL
);

INSERT INTO RatingCategories VALUES(DEFAULT, 'Casting');
INSERT INTO RatingCategories VALUES(DEFAULT, 'Significance');
INSERT INTO RatingCategories VALUES(DEFAULT, 'Intelligence');
INSERT INTO RatingCategories VALUES(DEFAULT, 'Atmosphere');
INSERT INTO RatingCategories VALUES(DEFAULT, 'Aim');
INSERT INTO RatingCategories VALUES(DEFAULT, 'Luck');

CREATE TABLE Ratings (
	Id SERIAL PRIMARY KEY,
	VideoId SERIAL REFERENCES Videos,
	UserId SERIAL REFERENCES Users,
	RatingCategoryId SERIAL REFERENCES RatingCategories,
	UNIQUE (VideoId, UserId, RatingCategoryId),
	Rating FLOAT CHECK (rating >= 0.0 AND rating <= 5.0),
	CreationDate DATE NOT NULL DEFAULT now()
);

-- Table to track the average aggregate ratings, per cat, per video
CREATE TABLE RatingAvgs (
	Id SERIAL PRIMARY KEY,
	VideoId SERIAL REFERENCES Videos,
	RatingCategoryId SERIAL REFERENCES RatingCategories,
	UNIQUE (VideoId, RatingCategoryId),
	Total INT NOT NULL DEFAULT 0,
	Average FLOAT NULL CHECK (average >= 0.0 AND average <= 5.0)
);