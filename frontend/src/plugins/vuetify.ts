/**
 * plugins/vuetify.ts
 *
 * Framework documentation: https://vuetifyjs.com`
 */

// Styles
import "@mdi/font/css/materialdesignicons.css";
import "vuetify/styles";

// Composables
import { createVuetify, ThemeDefinition } from "vuetify";

// https://vuetifyjs.com/en/introduction/why-vuetify/#feature-guides
export default createVuetify({
  theme: {
    defaultTheme: "YappyTheme",
    themes: {
      YappyTheme: {
        dark: true,
        colors: {
          background: "#1B1B1F",
          "on-surface": "red",
          surface: "#00E5BC",
          primary: "#00E5BC",
          secondary: "rgba(255, 255, 255, 0.40)",
        },
      },
    },
  },
});
