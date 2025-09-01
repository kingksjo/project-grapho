/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'background': '#000000',
        'surface': '#1c1c1e',
        'text-primary': '#ffffff',
        'text-secondary': '#8e8e93',
        'accent': '#007aff',
        'accent-hover': '#0056cc',
        'card-bg': '#2c2c2e',
        'ui-border': '#38383a',
      },
      fontFamily: {
        'sans': ['-apple-system', 'BlinkMacSystemFont', 'SF Pro Display', 'Segoe UI', 'Roboto', 'Helvetica Neue', 'Arial', 'sans-serif'],
      },
      backdropBlur: {
        'xs': '2px',
      }
    },
  },
  plugins: [],
}
