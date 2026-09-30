/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        darkBg: "#0b0f19",
        cardBg: "rgba(23, 32, 54, 0.75)",
        cardBorder: "rgba(255, 255, 255, 0.08)",
        primaryIndigo: "#6366f1",
        emeraldGreen: "#10b981",
        roseRed: "#f43f5e",
        amberYellow: "#f59e0b",
      }
    },
  },
  plugins: [],
}
