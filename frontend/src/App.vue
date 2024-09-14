<script>
	// import axios from "axios";
	export default {
		data() {
			return {
				columns: [],
				data: null,
				rowIndex: null,
				picked: null,
				newValue: {id: '', name: '', quantity: '', price: '', vat: '', margin: '' },
			}
		},
		methods: {
			async fetchData(endpoint) {
				try {
					const response = await this.axios.get(endpoint)
					this.data = response.data
					this.columns = this.data.data.length && Object.keys(this.data.data[0])
				} catch (error) {
					console.error('Error fetching data:', error)
				}
			},
			async fetchDataProductsTable() {
				await this.fetchData('/api/products')
			},
			// async fetchDataCustomersTable() {
			// 	await this.fetchData('/api/customers')
			// },
			// async fetchDataOrdersTable() {
			// 	await this.fetchData('/api/orders')
			// },
			async sendData(endpoint, payload) {
				try {
					const response = await this.axios.post(endpoint, payload, {
						headers: {
							'Content-Type': 'application/json',
						},
					})
					console.log('Data sent successfully:', response.data)
					await this.fetchData(endpoint)
				} catch (error) {
					console.error('Error sending data:', error)
				}
			},
			async deleteData(endpoint, payload) {
				try {
					const response = await this.axios.delete(endpoint, {
						headers: {
							'Content-Type': 'application/json',
						},
						data: payload,
					})
					console.log('Data deleted successfully:', response.data)
					await this.fetchData(endpoint)
				} catch (error) {
					console.error('Error deleting data:', error)
				}
			},
		},
	}
</script>

<template>
	<div>
		<nav>
			<router-link to="/">Home</router-link>
			|
			<router-link to="/about">About</router-link>
		</nav>
		<div>
			<button class="dataFetchingBtn" @click="fetchData('/api/products')">GET the data - products table</button>
			<!-- <button class="dataFetchingBtn" @click="fetchData('/api/customers')">GET the data - customers table</button>
			<button class="dataFetchingBtn" @click="fetchData('/api/orders')">GET the data - orders table</button> -->
		</div>
		<div>
			<h2 v-if="data">Fetched Data:</h2>
			<table v-if="data">
				<thead>
					<tr>
						<th v-for="(column, index) in data.columns" :key="index">
							{{ column }}
						</th>
					</tr>
				</thead>
				<tbody>
					<tr v-for="(row, rowIndex) in data.data" :key="rowIndex">
						<td v-for="(item, itemIndex) in row" :key="itemIndex">
							{{ item }}
						</td>
					</tr>
				</tbody>
			</table>
		</div>
		<div v-if="data">
			Choose the reaction:
			<div>Picked: {{ picked }}</div>

			<input type="radio" id="insert" value="Insert a record" v-model="picked" />
			<label for="insert">Insert a record</label>

			<input type="radio" id="delete" value="Delete a record" v-model="picked" />
			<label for="delete">Delete a record</label>

			<input type="radio" id="refresh" value="Refresh the table" v-model="picked" />
			<label for="refresh">Refresh the table</label>
		</div>
		<div v-if="(data, picked === 'Insert a record')">
			<input type="text" placeholder="name" v-model="newValue.name" />
			<input type="text" placeholder="quantity" v-model="newValue.quantity" />
			<input type="text" placeholder="price" v-model="newValue.price" />
			<input type="text" placeholder="vat" v-model="newValue.vat" />
			<input type="text" placeholder="margin" v-model="newValue.margin" />
			<button class="dataHandlingBtn" @click="sendData('/api/products', newValue)">
				SEND the data - products table
			</button>
		</div>
		<div v-if="(data, picked === 'Delete a record')">
			<input type="text" placeholder="enter ProductID" v-model="newValue.id" />
			<button class="dataHandlingBtn" @click="deleteData('/api/products', newValue)">
				DELETE the data from products table
			</button>
		</div>
		<div v-if="(data, picked === 'Update a record')">
			<input type="text" placeholder="name" v-model="newValue.name" />
			<input type="text" placeholder="quantity" v-model="newValue.quantity" />
			<input type="text" placeholder="price" v-model="newValue.price" />
			<input type="text" placeholder="vat" v-model="newValue.vat" />
			<input type="text" placeholder="margin" v-model="newValue.margin" />
			<button class="dataHandlingBtn" @click="updateData('/api/products', newValue)">
				UPDATE the data - products table
			</button>
		</div>
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

		button {
			padding: 10px;
			margin: 5px;

			&.dataFetchingBtn {
				width: 80%;
			}

			&.tableUpdatingBtn {
				width: 60px;
			}
		}

		table {
			width: 100%;
			padding: 10px;
			margin: 5px;

			> thead {
				text-transform: uppercase;
				height: 30px;
				background-color: cornflowerblue;
			}

			> tbody tr:nth-child(even) {
				background-color: lightcyan;
			}
		}
	}
</style>
