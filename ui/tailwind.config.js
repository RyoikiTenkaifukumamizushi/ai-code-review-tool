module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
    "./public/index.html"
  ],
  theme: {
    extend: {
      animation: {
        'border-glow': 'glow 1.5s infinite ease-in-out',
        'border-light': 'trail 2s infinite ease-in-out',
      },
      keyframes: {
        glow: {
          '0%, 100%': { borderColor: 'transparent' },
          '50%': { borderColor: '#60a5fa' }
        },
        trail: {
          '0%': { opacity: 0 },
          '50%': { opacity: 0.7 },
          '100%': { opacity: 0 },
        },
      },
    },
  },
  plugins: [],
}
