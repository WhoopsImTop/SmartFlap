const tf = require('@tensorflow/tfjs');
const nodeTf = require('@tensorflow/tfjs-node');
const fs = require('fs');

const TARGET_CLASSES = {
  0: "Katze",
  1: "Mit Maus",
  2: "Mit Vogel",
  3: "Weg"
};

async function predict() {
let model;
	try {
    	model = await tf.loadGraphModel('file://./model/model.json');
	} catch(e) {
		console.log("ERROR:", e);
	}

	const img = fs.readFileSync('./pictures/picture.jpg');
        let tensor = nodeTf.node.decodeImage(img, 3)
		.resizeNearestNeighbor([224, 224])
		.expandDims()
		.toFloat()
	let predictions = await model.predict(tensor).data();
	
	let top5 = Array.from(predictions)
	console.log(top5)
		.map(function (p, i) { // this is Array.map
			return {
				probability: p,
				label: TARGET_CLASSES[i] // we are selecting the value from the obj
			};
		}).sort(function (a, b) {
			return b.probability - a.probability;
		});+
	console.log(JSON.stringify(top5[0].label + ' ' + top5[0].probability))
};

predict();
