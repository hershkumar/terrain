
height = 100;
width = 100;
heightAmplification = 50;
let gen = new SimplexNoise();

function noise(nx, ny) {
  // Rescale from -1.0:+1.0 to 0.0:1.0
  return gen.noise2D(nx, ny) / 2 + 0.5;
}

function ridgenoise(nx, ny) {
	return 2 * (0.5 - Math.abs(0.5 - noise(nx, ny)));
}

let elevation = [];   
for (let y = 0; y < height; y++) {
	elevation[y] = [];
	for (let x = 0; x < width; x++) {      
		let nx = x/width - 0.5, ny = y/height - 0.5;
		e =1 * noise(1 * nx, 1 * ny)	
		+  0.5 * noise(2 * nx, 2 * ny)
		+ 0.25 * noise(4 * nx, 4 * ny);
		elevation[y][x] = Math.pow(e, 1.48);
	}
}


elevation2 = [];
for (let i = 0; i < elevation.length; i++){
	for (let j = 0; j < elevation[i].length; j++){
		elevation2.push(elevation[i][j]);
	}
}
var scene = new THREE.Scene();
var camera = new THREE.PerspectiveCamera( 75, window.innerWidth / window.innerHeight, 0.1, 1000 );
var renderer = new THREE.WebGLRenderer();

renderer.shadowMap.enabled = true;
renderer.setSize( window.innerWidth, window.innerHeight );
document.body.appendChild( renderer.domElement );
function addLight(...pos) {
	const color = 0xFFFFFF;
	const intensity = 1;
	const light = new THREE.DirectionalLight(color, intensity);
	light.position.set(...pos);
	scene.add(light);
}

addLight(-1, 2, 4);
addLight(1, 2, -2);

//the real terrain making
var geo = new THREE.PlaneGeometry(width, height, elevation.length -1, elevation.length - 1);
geo.computeFaceNormals();
geo.computeVertexNormals();
var mat = new THREE.MeshPhongMaterial({
	color: 'green',
	wireframe: false
});
mat.castShadows = true;
mat.receiveShadows = true;

var terrain = new THREE.Mesh(geo, mat);
for (var i = 0, l = geo.vertices.length; i < l; i++){
	var terrainValue = elevation2[i];
	geo.vertices[i].z = geo.vertices[i].z + terrainValue * heightAmplification;
}


var controls = new THREE.OrbitControls(camera, renderer.domElement);
camera.position.z = 250;
controls.update();
scene.add(terrain);

terrain.rotation.z = 90;
function animate() {
	requestAnimationFrame( animate );
	renderer.render( scene, camera );
}
animate();