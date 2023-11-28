package main

import (
	"fmt"
	"log"
	"math/rand"
	"os"
	"os/signal"
	"strconv"
	"strings"

	"github.com/bwmarrin/discordgo"
	"github.com/joho/godotenv"
)

var s *discordgo.Session

var (
	GuildID = "1174873885490020362"

	commands = []*discordgo.ApplicationCommand{
		{
			Name:        "ping",
			Description: "Ping Pong",
		},
		{
			Name:        "fish",
			Description: "Go fishing!",
		},
	}

	commandHandlers = map[string]func(s *discordgo.Session, i *discordgo.InteractionCreate){
		"ping": func(s *discordgo.Session, i *discordgo.InteractionCreate) {
			s.InteractionRespond(i.Interaction, &discordgo.InteractionResponse{
				Type: discordgo.InteractionResponseChannelMessageWithSource,
				Data: &discordgo.InteractionResponseData{
					Content: "Pong!",
				},
			})
		},
		"fish": func(s *discordgo.Session, i *discordgo.InteractionCreate) {
			s.InteractionRespond(i.Interaction, &discordgo.InteractionResponse{
				Type: discordgo.InteractionResponseDeferredChannelMessageWithSource,
			})

			// register user
			userExists(i.Member.User)

			// setup response message
			fish := generateFish()
			buttons := generateFishButtons(fish, i.Member.User.ID)

			message, err := s.FollowupMessageCreate(i.Interaction, true, &discordgo.WebhookParams{
				Content:         fmt.Sprintf("%s started fishing with a level %d 🎣", i.Member.User.Username, 1),
				Components:      buttons,
				AllowedMentions: &discordgo.MessageAllowedMentions{},
			})
			if err != nil {
				log.Println(err)
			}

			sleep := rand.Intn(5) + 1
			fishIdx := rand.Intn(len(fish))

			registerFishing(i.Member.User.ID, fishIdx, fish[fishIdx], sleep)

			go fishButtonHandler(s, i, message, sleep, fish[fishIdx])
		},
	}
)

func init() {
	godotenv.Load()

	bot_token := os.Getenv("DISCORD_TOKEN")

	log.Println(bot_token)

	s, _ = discordgo.New("Bot " + bot_token)

	s.AddHandler(func(s *discordgo.Session, i *discordgo.InteractionCreate) {
		switch i.Type {
		case discordgo.InteractionApplicationCommand:
			if handler, ok := commandHandlers[i.ApplicationCommandData().Name]; ok {
				handler(s, i)
			}
		case discordgo.InteractionMessageComponent:
			if i.MessageComponentData().CustomID != "" {
				parts := strings.Split(i.MessageComponentData().CustomID, "-")
				if len(parts) != 2 {
					return
				}

				userId := parts[0]
				fishIdx, err := strconv.Atoi(parts[1])
				if err != nil {
					fmt.Println("Conversion error:", err)
					return
				}

				if i.Member.User.ID != userId {
					s.InteractionRespond(i.Interaction, &discordgo.InteractionResponse{
						Type: discordgo.InteractionResponseChannelMessageWithSource,
						Data: &discordgo.InteractionResponseData{
							Content: "Don't try to catch someone else's fish!",
							Flags:   discordgo.MessageFlagsEphemeral,
						},
					})

					return
				}

				success, reason, fish := checkFishing(i.Member.User.ID, fishIdx)

				if success {
					s.InteractionRespond(i.Interaction, &discordgo.InteractionResponse{
						Type: discordgo.InteractionResponseUpdateMessage,
						Data: &discordgo.InteractionResponseData{
							Content: fmt.Sprintf("You caught a %s!", fish),
						},
					})
				} else {
					var message string
					switch reason {
					case 1:
						message = "Wrong fish :("
					case 2:
						message = "Too slow :("
					}

					s.InteractionRespond(i.Interaction, &discordgo.InteractionResponse{
						Type: discordgo.InteractionResponseUpdateMessage,
						Data: &discordgo.InteractionResponseData{
							Content: message,
						},
					})
				}

				/*s.InteractionRespond(i.Interaction, &discordgo.InteractionResponse{
					Type: discordgo.InteractionResponseUpdateMessage,
					Data: &discordgo.InteractionResponseData{
						Content: "You clicked " + i.MessageComponentData().CustomID,
					},
				})*/
			}
		}
	})
}

func main() {
	err := s.Open()
	if err != nil {
		log.Fatal("Error opening connection,", err)
	}

	log.Println("Adding commands...")
	registeredCommands := make([]*discordgo.ApplicationCommand, len(commands))
	for i, v := range commands {
		registeredCommands[i], err = s.ApplicationCommandCreate(s.State.User.ID, GuildID, v)
		if err != nil {
			log.Fatal("Error creating command,", err)
		}
	}

	defer s.Close()
	stop := make(chan os.Signal, 1)
	signal.Notify(stop, os.Interrupt)
	<-stop
	closeDB()
	log.Println("Graceful shutdown")
}
