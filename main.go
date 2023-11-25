package main

import (
	"log"
	"os"
	"os/signal"

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

			buttons := generateFishButtons()
			_, err := s.FollowupMessageCreate(i.Interaction, true, &discordgo.WebhookParams{
				Content:         "asdf",
				Components:      buttons,
				AllowedMentions: &discordgo.MessageAllowedMentions{},
			})
			if err != nil {
				log.Println(err)
			}
		},
	}
)

func init() {
	err := godotenv.Load()
	if err != nil {
		log.Fatal("Error loading .env file")
	}

	bot_token := os.Getenv("DISCORD_TOKEN")

	log.Println(bot_token)

	s, err = discordgo.New("Bot " + bot_token)

	s.AddHandler(func(s *discordgo.Session, i *discordgo.InteractionCreate) {
		switch i.Type {
		case discordgo.InteractionApplicationCommand:
			if handler, ok := commandHandlers[i.ApplicationCommandData().Name]; ok {
				handler(s, i)
			}
		case discordgo.InteractionMessageComponent:
			if i.MessageComponentData().CustomID != "" {
				s.InteractionRespond(i.Interaction, &discordgo.InteractionResponse{
					Type: discordgo.InteractionResponseUpdateMessage,
					Data: &discordgo.InteractionResponseData{
						Content: "You clicked " + i.MessageComponentData().CustomID,
					},
				})
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
	log.Println("Graceful shutdown")
}
