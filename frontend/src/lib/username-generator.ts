const adjectives = [
  "Wandering",
  "Global",
  "Nomadic",
  "Adventure",
  "Explorer",
  "Voyaging",
  "Roaming",
  "Traveling",
  "Journeying",
  "Galactic",
  "Cosmic",
  "Intrepid",
  "Daring",
  "Fearless",
  "Curious",
];

const nouns = [
  "Traveler",
  "Wanderer",
  "Explorer",
  "Voyager",
  "Adventurer",
  "Nomad",
  "Globetrotter",
  "Pathfinder",
  "Pioneer",
  "Navigator",
  "Discoverer",
  "Wayfarer",
  "Rover",
  "Trekker",
  "Pilgrim",
];

export function generateUsername(): string {
  const adjective = adjectives[Math.floor(Math.random() * adjectives.length)];
  const noun = nouns[Math.floor(Math.random() * nouns.length)];
  const number = Math.floor(Math.random() * 1000);

  // Format: AdjectiveNoun123
  return `${adjective}${noun}${number}`;
}
