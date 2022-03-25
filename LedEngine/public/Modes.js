var socket = io();

var rowX = 0;
var rowY = 0;

var lastClickedMode = ""

window.addEventListener("load", function()
{
  if(('ontouchstart' in window) || (navigator.MaxTouchPoints > 0) || (navigator.msMaxTouchPoints > 0)) 	
  {
    //mobile
    document.addEventListener("touchstart", ReportTouchStart, false);
    document.addEventListener("touchend", ReportTouchEnd, false);
    document.addEventListener("mousedown", ReportMouseDown, false);
  }
  else
  {
    //desktop
    document.addEventListener("touchstart", ReportTouchStart, false);
    document.addEventListener("touchend", ReportTouchEnd, false);
    document.addEventListener("mousedown", ReportMouseDown, false);
  }
  
});

function ReportOnMouseDown(e) 
{
  socket.emit('msg','{"'+e.target.id+'":1}');
}

function ReportTouchStart(e) 
{
	if (e.target.className != "serialtext") 
  { 
		e.preventDefault();
	}
	if (e.target.className != 'range-slider') 
  {
		socket.emit('msg','{"'+e.target.id+'":1}');
	}
}

function ReportTouchEnd(e) 
{
  if (e.target.id == 'A1')
  {
    e.preventDefault(); 
  } 
  else
  {
    socket.emit('msg','{"'+e.target.id+'":0}');
  }
}

function ReportMouseDown(e) 
{
  if (e.target.className != 'range-slider') 
  {
    socket.emit('msg','{"'+e.target.id+'":1}');
  }
}

var ConsoleText = "";

socket.on('FB',function (data) {  
  console.log('DataFromServer'+data.toString()+'!');
  var obj2 = JSON.parse(data.toString()); // convert to json
  var keys = Object.keys(obj2);
  var result = Object.keys(obj2).map(function(e) {
    return obj2[e]
  })
  var id = keys[0];
  
  if (id != null) {
    if(document.querySelector('#' + id) != null) {
      console.log(document.querySelector('#' + id));
      var className = document.querySelector('#' + id).className;
      if (className !== null) { // this object as a classname
	      console.log('id='+id+'; className='+className)+" value="+result;	
        if (id == 'rainbowSpeedSlider') {
	        document.getElementById(id).value = result;
	      } else if (id == 'A1'){
          document.getElementById(id).value = result;
        }
        else if (id == 'WireWorldEmpty')
        {
          SetColor('#000000');
          SetMode(0);
        }
        else if (id == 'WireWorldConductor')
        {
          SetColor('#FFBC42');
          SetMode(1);
        }
        else if (id == 'WireWorldElectronHead')
        {
          SetColor('#0000FF');
          SetMode(2);
        }
        else if (id == "WireWorldElectronTail")
        {
          SetColor('#FF0000');
          SetMode(3);
        }
        else if (id == "SineWave")
        {
          CollapseAllMenus();
          var dropdown = document.getElementById("dropdown-container");
          dropdown.classList.toggle("active");
          if (dropdown.style.display === "block") {
            dropdown.style.display = "none";
          } else {
            dropdown.style.display = "block";
          } 
          lastClickedMode = "SineWave.Start"
        }
        else if (id == "FireEffect")
        {
          CollapseAllMenus();
          lastClickedMode = "Fire.Start"
        }
        else if (id == "StarsEffect")
        {
          CollapseAllMenus();
          var dropdown = document.getElementById("dropdown-StarsEffect");
          dropdown.classList.toggle("active");
          if (dropdown.style.display === "block") {
            dropdown.style.display = "none";
          } else {
            dropdown.style.display = "block";
          } 
          lastClickedMode = "Stars.Start"
        }
        else if (id == "KnightRider")
        {
          CollapseAllMenus();
          var dropdown = document.getElementById("dropdown-KnightRider");
          dropdown.classList.toggle("active");
          if (dropdown.style.display === "block") {
            dropdown.style.display = "none";
          } else {
            dropdown.style.display = "block";
          } 
          lastClickedMode = "KnightRider.Start"
        }
        else if (id == "DisplayText")
        {
          CollapseAllMenus();
          var dropdown = document.getElementById("dropdown-DisplayText");
          dropdown.classList.toggle("active");
          if (dropdown.style.display === "block") {
            dropdown.style.display = "none";
          } else {
            dropdown.style.display = "block";
          } 
          lastClickedMode = "DisplayText.Start"
        }
      }
    }
    else if (id == 'JSONdata')
    {
      if (obj2.JSONdata[0].LEDPanelHeight && obj2.JSONdata[0].LEDPanelWidth && obj2.JSONdata[0].amountOfPanelsInWidth && obj2.JSONdata[0].amountOfPanelsInHeight)
      {
        rowX = obj2.JSONdata[0].LEDPanelWidth * obj2.JSONdata[0].amountOfPanelsInWidth;
        rowY = obj2.JSONdata[0].LEDPanelHeight * obj2.JSONdata[0].amountOfPanelsInHeight;
        setup2();
      }
      if (obj2.JSONdata[0].brightnessValue)
      {
        document.getElementById("LedController.SetBrightness").value = obj2.JSONdata[0].brightnessValue;
      }
    }
  }
});

function CollapseAllMenus()
{
  var dropdown0 = document.getElementById("dropdown-container");
  var dropdown1 = document.getElementById("dropdown-StarsEffect");
  var dropdown2 = document.getElementById("dropdown-KnightRider");
  var dropdown3 = document.getElementById("dropdown-DisplayText");
  dropdown0.style.display = "none";
  dropdown1.style.display = "none";
  dropdown2.style.display = "none";
  dropdown3.style.display = "none";
}

function SetColor(colorValue)
{
  col = colorValue
}

function SetMode(value)
{
  mode = value
}

function SpeedInputChanged(e){
  // this updates the brightness slider value
  if (e.value != 0)
  {
    var sliderValue = document.getElementById("SpeedInput");
    sliderValue.innerHTML = e.value;
    socket.emit('msg','{"SpeedInput":'+e.value+'}');
  }
}

function waitForElement()
{
  if(typeof rowX !== 0)
  {
    console.log(rowX);
    return rowX
  }
  else
  {
    setTimeout(waitForElement, 250);
  }
}

function Start()
{
  //here we read the json file for the previous settings
  socket.emit('msg','{"RequestJSONdata":"1"}');
}
Start();

var grid = [];
var col = ('#000000');
var mode = 0; // 0 = off, 1 = conductor, 2 = electron Head, 3 = electron tail

function PixelColorChanged(e)
{
  //updates the value of the pixel to draw
  col = e.value;
}

function setup(){} //p5js setup

function setup2()
{
  console.log("start setup");
  Xwidth = waitForElement();
  if (Xwidth != 0 || rowY != 0)
  {
    canvas = createCanvas(8 * rowX, 8 * rowY);
    canvas.parent('canvasPanel');
    background(120);
    var row = new Array(rowY).fill('#000000');
    for (let i = 0; i < Xwidth; i++) 
    {
      grid[i] = row;
    }
    colorMode(RGB)
    renderBoard();
    //background(255, 204, 0);
  }
  else
  {
    document.getElementById("noSizeSpecified").value = "Please enter LED-Panel size in setup"
  }
}

function Clear()
{
  //clear the drawn pixels
  renderBoard();
  //clears the pixels from the array
  var row = new Array(rowY).fill('#000000');
  for (let i = 0; i < rowX; i++) 
  {
    grid[i] = row;
  }
}

function mousePressed() 
{

  let spotX = floor(mouseX / (width / rowX));
  let spotY = floor(mouseY / (height / rowY));
  if (spotX >= 0 && spotX <= rowX && spotY >= 0 && spotY <= rowY)
  {
    drawPixel(spotX, spotY, col);
    // send changed pixel to python program
    var object = {  setPixelWireWorld: { X: spotX, Y: spotY, mode: mode}}

    socket.emit('msg',JSON.stringify(object));
  }
  
  else
  {
    let spotX = floor(mouseX / (width / rowX));
    let spotY = floor(mouseY / (height / rowY));
    if (spotX >= 0 && spotX <= rowX && spotY >= 0 && spotY <= rowY)
    {
      var hex = grid[spotX][spotY];
      SetColor(hex);
    }
  }
}

function renderBoard()
{
  for (let x = 0; x < rowX; x++) 
  {
   for (let y = 0; y < rowY; y++) 
   {
    stroke(50, 50, 50);
    strokeWeight(1);
    fill("#000000");
    rect(x*(width / rowX),y*(height / rowY), width / rowX, height / rowY);
  }
 }
}

function drawPixel(spotX, spotY, pickedColor)
{
  //add pixel to grid
  //adding a pixel like this: "grid[spotX][spotY] = col" sets the whole row for some reason
  //so we just create a array and add the whole array to the grid array
  //There must be a better way so please improve my code here:
  gridY = []
  for (let i = 0; i < rowY; i++)
  {
    if (spotY != i)
    {
      gridY.push(grid[spotX][i]);
    }
    else
    {
      gridY.push(pickedColor);
    }
  }
  grid[spotX] = gridY;
  fill(color(grid[spotX][spotY]));
  rect(spotX*(width / rowX),spotY*(height / rowY), width / rowX, height / rowY);
}

var oneColorEffect

function effecthexChanged(e)
{ 
  console.log(e.id);
  socket.emit('msg',JSON.stringify({ effecthexChanged: e.value }));
}

function valueObjectChanged(e)
{ 
  if (e.value != "")
  {
    var element = document.getElementById(e.id);
    element.innerHTML = e.value;
    socket.emit('msg',JSON.stringify({ valueChanged: {objectID : e.id, objectValue : e.value} }));
  }
}

function ExecuteFunction(e)
{ 
  if (e.id == "StartOneColorMode")
  {
    socket.emit('msg',JSON.stringify({ ExecuteFunction: lastClickedMode }));
    return
  }
  else 
  {
    socket.emit('msg',JSON.stringify({ ExecuteFunction: e.id }));
  }
}

function StopProcesses()
{ 
  socket.emit('msg',JSON.stringify({ "StopProcesses": 1 }));
}

function SetOneValue(e)
{
  if (e.value != "")
  {
    socket.emit('msg', JSON.stringify({ SetOneValueFunction: e.id, value : e.value}));
  }
}