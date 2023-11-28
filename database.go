package main

import (
	"database/sql"
	"log"
	"math/rand"
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
			bait INTEGER,
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
			pick_fish TEXT,
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
func userExists(user *discordgo.User) bool {
	// check if userid is in table
	sqlStmt := `
		SELECT user_id FROM users WHERE user_id = ?;
	`

	var userId string
	err := db.QueryRow(sqlStmt, user.ID).Scan(&userId)
	if err != nil {
		if err == sql.ErrNoRows {
			createUser(user.ID, user.Username)
			createUserFish(user.ID)

			return false
		} else {
			log.Printf("%q: %s\n", err, sqlStmt)
			return false
		}
	}

	return true
}

func createUser(userId string, username string) {
	sqlStmt := `
		INSERT INTO users (user_id, username, join_date)
		VALUES (?, ?, ?)
		ON CONFLICT(user_id) DO NOTHING;
	`

	// get current date
	date := time.Now().Format("2006-01-02 15:04")

	var err error
	_, err = db.Exec(sqlStmt, userId, username, date)
	if err != nil {
		log.Printf("%q: %s\n", err, sqlStmt)
		return
	}
}

func createUserFish(userId string) {
	sqlStmt := `
		INSERT INTO fish (user_id, rod_level, bait, total_caught, common_caught, rare_caught, epic_caught, legendary_caught)
		VALUES (?, ?, ?, ?, ?, ?, ?, ?)
		ON CONFLICT(user_id) DO NOTHING;
	`

	var err error
	_, err = db.Exec(sqlStmt, userId, 1, 0, 0, 0, 0, 0, 0)
	if err != nil {
		log.Printf("%q: %s\n", err, sqlStmt)
		return
	}
}

// TODO fill user stats table

// getUserStats returns a user's stats from the database
func getUserStats(userId string) (user UserStats) {
	sqlStmt := `
		SELECT join_date, rod_level, bait, total_caught, common_caught, rare_caught, epic_caught, legendary_caught FROM users
		INNER JOIN fish ON users.user_id = fish.user_id
		WHERE users.user_id = ?;
	`

	err := db.QueryRow(sqlStmt, userId).Scan(&user.JoinDate, &user.RodLevel, &user.Bait, &user.TotalCaught, &user.CommonCaught, &user.RareCaught, &user.EpicCaught, &user.LegendaryCaught)
	if err != nil {
		log.Printf("%q: %s\n", err, sqlStmt)
		return
	}

	user.UserID = userId

	return user
}

// updateUserStats, updates a user's existing stats in the database when they catch a fish. the rod level increases by 1 every 10 fish caught, the function recieves the fish rarity
func updateUserStats(statsCur UserStats, rarity int) {
	statsCur.TotalCaught += 1
	// increase rod level every 10 fish caught
	if statsCur.TotalCaught%10 == 0 {
		statsCur.RodLevel += 1
	}

	// add a fish to the correct rarity
	switch rarity {
	case 0:
		statsCur.CommonCaught += 1
	case 1:
		statsCur.RareCaught += 1
	case 2:
		statsCur.EpicCaught += 1
	case 3:
		statsCur.LegendaryCaught += 1
	}

	// fill updated statsCur into database
	sqlStmt := `
		UPDATE fish SET rod_level = ?, total_caught = ?, common_caught = ?, rare_caught = ?, epic_caught = ?, legendary_caught = ?
		WHERE user_id = ?;
	`

	_, err := db.Exec(sqlStmt, statsCur.RodLevel, statsCur.TotalCaught, statsCur.CommonCaught, statsCur.RareCaught, statsCur.EpicCaught, statsCur.LegendaryCaught, statsCur.UserID)
	if err != nil {
		log.Printf("%q: %s\n", err, sqlStmt)
		return
	}
}

func getFishRarity(rodLevel int, bait bool) int {
	chances := map[int]float64{
		0: 70.0, // Common
		1: 20.0, // Rare
		2: 8.0,  // Epic
		3: 2.0,  // Legendary
	}

	for i := 0; i < rodLevel; i++ {
		chances[0] *= 0.95
		chances[1] += 0.03
		chances[2] += 0.01
		chances[3] += 0.01
	}

	if bait {
		chances[0] *= 0.9
		chances[1] += 0.05
		chances[2] += 0.03
		chances[3] += 0.02
	}

	fishRng := rand.Float64() * 100

	var cumulativeChance float64
	for rarity, chance := range chances {
		cumulativeChance += chance
		if fishRng <= cumulativeChance {
			return rarity
		}
	}

	return 0
}

// insert or replace a line into the fishing table
func registerFishing(userId string, fishIdx int, fishType string, sleep int) {
	sqlStmt := `
		INSERT INTO fishing (user_id, pick_index, pick_fish, date)
		VALUES (?, ?, ?, ?)
		ON CONFLICT(user_id) DO UPDATE SET pick_index = ?, pick_fish = ?, date = ?;
	`

	// get current date in unixtime & add sleep time int
	date := time.Now().Add(time.Duration(sleep) * time.Second).Unix()

	var err error
	_, err = db.Exec(sqlStmt, userId, fishIdx, fishType, date, fishIdx, fishType, date)
	if err != nil {
		log.Printf("%q: %s\n", err, sqlStmt)
		return
	}
}

// funcion checkFishing(userId string, fishIdx int) that returns either true or false if the correct index was chosen for the user & if no more than 2 seconds have passed since the last fishing attempt
func checkFishing(userId string, fishIdx int) (success bool, reason int, fishType string) {
	sqlStmt := `
		SELECT pick_index, pick_fish, date FROM fishing WHERE user_id = ?;
	`

	var (
		pickIndex int
		fish      string
		date      int64
	)

	err := db.QueryRow(sqlStmt, userId).Scan(&pickIndex, &fish, &date)
	if err != nil {
		log.Printf("%q: %s\n", err, sqlStmt)
		return false, 0, ""
	}

	// check if more than 2 seconds have passed
	if time.Now().Unix() > date+2 {
		return false, 2, fish
	}

	// check if correct index was chosen
	if pickIndex != fishIdx {
		return false, 1, fish
	}

	return true, 0, fish
}
