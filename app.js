const express = require('express');
const path = require('path');
const cors = require('cors');
const bodyParser = require('body-parser');
const jsonParser = bodyParser.json();
const jwt = require('jsonwebtoken');
const bcrypt = require('bcrypt');
const saltRounds = 10;
const { emitWarning } = require('process');
const { application } = require('express');
const { spawn } = require('child_process');
const formidable = require('formidable');
const fs = require('fs');
const multer = require('multer');

const app = express();
app.use(cors());
app.use(express.json());
app.use(
	multer({
		dest: __dirname + '/uploads/',
		//rename to test.xlsx
		rename: function (fieldname, filename) {
			return filename;
		}

	}).single('file')
);


const port = 8080;

app.get('/', (req, res) => {
  res.sendFile(__dirname + '/index.html');
});

app.post('/upload', (req, res) => {
	res.send(req.files);
});

app.get('/test', (req, res) => {
	let data1;
	const python = spawn('python3', ['test.py']);
	python.stdout.on('data', function (data) {
		console.log('Pipe data from python script ...');
		data1 = data.toString();
	});

	python.on('close', (code) => {
		console.log(`child process close all stdio with code ${code}`);
		console.log(data1);
		res.send(data1);
	});
});

// app.get('/test2/:fname/:lname', (req, res) => {
// 	let data1;
// 	const python = spawn('python3', ['test.py', req.params.fname, req.params.lname]);
// 	python.stdout.on('data', function (data) {
// 		console.log('Pipe data from python script ...');
// 		data1 = data.toString();
// 	});

// 	python.on('close', (code) => {
// 		console.log(`child process close all stdio with code ${code}`);
// 		console.log(data1);
// 		res.send(data1);
// 	});
// });

app.post('/testpost', jsonParser, (req, res, next) => {
	console.log(req.body);
	let data1;
	const python = spawn('python3', ['test.py', req.body.fname, req.body.lname]);
	python.stdout.on('data', function (data) {
		console.log('Pipe data from python script ...');
		data1 = data.toString();
	});

	python.on('close', (code) => {
		console.log(`child process close all stdio with code ${code}`);
		console.log(data1);
		res.send(data1);
	});
});

app.listen(port, () => {
	  console.log(`Example app listening at http://localhost:${port}`);
});
