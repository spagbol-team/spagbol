/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'main-bg-color': {
          DEFAULT: 'rgb(52, 53, 65)',
        },
        'secondary-bg-color': {
          DEFAULT: 'rgb(55, 57, 70)',
        },
        'third-bg-color': {
          DEFAULT: 'rgb(236, 236, 241)',
        },
        'bg-image': {
          DEFAULT: 'linear-gradient(45deg, rgb(62, 64, 80), rgb(55, 56, 70))',
        },
        'box-shadow': {
          DEFAULT: 'rgba(26, 27, 39, 0.68) 0px 0px 4px 0px',
        },
        'color': {
          DEFAULT: 'rgb(139, 140, 152)',
          'color2': 'rgb(153, 155, 182)',
        },
        'highlight-text-color': {
          DEFAULT: 'rgb(255, 87, 34)',
        },
        'highlighting-bg-image': {
          DEFAULT: 'linear-gradient(45deg, rgb(244, 67, 54), rgba(0, 0, 0, 0))',
        },
        'white-bg-color': {
          DEFAULT: 'rgb(236, 236, 241)',
        },
        'active-color': {
          DEFAULT: 'rgb(255, 255, 255)',
        },
        'active-border-color': {
          DEFAULT: 'rgb(200, 201, 211)',
        },
      },
    },
  },
  plugins: [],
}

