export const calculateTotalCarbon = (logs) => {
  return logs.reduce((total, log) => total + log.carbon, 0);
};

export const classifyCarbon = (value) => {
  if (value === 0) return "Eco-Friendly";
  if (value < 5) return "Moderate";
  return "High Impact";
};