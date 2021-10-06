const express = require('express')
const fs = require('fs')

const app = express()

app.use('/uploads', express.static('/home/pi/Desktop/tfjs-customvision/static/pictures/'))
app.get('/logs', async (req, res) => {
	const data = fs.readFileSync('Katze.log', 'utf-8', (err, data) => {
	if(err) throw err;
	return data
	})
	res.json(data)
})

app.listen('3000', () => {
	console.log("Listening")
})
