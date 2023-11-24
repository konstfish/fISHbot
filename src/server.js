/**
 * The core server that runs on a Cloudflare worker.
 */

import { Router } from 'itty-router';
import {
  InteractionResponseType,
  InteractionType,
  verifyKey,
  InteractionResponseFlags,
} from 'discord-interactions';
import { FISH_COMMAND, STATS_COMMAND, FACT_COMMAND } from './commands.js';

import { generateFish, generateFishButtons } from './fishing.js';

import { fishFacts } from './fishfacts.js';

import {
  getUserData,
  setUserFishData,
  checkFishingSuccess,
} from './fishStore.js';

class JsonResponse extends Response {
  constructor(body, init) {
    const jsonBody = JSON.stringify(body);
    init = init || {
      headers: {
        'content-type': 'application/json;charset=UTF-8',
      },
    };
    super(jsonBody, init);
  }
}

const router = Router();

router.get('/', (request, env) => {
  const applicationId = env.DISCORD_APPLICATION_ID;
  const INVITE_URL = `https://discord.com/oauth2/authorize?client_id=${applicationId}&permissions=2112&scope=bot%20applications.commands`;

  return Response.redirect(INVITE_URL, 301);
});

/**
 * Main route for all requests sent from Discord.  All incoming messages will
 * include a JSON payload described here:
 * https://discord.com/developers/docs/interactions/receiving-and-responding#interaction-object
 */
router.post('/', async (request, env) => {
  const { isValid, interaction } = await server.verifyDiscordRequest(
    request,
    env,
  );
  if (!isValid || !interaction) {
    return new Response('Bad request signature.', { status: 401 });
  }

  if (interaction.type === InteractionType.PING) {
    return new JsonResponse({
      type: InteractionResponseType.PONG,
    });
  }

  if (interaction.type === InteractionType.APPLICATION_COMMAND) {
    switch (interaction.data.name.toLowerCase()) {
      case FISH_COMMAND.name.toLowerCase(): {
        const fishList = generateFish();
        const pickFish = Math.floor(Math.random() * fishList.length);

        const userData = await getUserData(env, interaction.member.user.id);
        await setUserFishData(
          env,
          interaction.member.user.id,
          fishList,
          pickFish,
        );

        const fishingMessage = `Started fishing with a level ${userData.rodLevel} 🎣 for ${fishList[pickFish]}`;

        return new JsonResponse({
          type: InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
          data: {
            content: fishingMessage,
            components: [
              {
                type: 1,
                components: generateFishButtons(
                  fishList,
                  interaction.member.user.id,
                ),
              },
            ],
          },
        });
      }
      case STATS_COMMAND.name.toLowerCase(): {
        const userData = await getUserData(env, interaction.member.user.id);
        const statsMessage = `
🎣 Rod Level: ${userData.rodLevel}
**🐟 Fish Caught:** ${userData.fishCaught.total}
⭐ Common: ${userData.fishCaught.common}
💠 Rare: ${userData.fishCaught.rare}
🌀 Epic: ${userData.fishCaught.epic}
🌌 Legendary: ${userData.fishCaught.legendary}`;

        return new JsonResponse({
          type: InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
          data: {
            content: statsMessage,
          },
        });
      }
      case FACT_COMMAND.name.toLowerCase(): {
        // pick random entry from fishFacts and return
        const pickFact = Math.floor(Math.random() * fishFacts.length);
        const factMessage = fishFacts[pickFact];

        return new JsonResponse({
          type: InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
          data: {
            content: factMessage,
          },
        });
      }
      default:
        return new JsonResponse({ error: 'Unknown Type' }, { status: 400 });
    }
  } else if (interaction.type === InteractionType.MESSAGE_COMPONENT) {
    // check if pressed button id corresponds with user id
    if (
      interaction.data.custom_id.split('-')[0] !== interaction.member.user.id
    ) {
      return new JsonResponse({
        type: InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
        data: {
          content: "Don't try to catch someone else's fish!",
          flags: InteractionResponseFlags.EPHEMERAL,
        },
      });
    }

    const succ = await checkFishingSuccess(
      env,
      interaction.member.user.id,
      interaction.data.custom_id,
    );

    var message = '';
    if (succ.status) {
      if (succ.type === 'epic') {
        message = `You caught an ${succ.type} ${succ.fish}!`;
      } else {
        message = `You caught a ${succ.type} ${succ.fish}!`;
      }
    } else {
      message = succ.message;
    }

    return new JsonResponse({
      type: InteractionResponseType.UPDATE_MESSAGE,
      data: {
        content: message,
        components: [],
      },
    });
  }

  console.error('Unknown Type');
  return new JsonResponse({ error: 'Unknown Type' }, { status: 400 });
});

router.all('*', () => new Response('Not Found.', { status: 404 }));

async function verifyDiscordRequest(request, env) {
  const signature = request.headers.get('x-signature-ed25519');
  const timestamp = request.headers.get('x-signature-timestamp');
  const body = await request.text();
  const isValidRequest =
    signature &&
    timestamp &&
    verifyKey(body, signature, timestamp, env.DISCORD_PUBLIC_KEY);
  if (!isValidRequest) {
    return { isValid: false };
  }

  return { interaction: JSON.parse(body), isValid: true };
}

const server = {
  verifyDiscordRequest: verifyDiscordRequest,
  fetch: async function (request, env) {
    return router.handle(request, env);
  },
};

export default server;
