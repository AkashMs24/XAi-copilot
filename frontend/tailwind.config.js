/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      fontFamily: {
        display: ['"Syne"', 'sans-serif'],
        body: ['"DM Sans"', 'sans-serif'],
        mono: ['"JetBrains Mono"', 'monospace']
      },
      colors: {
        ink: '#0A0A0F',
        surface: '#111118',
        panel: '#1A1A25',
        border: '#2A2A3A',
        accent: '#6C63FF',
        'accent-soft': '#9B95FF',
        emerald: '#00D48A',
        crimson: '#FF4D6A',
        amber: '#FFB547',
        muted: '#6B7080'
      }
    }
  },
  plugins: []
}
