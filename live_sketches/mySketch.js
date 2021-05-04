// need acceleration/velocity decay, transparency?, color

let particles = [];
let attractor;
let padding;
let mouseCharge;
let velDecay;

function setup() {
	createCanvas(windowWidth, windowHeight);
	background(0);
	velDecay = 0.999;
	for (let i = 0; i < 100; i++) {
		let p = new Particle()
		particles.push(p)
	}
	//attractor = createVector(200,200)
	
}

function draw() {
	
	////taken from frozen brush, make the lines fade
	//noStroke();
  //fill(0, 20);
  //rect(0, 0, width, height);
	
	for (let i = 0; i < particles.length; i ++){
		//for (let j = 0; j < attractors.length; j ++) {
		//particles[i].attracted(attractor);
		particles[i].attracted()
		//}
		particles[i].update();
		particles[i].render();
	}
	fill('white')
	noStroke();
	textSize(15)
	text("Press any key to clear the screen", width/2-((width/2)*0.1), 30)
	text("Click and hold to repel the particles", width/2-((width/2)*0.1), 50)
}
function keyPressed() {
	clear();
}
class Particle{
	constructor(){
		let x = random(width)
		let y = random(height)
		this.loc = createVector(x, y)//new PVector(random(width), random(height))
		this.prev = createVector(x, y) //coding trains way of making tails that isn't quite working
		this.vel = createVector() 
		this.acc = createVector() 
		this.size = random(1,3);
		this.padding = 3;
		this.mouseCharge = 4; //increase value to increase velocity
		//this.charge = 0.05; not currently using
    //this.mass = 1.0; a given that mass is 1
	}
	
	render() {
		var col = mag(this.vel.x, this.vel.y);
    //fill(col, col*50, col*200);
		//ellipse(this.loc.x,this.loc.y,this.size)
		stroke(col, col*50, col*150);
		strokeWeight(this.size);
		line(this.loc.x, this.loc.y, this.prev.x, this.prev.y) //coding train
		this.prev.x = this.loc.x;
    this.prev.y = this.loc.y;
		
		
		//// bounce off walls
		if ((this.loc.x > width) || (this.loc.x < 0)) {
		this.vel.x = this.vel.x * -1;
		}
		if ((this.loc.y > height) || (this.loc.y < 0)) {
		this.vel.y = this.vel.y * -1;
		}
    
	}
	update() {
		this.loc.add(this.vel);
		//this.vel.add(this.acc);
		//this.vel.limit(5);
		//this.acc.mult(0);
	}
	
	attracted(target){
		//// coding train force
		// var force = p5.Vector.sub(target, this.loc)
		// var d = force.mag()
		// d = constrain(d, 1, 25);
		// var G = 0.05;
		// var strength = G/(d*d)
		// strength = constrain(strength,1,20)
		// force.setMag(strength)
		// //if (d<20){
		// 	//force.mult(-20);
		// //}
		// this.acc.add(force);
	
		// from Nbody interact with mouse force
    var dx = this.loc.x - mouseX;
    var dy = this.loc.y - mouseY;
    var d = sqrt(dx*dx+dy*dy)+this.padding;
    var f = this.mouseCharge/(d*d);
    if (mouseIsPressed) f = -f;
  	this.vel.x -= dx * f;
    this.vel.y -= dy * f;
    
    // Velocity decay
    this.vel.x *= velDecay;
    this.vel.y *= velDecay;
		
		
	}
}

