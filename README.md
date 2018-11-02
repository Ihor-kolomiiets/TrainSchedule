# Train-Schedule
It's a bot for Telegram which provide info about Ukrainian railroad schedule(Except Dnipro) [Telegram link](https://t.me/UZTrain_Bot)

# What this project do
Scrape schedule information from 2 different UZ sites using users query, normalized it and provide as text in chat.

# How to install
For properly work requests, Beautiful Soup and pyTelegramBotAPI need to be installed. 
Make tables for station storage, and run TrainPars.py for scrape stations data and pull it to database.
```
CREATE TABLE `lviv_stations` (
	`station_id`	INTEGER UNIQUE,
	`name_ua`	TEXT,
	`department_id`	INTEGER,
	`region_id`	INTEGER
);
```
```
CREATE TABLE `regions` (
	`id`	INTEGER NOT NULL UNIQUE,
	`name_ua`	TEXT,
	`name_ru`	TEXT,
	`name_en`	TEXT,
	PRIMARY KEY(`id`)
) WITHOUT ROWID;
```
```
CREATE TABLE `stations` (
	`id`	INTEGER NOT NULL DEFAULT 1 PRIMARY KEY AUTOINCREMENT UNIQUE,
	`station_id`	INTEGER,
	`name_ua`	TEXT,
	`name_ru`	TEXT,
	`name_en`	TEXT,
	`region_id`	INTEGER,
	`department_id`	INTEGER DEFAULT 1,
	FOREIGN KEY(`region_id`) REFERENCES `regions`(`id`)
);
```
```
CREATE TABLE `user_info` (
	`user_id`	INTEGER,
	`state`	TEXT,
	`station_id`	INTEGER,
	`department_id`	INTEGER
);
```
P.S. If some of token left in git history it was revoked anyway.