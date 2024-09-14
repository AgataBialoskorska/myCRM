module.exports = {
  devServer: {
    proxy: {
      "/api/products": {
        target: "http://127.0.0.1:5000",
        changeOrigin: true,
        pathRewrite: {
          "^/api/products": "api/products",
        },
      },
      "/api/customers": {
        target: "http://127.0.0.1:5000",
        changeOrigin: true,
        pathRewrite: {
          "^/api/customers": "api/customers",
        },
      },
      "/api/orders": {
        target: "http://127.0.0.1:5000",
        changeOrigin: true,
        pathRewrite: {
          "^/api/orders": "api/orders",
        },
      },
    },
  },
};
