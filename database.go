package main

import (
	"database/sql"
	"log"
	"time"

	"github.com/bwmarrin/discordgo"
	_ "github.com/mattn/go-sqlite3"
)

var db *sql.DB

func init() {
	var err error

	db, err = sql.Open("sqlite3", "./db/fishbot.db")
	if err != nil {
		log.Fatal(err)
	}

	sqlStmt := `
		CREATE TABLE IF NOT EXISTS users (
			user_id TEXT PRIMARY KEY,
			username TEXT,
			join_date DATE
		);
		CREATE TABLE IF NOT EXISTS fish (
			user_id TEXT PRIMARY KEY,
			rod_level INTEGER,
			total_caught INTEGER,
			common_caught INTEGER,
			rare_caught INTEGER,
			epic_caught INTEGER,
			legendary_caught INTEGER,
			FOREIGN KEY (user_id) REFERENCES users(user_id)
		);
		CREATE TABLE IF NOT EXISTS fishing (
			user_id TEXT PRIMARY KEY,
			pick_index INTEGER,
			date INTEGER,
			FOREIGN KEY (user_id) REFERENCES users(user_id)
		);
	`
	_, err = db.Exec(sqlStmt)
	if err != nil {
		log.Printf("%q: %s\n", err, sqlStmt)
		return
	}
}

func closeDB() {
	if db != nil {
		log.Println("Closing database")
		db.Close()
	}
}

// userExists checks if a user exists in the database & if not, adds them
func userExists(user *discordgo.User) {
	sqlStmt := `
		INSERT INTO users (user_id, username, join_date)
		VALUES (?, ?, ?)
		ON CONFLICT(user_id) DO NOTHING;
	`

	// get current date
	date := time.Now().Format("2006-01-02")

	var err error
	_, err = db.Exec(sqlStmt, user.ID, user.Username, date)
	if err != nil {
		log.Printf("%q: %s\n", err, sqlStmt)
		return
	}
}

// insert or replace a line into the fishing table
func registerFishing(userId string, fishIdx int, sleep int) {
	sqlStmt := `
		INSERT INTO fishing (user_id, pick_index, date)
		VALUES (?, ?, ?)
		ON CONFLICT(user_id) DO UPDATE SET pick_index = ?, date = ?;
	`

	// get current date in unixtime & add sleep time int
	date := time.Now().Add(time.Duration(sleep) * time.Second).Unix()

	var err error
	_, err = db.Exec(sqlStmt, userId, fishIdx, date, fishIdx, date)
	if err != nil {
		log.Printf("%q: %s\n", err, sqlStmt)
		return
	}
}

// funcion checkFishing(userId string, fishIdx int) that returns either true or false if the correct index was chosen for the user & if no more than 2 seconds have passed since the last fishing attempt
func checkFishing(userId string, fishIdx int) (success bool, reason int) {
	sqlStmt := `
		SELECT pick_index, date FROM fishing WHERE user_id = ?;
	`

	var (
		pickIndex int
		date      int64
	)

	err := db.QueryRow(sqlStmt, userId).Scan(&pickIndex, &date)
	if err != nil {
		log.Printf("%q: %s\n", err, sqlStmt)
		return false, 0
	}

	// check if more than 2 seconds have passed
	if time.Now().Unix() > date+2 {
		return false, 2
	}

	// check if correct index was chosen
	if pickIndex != fishIdx {
		return false, 1
	}

	return true, 0
}
