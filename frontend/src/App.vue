<script>
	// import axios from "axios";
	export default {
		data() {
			return {
				columns: [],
				data: null,
				rowIndex: null,
				picked: null,
				newValue: { id: '', name: '', quantity: '', price: '', vat: '', margin: '' },
				updateValue: { id: '', name: '', quantity: '', price: '', vat: '', margin: '' },
			}
		},
		methods: {
			async fetchData(endpoint) {
				try {
					const response = await this.axios.get(endpoint)
					this.data = response.data
					this.columns = this.data.data.length && Object.keys(this.data.data[0])
				} catch (error) {
					console.error('Vue - Error fetching data:', error)
				}
			},
			async fetchDataProductsTable() {
				await this.fetchData('/api/products')
			},
			async insertData(endpoint, payload) {
				try {
					const response = await this.axios.post(endpoint, payload, {
						headers: {
							'Content-Type': 'application/json',
						},
					})
					console.log('Data sent successfully:', response.data)
					await this.fetchData(endpoint)
				} catch (error) {
					console.error('Vue - Error sending data:', error)
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
					console.error('Vue - Error deleting data:', error)
				}
			},
			async updateData(endpoint, payload) {
				try {
					const response = await this.axios.put(endpoint, payload, {
						headers: {
							'Content-Type': 'application/json',
						},
					})
					console.log('Data updated successfully:', response.data)
					await this.fetchData(endpoint)
				} catch (error) {
					console.error('Vue - Error updating data:', error)
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
		</div>
		<div id="table">
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
		<section id="reaction">
			<div v-if="data">
				<h2>Choose the reaction:</h2>

				<input type="radio" id="insert" value="Insert a record" v-model="picked" />
				<label for="insert">Insert a record</label>

				<input type="radio" id="delete" value="Delete a record" v-model="picked" />
				<label for="delete">Delete a record</label>

				<input type="radio" id="update" value="Update a record" v-model="picked" />
				<label for="update">Update a record</label>
			</div>
			<div>
				<h2 v-if="picked">Picked: {{ picked }}</h2>

				<div v-if="data && picked === 'Insert a record'">
					<input type="text" placeholder="name" v-model="newValue.name" />
					<input type="text" placeholder="quantity" v-model="newValue.quantity" />
					<input type="text" placeholder="price" v-model="newValue.price" />
					<input type="text" placeholder="vat" v-model="newValue.vat" />
					<input type="text" placeholder="margin" v-model="newValue.margin" />
					<button class="dataHandlingBtn" @click="insertData('/api/products', newValue)">
						INSERT the data - products table
					</button>
				</div>
				<div v-if="data && picked === 'Delete a record'">
					<input type="text" placeholder="enter ProductID" v-model="newValue.id" />
					<button class="dataHandlingBtn" @click="deleteData('/api/products', newValue)">
						DELETE the data from products table
					</button>
				</div>
				<div v-if="data && picked === 'Update a record'">
					<label>Which record do you want to update?</label>
					<input type="text" placeholder="id" v-model="updateValue.id" />
					<label>Enter new data:</label>
					<input type="text" placeholder="name" v-model="updateValue.name" />
					<input type="text" placeholder="quantity" v-model="updateValue.quantity" />
					<input type="text" placeholder="price" v-model="updateValue.price" />
					<input type="text" placeholder="vat" v-model="updateValue.vat" />
					<input type="text" placeholder="margin" v-model="updateValue.margin" />
					<button class="dataHandlingBtn" @click="updateData('/api/products', updateValue)">
						UPDATE the data - products table
					</button>
				</div>
			</div>
		</section>
	</div>
	<!-- <router-view /> -->
</template>

<style lang="scss">
	#app {
		font-family: Avenir, Helvetica, Arial, sans-serif;
		-webkit-font-smoothing: antialiased;
		-moz-osx-font-smoothing: grayscale;
		font-size: 16px;
		text-align: center;
		color: #2c3e50;
		width: 100%;

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
			width: calc(100% - 10px);
			padding: 10px;
			margin: 5px;
			border-radius: 4px;
			border: none;
			cursor: pointer;
			background-color: #42b983;
			color: white;
			&:hover {
				background-color: #2c3e50;
			}
		}

		table {
			display:inline-block;
			width: 810px;
			height: 400px;
			overflow-y: auto;
			resize: vertical;
			border-collapse: collapse;
			margin: 20px 0;

			> thead {
				text-transform: uppercase;
				background-color: cornflowerblue;
				color: white;
				position: sticky;
				top: 0;
				z-index: 2;
				th {
					padding: 10px;
					border: 1px solid #ddd;
				}
			}

			> tbody {
				tr {
					width: 100%;
				}
				tr:nth-child(even) {
					background-color: lightcyan;
				}

				tr:nth-child(odd) {
					background-color: white;
				}

				td {
					padding: 10px;
					border: 1px solid #ddd;
					text-align: center;
				}
			}
		}

		#reaction {
			display: flex;
			margin: 20px 25vw;
			align-items: flex-start;
			justify-content: space-evenly;

			div:first-of-type {
				display: grid;
				grid-template-columns: 0.4fr 1fr;
				align-items: baseline;
				justify-items: start;
				margin: 20px auto;

				h2 {
					grid-column: 1 / -1;
				}
				input {
					grid-column: 1;
				}
				label {
					grid-column: 2;
				}
			}

			div:nth-child(2) {
				display: flex;
				flex-direction: column;
				align-items: stretch;
				width: 70%;
				margin: auto;
				input {
					margin-top: 5px;
				}
				label {
					margin-top: 5px;
				}
				button {
					width: 100%;
					margin: 10px 0;
				}
			}
		}
	}
</style>
