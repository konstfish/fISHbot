package main

import (
	"fmt"
	"math/rand"
	"time"

	"github.com/bwmarrin/discordgo"
)

func generateFish() []string {
	fishList := []string{"🐟", "🐡", "🐠", "🦈", "🐳", "🐬", "🦀", "🦐", "🦑"}
	var fish []string

	rand.Seed(time.Now().UnixNano())
	for i := 0; i < 5; i++ {
		randomFish := fishList[rand.Intn(len(fishList))]
		for contains(fish, randomFish) {
			randomFish = fishList[rand.Intn(len(fishList))]
		}
		fish = append(fish, randomFish)
	}

	return fish
}

func contains(slice []string, val string) bool {
	for _, item := range slice {
		if item == val {
			return true
		}
	}
	return false
}

func generateFishButtons() []discordgo.MessageComponent {
	fish := generateFish()

	var buttons []discordgo.MessageComponent
	var actionRowComponents []discordgo.MessageComponent

	for i, v := range fish {
		// create button with "f"+index as custom id
		button := discordgo.Button{
			Label:    v,
			CustomID: fmt.Sprintf("f%d", i),
			Style:    discordgo.PrimaryButton,
		}
		actionRowComponents = append(actionRowComponents, button)
	}

	buttons = append(buttons, discordgo.ActionsRow{
		Components: actionRowComponents,
	})

	return buttons
}
