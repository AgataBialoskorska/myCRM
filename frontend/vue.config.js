module.exports = {
  devServer: {
    proxy: {
      "/api/data": {
        target: "http://127.0.0.1:5000", // Adres serwera Flask
        changeOrigin: true,
        pathRewrite: {
          "^/api/data": "api/data",
        },
      },
    },
  },
};
