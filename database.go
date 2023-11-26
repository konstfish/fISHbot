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
	db, err := sql.Open("sqlite3", "./db/fishbot.db")
	if err != nil {
		log.Fatal(err)
	}
	defer db.Close()

	sqlStmt := `
		CREATE TABLE IF NOT EXISTS users (
			user_id TEXT PRIMARY KEY,
			username TEXT,
			join_date DATE
		);
		CREATE TABLE IF NOT EXISTS fish (
			user_id TEXT,
			rod_level INTEGER,
			total_caught INTEGER,
			common_caught INTEGER,
			rare_caught INTEGER,
			epic_caught INTEGER,
			legendary_caught INTEGER,
			FOREIGN KEY (user_id) REFERENCES users(user_id)
		);
		CREATE TABLE IF NOT EXISTS fishing (
			user_id TEXT,
			pick_fish TEXT,
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

// userExists checks if a user exists in the database & if not, adds them
func userExists(user *discordgo.User) {
	db, err := sql.Open("sqlite3", "./db/fishbot.db")
	if err != nil {
		log.Fatal(err)
	}
	defer db.Close()

	sqlStmt := `
		INSERT INTO users (user_id, username, join_date)
		VALUES (?, ?, ?)
		ON CONFLICT(user_id) DO NOTHING;
	`

	// get current date
	date := time.Now().Format("2006-01-02")

	_, err = db.Exec(sqlStmt, user.ID, user.Username, date)
	if err != nil {
		log.Printf("%q: %s\n", err, sqlStmt)
		return
	}
}
