const defaultUserData = {
  rodLevel: 1,
  fishCaught: {
    total: 0,
    common: 0,
    rare: 0,
    epic: 0,
    legendary: 0,
  },
};

const FISH_TIME = 2500;

export async function getUserData(env, id) {
  const data = await env.FISHBOT_STORE.get(id);

  if (data === null) {
    await env.FISHBOT_STORE.put(id, JSON.stringify(defaultUserData));
    return defaultUserData;
  } else {
    return JSON.parse(data);
  }
}

export async function setUserData(env, id, fishType) {
  const data = await getUserData(env, id);
  data.fishCaught.total++;
  data.fishCaught[fishType]++;

  // rod levels up every 10 fish
  if (data.fishCaught.total % 10 === 0) {
    data.rodLevel++;
  }

  await env.FISHBOT_STORE.put(id, JSON.stringify(data));
}

export async function setUserFishData(env, id, fishList, pickFish) {
  await env.FISHBOT_STORE.put(
    id + '-fish',
    JSON.stringify({
      fishList: fishList,
      pick: pickFish,
      date: new Date().getTime(),
    }),
  );
}

function fishRandomness() {
  const fishType = Math.floor(Math.random() * 100);
  if (fishType < 50) {
    return 'common';
  } else if (fishType < 75) {
    return 'uncommon';
  } else if (fishType < 90) {
    return 'rare';
  } else if (fishType < 99) {
    return 'epic';
  } else {
    return 'legendary';
  }
}

export async function checkFishingSuccess(env, id, fishPick) {
  const data = JSON.parse(await env.FISHBOT_STORE.get(id + '-fish'));
  const time = new Date().getTime();

  if (time - data.date <= FISH_TIME) {
    if ('f' + data.pick === fishPick) {
      const fishType = fishRandomness();
      await setUserData(env, id, fishType);

      return {
        status: true,
        type: fishType,
        fish: data.fishList[data.pick],
      };
    }
    return { status: false, message: 'Wrong Fish :(' };
  }

  return { status: false, message: 'Too slow :(' };
}
