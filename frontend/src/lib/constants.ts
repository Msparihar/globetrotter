export const RANKS = [
  { min: 0, title: "Novice Explorer", icon: "🌱" },
  { min: 20, title: "Adventurous Soul", icon: "🗺️" },
  { min: 40, title: "Seasoned Traveler", icon: "✈️" },
  { min: 60, title: "Globe Trotter", icon: "🌎" },
  { min: 80, title: "World Adventurer", icon: "🌟" },
  { min: 90, title: "Travel Master", icon: "👑" },
] as const;

export function getRank(score: number) {
  return RANKS.reduce((prev, curr) => (score >= curr.min ? curr : prev));
}
