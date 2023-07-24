/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./templates/*.html"],
  theme: {
    extend: {
      colors: {
        chat_black: {50:'#343541'},
        left_color: {50:'#202123'},
        send: "#6b6c7b",
        bg_ans: "#444654"
      }
    }, 
  },
  plugins: [],
}

