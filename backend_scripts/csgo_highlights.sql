CREATE database csgo_highlights;

use csgo_highlights;

CREATE TABLE videos(
link VARCHAR(512) NOT NULL,
event VARCHAR(64) NULL,
casting FLOAT CHECK (casting >= 1.0 AND casting <= 5.0),
significance FLOAT CHECK (significance >= 1.0 AND significance <= 5.0),
intelligence FLOAT CHECK (intelligence >= 1.0 AND intelligence <= 5.0),
atmosphere FLOAT CHECK (atmosphere >= 1.0 AND atmosphere <= 5.0),
aim FLOAT CHECK (aim >= 1.0 AND aim <= 5.0),
luck FLOAT CHECK (luck >= 1.0 AND luck <= 5.0),
player VARCHAR(32) NOT NULL,
team VARCHAR(64) NULL,
grand_final ENUM('Y','N') NOT NULL,
armor ENUM('Y','N') NOT NULL,
crowd ENUM('Y','N') NOT NULL,
kills INT CHECK (kills >= 0 AND kills <= 5),
clutch_kills INT CHECK (clutch_kills >= 0 AND clutch_kills <= 5),
-- ENUM('cz','desert_eagle','dual_berettas','five_seven','glock','p2000','p250','r8','tec9','usp','mag7','nova','sawed_off','xm','mac10','mp5','mp7','mp9','p90','pp_bizon','ump','ak','aug','famas','galil','m4a1s','m4a4','sg','awp','g3sg1','scar','ssg','m249','negev','knife','zeus','he','fire','flash','smoke')
weapons VARCHAR(32) NOT NULL
);

INSERT INTO videos VALUES(
'https://www.youtube.com/watch?v=AzeuySdai40',
'PGL Major Krakow 2017',
3.0,
3.0,
5.0,
4.0,
1.0,
3.0,
'Dosia',
'Gambit Gaming',
'Y',
'Y',
'Y',
0,
0,
'he'
);

INSERT INTO videos VALUES(
'https://www.youtube.com/watch?v=yJifD2IEgx4',
'PGL Regional Minor Championship Europe - ELEAGUE Major 2017',
3.0,
2.0,
3.0,
2.0,
4.0,
1.0,
'BARBARR',
'Epsilon',
'N',
'Y',
'N',
4,
4,
'ak'
);

INSERT INTO videos VALUES(
'https://www.youtube.com/watch?v=1NN1CjhH7rA',
'ESL One Katowice 2015',
5.0,
3.0,
2.0,
5.0,
5.0,
1.5,
'friberg',
'Ninjas in Pyjamas',
'Y',
'Y',
'Y',
2,
2,
'ak'
);

INSERT INTO videos VALUES(
'https://www.youtube.com/watch?v=W9Jbo4Dv7vc',
'ESL One Cologne 2015',
4.5,
5.0,
2.5,
4.5,
5.0,
2.0,
'KRIMZ',
'Fnatic',
'Y',
'Y',
'Y',
3,
3,
'ak'
);

INSERT INTO videos VALUES(
'https://www.youtube.com/watch?v=W9Jbo4Dv7vc',
'ESL One Cologne 2015',
5.0,
4.0,
3.5,
5.0,
1.0,
2.5,
'NBK',
'Team EnVyUs',
'Y',
'Y',
'Y',
1,
0,
'knife'
);

INSERT INTO videos VALUES(
'https://www.youtube.com/watch?v=cjOVXdarUTs',
'MLG Major Championship: Columbus 2016',
5.0,
5.0,
2.0,
4.0,
2.0,
5.0,
'coldzera',
'Luminosity Gaming',
'N',
'N',
'Y',
4,
0,
'awp'
);

INSERT INTO videos VALUES(
'https://www.youtube.com/watch?v=kUSN6u5CSRE',
'ESL One Cologne 2016',
5.0,
5.0,
2.0,
5.0,
5.0,
5.0,
's1mple',
'Team Liquid',
'N',
'Y',
'Y',
2,
2,
'awp'
);

INSERT INTO videos VALUES(
'https://www.youtube.com/watch?v=PO1G0bmWurc',
'ESL One New York 2016',
4.0,
2.5,
3.0,
3.0,
3.0,
1.5,
's1mple',
'Natus Vincere',
'N',
'Y',
'Y',
1,
1,
('awp,p250')
);

INSERT INTO videos VALUES(
'https://www.youtube.com/watch?v=qLVIgyrRk28',
'ESL One New York 2016',
5.0,
4.0,
3.5,
5.0,
5.0,
1.5,
'Snax',
'Virtus.pro',
'Y',
'Y',
'Y',
4,
4,
('usp')
);

INSERT INTO videos VALUES(
'https://www.youtube.com/watch?v=dmrIfz1TN00',
'MLG Major Championship: Columbus 2016',
5.0,
4.0,
4.5,
5.0,
4.5,
1.0,
'Hiko',
'Team Liquid',
'N',
'Y',
'Y',
4,
4,
('m4a4')
);