const express = require('express')
const fs = require('fs')

const app = express()

app.use('/uploads', express.static('/home/pi/Desktop/tfjs-customvision/static/pictures/'))

app.listen('3000', () => {
	console.log("Listening")
})
