import { createApp } from "vue";
import App from "./App.vue";
import "./registerServiceWorker";
import router from "./router";
import axios from "axios";
const APP = createApp(App);
APP.config.globalProperties.axios = axios;
APP.use(router).mount("#app");
