import { ButtonStyleTypes } from 'discord-interactions';

export function generateFish() {
  var fishList = ['🐟', '🐡', '🐠', '🦈', '🐳', '🐬', '🦀', '🦐', '🦑'];

  var fish = [];
  for (var i = 0; i < 5; i++) {
    var randomFish = fishList[Math.floor(Math.random() * fishList.length)];
    while (fish.includes(randomFish)) {
      randomFish = fishList[Math.floor(Math.random() * fishList.length)];
    }
    fish.push(randomFish);
  }

  return fish;
}

export function generateFishButtons(fishList) {
  var fishActions = [];

  for (var i = 0; i < fishList.length; i++) {
    fishActions.push({
      type: 2,
      label: '',
      style: ButtonStyleTypes.PRIMARY,
      custom_id: 'f' + i,
      emoji: {
        name: fishList[i],
      },
    });
  }

  return fishActions;
}
