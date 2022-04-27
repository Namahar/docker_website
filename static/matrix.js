var streams = [];
var symbolSize = 20;
var fadeInterval = 5;

function setup() {
	createCanvas(windowWidth, windowHeight);
	background(0);
	
	var x = 0;
	for (var i = 0; i <= width / symbolSize; i++) {
		var stream = new Stream();
		stream.generate(x, random(-2000, 0));
		streams.push(stream);
		x += symbolSize;
	}
	
	textFont('Consolas');
	textSize(symbolSize);
}

function draw() {
	background(0, 150);
	for (var i = 0; i < streams.length; i++) {
		streams[i].show();
	}
}

function Symbol(x, y, speed, first, opacity) {
	this.x = x;
	this.y = y;
	this.speed = speed;
	this.value;
	this.first = first;
	this.opacity = opacity;
	this.switchInterval = round(random(2, 25));
	
	this.setSymbol = function() {
		var charType = round(random(0, 5));
		if (frameCount % this.switchInterval == 0) {
			if (charType > 1) {
				this.value = String.fromCharCode(0x30A0 + round(random(0, 96)));
			}
			else {
				this.value = round(random(0, 9));
			}
		}
	}
	
	this.rain = function() {
		this.y = (this.y >= height) ? 0 : this.y += this.speed;
	}
}

function Stream() {
	this.symbols = [];
	this.numSymbols = round(random(5, 35));
	this.speed = random(5, 22);
	
	this.generate = function(x, y) {
		var first = true;
		var opacity = 255;
		for (var i = 0; i < this.numSymbols; i++) {
			symbol = new Symbol(x, y, this.speed, first, opacity);
			symbol.setSymbol();
			this.symbols.push(symbol);
			y -= symbolSize;
			opacity -= (255 / this.numSymbols) / fadeInterval;
			first = false;
		}
	}
	
	this.show = function() {
		for (var i = 0; i < this.symbols.length; i++) {
			if (this.symbols[i].first) {
				fill(140, 255, 170, this.symbols[i].opacity);
			}
			else {
				fill(0, 255, 70);
			}
			text(this.symbols[i].value, this.symbols[i].x, this.symbols[i].y);
			this.symbols[i].rain();
			this.symbols[i].setSymbol();
			
		}
	}
}

function windowResized() {
	resizeCanvas(windowWidth, windowHeight);
}