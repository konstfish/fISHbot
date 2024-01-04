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

func generateFishButtons(fish []string, userId string) []discordgo.MessageComponent {
	var buttons []discordgo.MessageComponent
	var actionRowComponents []discordgo.MessageComponent

	for i, v := range fish {
		button := discordgo.Button{
			Emoji: discordgo.ComponentEmoji{
				Name: v,
			},
			CustomID: fmt.Sprintf("fish-%s-%d", userId, i),
			Style:    discordgo.PrimaryButton,
		}
		actionRowComponents = append(actionRowComponents, button)
	}

	buttons = append(buttons, discordgo.ActionsRow{
		Components: actionRowComponents,
	})

	return buttons
}

func fishButtonHandler(s *discordgo.Session, i *discordgo.InteractionCreate, message *discordgo.Message, sleep int, fish string) {
	sleeptime := time.Duration(sleep) * time.Second
	time.Sleep(sleeptime)

	messageText := fmt.Sprintf("React with %s!", fish)

	_, err := s.FollowupMessageEdit(i.Interaction, message.ID, &discordgo.WebhookEdit{
		Content:         &messageText,
		Components:      nil,
		AllowedMentions: &discordgo.MessageAllowedMentions{},
	})
	if err != nil {
		fmt.Println(err)
	}
}
