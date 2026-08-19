/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        ink: "#12233D",       // deep navy — headers, nav, hero sections
        paper: "#FAF6EE",     // cream — page background
        parchment: "#F1E9D8", // slightly darker cream — cards
        accent: "#E2892D",    // orange — buttons, highlights, active states
        // legacy names kept as aliases so existing components (which use
        // brass/burgundy/forest classes) render as the single new accent
        // color without needing every file edited individually.
        brass: "#E2892D",
        burgundy: "#E2892D",
        forest: "#E2892D",
      },
      fontFamily: {
        display: ["'Fraunces'", "Georgia", "serif"],
        body: ["'Inter'", "system-ui", "sans-serif"],
      },
    },
  },
  plugins: [],
};