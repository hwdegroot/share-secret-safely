/** @type {import('tailwindcss').Config} */
module.exports = {
    darkMode: 'class',
    content: [
        './wsgi_app/templates/**/*.{html,js,svg}',
    ],
    theme: {
        extend: {},
    },
    plugins: [],
}

