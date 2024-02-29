<script>
import axios from "axios";

export default {
  data() {
    return {
      columns: null,
      data: null,
    };
  },
  methods: {
    async fetchData() {
      try {
        const response = await axios.get("/api/data");
        this.data = response.data;
        if (this.data.data.length > 0) {
          this.columns = Object.keys(this.data.data[0]);
        } else {
          this.columns = [];
        }
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    },
  },
};
</script>
<template>
  <nav>
    <router-link to="/">Home</router-link> |
    <router-link to="/about">About</router-link>
  </nav>
  <div>
    <button @click="fetchData">GET the data</button>
    <h2 v-if="data">Fetched Data:</h2>
    <table v-if="data">
      <thead>
        <tr>
          <th v-for="(column, index) in this.data.columns" :key="index">
            {{ column }}
          </th>
        </tr>
      </thead>
      <tbody>
        <tr :key="0">
          <td v-for="(item, itemIndex) in this.data.data[0]" :key="itemIndex">
            {{ item }}
          </td>
        </tr>
        <tr
          v-for="(row, rowIndex) in this.data.data.slice(1)"
          :key="rowIndex + 1"
        >
          <td v-for="(item, itemIndex) in row" :key="itemIndex">
            {{ item }}
          </td>
        </tr>
      </tbody>
    </table>
  </div>
  <!-- <router-view /> -->
</template>

<style lang="scss">
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

nav {
  padding: 30px;

  a {
    font-weight: bold;
    color: #2c3e50;

    &.router-link-exact-active {
      color: #42b983;
    }
  }
}
</style>
