package main

import (
	"database/sql"
	"log"
	"math/rand"
	"os"
	"time"

	"github.com/bwmarrin/discordgo"
	_ "github.com/lib/pq"
)

var db *sql.DB

func init() {
	var err error

	dbURL := os.Getenv("DATABASE_URL")
	if dbURL == "" {
		log.Fatal("DATABASE_URL environment variable is not set")
	}

	db, err = sql.Open("postgres", dbURL)
	if err != nil {
		log.Fatal(err)
	}

	err = db.Ping()
	if err != nil {
		log.Fatal("Failed to connect to database:", err)
	}

	sqlStmt := `
		CREATE TABLE IF NOT EXISTS users (
			user_id TEXT PRIMARY KEY,
			username TEXT,
			join_date TIMESTAMP
		);
		CREATE TABLE IF NOT EXISTS fish (
			user_id TEXT PRIMARY KEY,
			money INTEGER DEFAULT 0,
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
			date BIGINT,
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
		SELECT user_id FROM users WHERE user_id = $1;
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
		VALUES ($1, $2, $3)
		ON CONFLICT(user_id) DO NOTHING;
	`

	date := time.Now()

	_, err := db.Exec(sqlStmt, userId, username, date)
	if err != nil {
		log.Printf("%q: %s\n", err, sqlStmt)
		return
	}
}

func createUserFish(userId string) {
	sqlStmt := `
		INSERT INTO fish (user_id, rod_level, bait, total_caught, common_caught, rare_caught, epic_caught, legendary_caught)
		VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
		ON CONFLICT(user_id) DO NOTHING;
	`

	_, err := db.Exec(sqlStmt, userId, 1, 10, 0, 0, 0, 0, 0)
	if err != nil {
		log.Printf("%q: %s\n", err, sqlStmt)
		return
	}
}

func getUserStats(userId string) (user UserStats) {
	sqlStmt := `
		SELECT join_date, rod_level, money, bait, total_caught, common_caught, rare_caught, epic_caught, legendary_caught FROM users
		INNER JOIN fish ON users.user_id = fish.user_id
		WHERE users.user_id = $1;
	`

	err := db.QueryRow(sqlStmt, userId).Scan(&user.JoinDate, &user.RodLevel, &user.Money, &user.Bait, &user.TotalCaught, &user.CommonCaught, &user.RareCaught, &user.EpicCaught, &user.LegendaryCaught)
	if err != nil {
		log.Printf("%q: %s\n", err, sqlStmt)
		return
	}

	user.UserID = userId

	return user
}

// updateUserStats, updates a user's existing stats in the database when they catch a fish
func updateUserStats(statsCur UserStats, rarity int) {
	if rarity != -1 {
		statsCur.TotalCaught += 1
		// increase rod level every 10 fish caught
		if statsCur.TotalCaught%10 == 0 {
			statsCur.RodLevel += 1
		}

		// add a fish to the correct rarity
		switch rarity {
		case 0:
			statsCur.CommonCaught += 1
			statsCur.Money += 1
		case 1:
			statsCur.RareCaught += 1
			statsCur.Money += 3
		case 2:
			statsCur.EpicCaught += 1
			statsCur.Money += 5
		case 3:
			statsCur.LegendaryCaught += 1
			statsCur.Money += 10
		}
	}

	if statsCur.Bait > 0 {
		statsCur.Bait -= 1
	}

	sqlStmt := `
		UPDATE fish SET rod_level = $1, money = $2, bait = $3, total_caught = $4, common_caught = $5, rare_caught = $6, epic_caught = $7, legendary_caught = $8
		WHERE user_id = $9;
	`

	_, err := db.Exec(sqlStmt, statsCur.RodLevel, statsCur.Money, statsCur.Bait, statsCur.TotalCaught, statsCur.CommonCaught, statsCur.RareCaught, statsCur.EpicCaught, statsCur.LegendaryCaught, statsCur.UserID)
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
		VALUES ($1, $2, $3, $4)
		ON CONFLICT(user_id) DO UPDATE SET pick_index = $5, pick_fish = $6, date = $7;
	`

	// get current date in unixtime & add sleep time int
	date := time.Now().Add(time.Duration(sleep) * time.Second).Unix()

	_, err := db.Exec(sqlStmt, userId, fishIdx, fishType, date, fishIdx, fishType, date)
	if err != nil {
		log.Printf("%q: %s\n", err, sqlStmt)
		return
	}
}

// funcion checkFishing(userId string, fishIdx int) that returns either true or false if the correct index was chosen for the user & if no more than 2 seconds have passed since the last fishing attempt
func checkFishing(userId string, fishIdx int) (success bool, reason int, fishType string) {
	sqlStmt := `
		SELECT pick_index, pick_fish, date FROM fishing WHERE user_id = $1;
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

// 💰 Price List:\n - 2 Bait for 1\n - 5 Bait for 2\n - 10 Bait for 4",
func buyBait(userId string, bait int) (success bool, reason int) {
	user := getUserStats(userId)

	log.Println(userId, bait)

	var amount int
	var price int

	switch bait {
	case 1:
		price = 1
		if user.Money < price {
			return false, 1
		}
		amount = 2
	case 2:
		price = 2
		if user.Money < price {
			return false, 1
		}
		amount = 5
	case 3:
		price = 4
		if user.Money < price {
			return false, 1
		}
		amount = 10
	}

	log.Println(amount, price)

	// update bait and money in user table
	user.Bait += amount
	user.Money -= price

	sqlStmt := `
		UPDATE fish SET bait = $1, money = $2 WHERE user_id = $3;
	`

	_, err := db.Exec(sqlStmt, user.Bait, user.Money, userId)
	if err != nil {
		log.Printf("%q: %s\n", err, sqlStmt)
		return false, 2
	}

	return true, 0
}
