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
	commands = []*discordgo.ApplicationCommand{
		{
			Name:        "ping",
			Description: "Ping Pong",
		},
		{
			Name:        "fish",
			Description: "Catch a fish!",
		},
		{
			Name:        "stats",
			Description: "View your fishing stats!",
		},
		{
			Name:        "shop",
			Description: "Trade your fish for bait and rods!",
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

			var discorduser *discordgo.User
			if i.GuildID == "" {
				discorduser = i.User
			} else {
				discorduser = i.Member.User
			}

			userExists(discorduser)
			var user UserStats = getUserStats(discorduser.ID)

			// setup response message
			fish := generateFish()
			buttons := generateFishButtons(fish, discorduser.ID)

			message, err := s.FollowupMessageCreate(i.Interaction, true, &discordgo.WebhookParams{
				Content:         fmt.Sprintf("%s started fishing with a level %d 🎣", discorduser.Username, user.RodLevel),
				Components:      buttons,
				AllowedMentions: &discordgo.MessageAllowedMentions{},
			})
			if err != nil {
				log.Println(err)
			}

			sleep := rand.Intn(5) + 1
			fishIdx := rand.Intn(len(fish))

			registerFishing(discorduser.ID, fishIdx, fish[fishIdx], sleep)

			go fishButtonHandler(s, i, message, sleep, fish[fishIdx])
		},
		"stats": func(s *discordgo.Session, i *discordgo.InteractionCreate) {
			s.InteractionRespond(i.Interaction, &discordgo.InteractionResponse{
				Type: discordgo.InteractionResponseDeferredChannelMessageWithSource,
			})

			var discorduser *discordgo.User
			if i.GuildID == "" {
				discorduser = i.User
			} else {
				discorduser = i.Member.User
			}

			userExists(discorduser)
			var user UserStats = getUserStats(discorduser.ID)

			/*
				🎣 Rod Level: 3
				🐟 Fish Caught: 26
				⭐ Common: 13
				💠 Rare: 11
				🌀 Epic: 2
				🌌 Legendary: 0
			*/

			_, err := s.FollowupMessageCreate(i.Interaction, true, &discordgo.WebhookParams{
				Content: fmt.Sprintf("🎣 Rod Level: %d\n💰 Money: %d\n🪝 Bait Available: %d\n🐟 Total Fish Caught: %d\n⭐ Common: %d\n💠 Rare: %d\n🌀 Epic: %d\n🌌 Legendary: %d",
					user.RodLevel, user.Money, user.Bait, user.TotalCaught, user.CommonCaught,
					user.RareCaught, user.EpicCaught, user.LegendaryCaught),
			})
			if err != nil {
				log.Println(err)
			}
		},
		"shop": func(s *discordgo.Session, i *discordgo.InteractionCreate) {
			s.InteractionRespond(i.Interaction, &discordgo.InteractionResponse{
				Type: discordgo.InteractionResponseDeferredChannelMessageWithSource,
			})

			var discorduser *discordgo.User
			if i.GuildID == "" {
				discorduser = i.User
			} else {
				discorduser = i.Member.User
			}

			userExists(discorduser)

			embed := []*discordgo.MessageEmbed{
				&discordgo.MessageEmbed{
					Image: &discordgo.MessageEmbedImage{
						URL: "https://media.tenor.com/Am-M2wsP19YAAAAd/morshu-zelda.gif",
					},
				},
			}

			actionRow := discordgo.ActionsRow{
				Components: []discordgo.MessageComponent{
					discordgo.Button{
						Label:    "2 Bait",
						CustomID: fmt.Sprintf("shop-%s-%d", discorduser.ID, 1),
					},
					discordgo.Button{
						Label:    "5 Bait",
						CustomID: fmt.Sprintf("shop-%s-%d", discorduser.ID, 2),
					},
					discordgo.Button{
						Label:    "10 Bait",
						CustomID: fmt.Sprintf("shop-%s-%d", discorduser.ID, 3),
					},
				},
			}

			_, err := s.FollowupMessageCreate(i.Interaction, true, &discordgo.WebhookParams{
				Content:    "**💰 Price List:**\n- 2 Bait for 1\n- 5 Bait for 2\n- 10 Bait for 4",
				Embeds:     embed,
				Components: []discordgo.MessageComponent{actionRow},
			})
			if err != nil {
				log.Println(err)
			}
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
				if len(parts) != 3 {
					return
				}

				userId := parts[1]

				chosenIdx, err := strconv.Atoi(parts[2])

				if err != nil {
					fmt.Println("Conversion error:", err)
					return
				}

				var discorduser *discordgo.User
				if i.GuildID == "" {
					discorduser = i.User
				} else {
					discorduser = i.Member.User
				}

				if parts[0] == "fish" {
					if discorduser.ID != userId {
						s.InteractionRespond(i.Interaction, &discordgo.InteractionResponse{
							Type: discordgo.InteractionResponseChannelMessageWithSource,
							Data: &discordgo.InteractionResponseData{
								Content: "Don't try to catch someone else's fish!",
								Flags:   discordgo.MessageFlagsEphemeral,
							},
						})

						return
					}

					success, reason, fish := checkFishing(discorduser.ID, chosenIdx)
					user := getUserStats(discorduser.ID)
					rarity := getFishRarity(user.RodLevel, (user.Bait > 0)) // todo implement bait

					// create string for rarity
					var rarityString string
					switch rarity {
					case 0:
						rarityString = "common"
					case 1:
						rarityString = "rare"
					case 2:
						rarityString = "epic"
					case 3:
						rarityString = "legendary"
					}

					if success {
						s.InteractionRespond(i.Interaction, &discordgo.InteractionResponse{
							Type: discordgo.InteractionResponseUpdateMessage,
							Data: &discordgo.InteractionResponseData{
								Content: fmt.Sprintf("You caught a %s %s!", rarityString, fish),
							},
						})

						updateUserStats(user, rarity)

					} else {
						var message string
						switch reason {
						case 1:
							message = "Wrong fish :("
						case 2:
							message = "Too slow :("
						}

						updateUserStats(user, -1)

						s.InteractionRespond(i.Interaction, &discordgo.InteractionResponse{
							Type: discordgo.InteractionResponseUpdateMessage,
							Data: &discordgo.InteractionResponseData{
								Content: message,
							},
						})
					}
				} else if parts[0] == "shop" {
					if discorduser.ID != userId {
						s.InteractionRespond(i.Interaction, &discordgo.InteractionResponse{
							Type: discordgo.InteractionResponseChannelMessageWithSource,
							Data: &discordgo.InteractionResponseData{
								Content: "Get ur own shop!",
								Flags:   discordgo.MessageFlagsEphemeral,
							},
						})

						return
					}

					success, reason := buyBait(discorduser.ID, chosenIdx)

					if success {
						s.InteractionRespond(i.Interaction, &discordgo.InteractionResponse{
							Type: discordgo.InteractionResponseUpdateMessage,
							Data: &discordgo.InteractionResponseData{
								Content: "You bought some bait!",
							},
						})
					} else {
						var message string
						switch reason {
						case 1:
							message = "Not enough money :("
						case 2:
							message = "DB error :("
						}

						s.InteractionRespond(i.Interaction, &discordgo.InteractionResponse{
							Type: discordgo.InteractionResponseUpdateMessage,
							Data: &discordgo.InteractionResponseData{
								Content: message,
							},
						})
					}
				}

				return

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
		registeredCommands[i], err = s.ApplicationCommandCreate(s.State.User.ID, "", v)
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
