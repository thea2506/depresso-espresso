

/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    colors: {
      primary: "#52796F",
      "secondary-light": "#84A98C",
      "secondary-dark": "#354F52",
      "accent-3": "#E8EDDF",
      "accent-2": "#BC4749",
      "accent-1": "#F5CB5C",
      black: "#242423",
      white: "#F9F9F9",
    },
  },
  plugins: [
    // eslint-disable-next-line no-undef
    require('@tailwindcss/typography'),
  ],
};
