var socket = io(); 

var rowX = 0;
var rowY = 0;

Start();

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
    //socket.emit('msg','{"'+e.target.id+'":1}');
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
  var result = Object.keys(obj2).map(function(e) 
  {
    return obj2[e]
  })
  var id = keys[0];
  if (id != null && id != "") 
  {
    if(document.querySelector('#' + id) != null) 
    {
      console.log(document.querySelector('#' + id));
      var className = document.querySelector('#' + id).className;
      if (className !== null) 
      { // this object as a classname
	      console.log('id='+id+'; className='+className)+" value="+result;	
        if (id == 'rainbowSpeedSlider') 
        {
	        document.getElementById(id).value = result;
	      } 
        else if (id == 'A1')
        {
          document.getElementById(id).value = result;
        }
        else if (id == 'PixelPicker')
        {
          PickColor();
        }
        else if (id == 'color0')
        {
          SetColor('#FFBC42');
        }
        else if (id == 'color1')
        {
          SetColor('#D81159');
        }
        else if (id == 'color2')
        {
          SetColor('#8F2D56');
        }
        else if (id == 'color3')
        {
          SetColor('#218380');
        }
        else if (id == 'color4')
        {
          SetColor('#73D2DE');
        }
        else if (id == 'ClearPixels')
        {
          Clear();
        }
        else if (id == 'searchImages')
        {
          ResetNames();
        }
      }
    }
    else if (id == 'X')
    {
      function ColorToHex(color) {
        var hexadecimal = color.toString(16);
        return hexadecimal.length == 1 ? "0" + hexadecimal : hexadecimal;
      }
      function ConvertRGBtoHex(red, green, blue) {
        return "#" + ColorToHex(red) + ColorToHex(green) + ColorToHex(blue);
      }
      drawPixel(result[0], result[1], ConvertRGBtoHex(result[2], result[3], result[4]));
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
    else if (id == 'LoadableImageName')
    {
      AddName(result);
    }
  }
});

function SetColor(colorValue)
{
  document.getElementById("PixelColorPicker").value = colorValue; //set the color of the color picker
  col = colorValue //even though the value of the color picker is changed we still need to update it manually
}

function valueChanged(e){
  let a = e.value;

  // this updates the brightness slider value
  var sliderDiv = document.getElementById("A1");
  sliderDiv.innerHTML = a;

  socket.emit('msg','{"A1":'+a+'}');
}

function WaveLengthInputChanged(e)
{
  // this updates the brightness slider value
  if (e.value != 0)
  {
    var sliderValue = document.getElementById("WaveLengthInput");
    sliderValue.innerHTML = e.value;
    socket.emit('msg','{"WaveLengthInput":'+e.value+'}');
  }
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
var pickColor = new Boolean(false);
function PickColor()
{
  pickColor = true;
}

//part for pixel drawer
var grid = [];
var col = ('#000000');

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

    for (var i = 0; i < rowY; i++) {
      grid[i] = Array(Xwidth).fill('#000000');
    }

    colorMode(RGB);
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
    grid[i] = row.slice();
  }
}

function mouseDragged() 
{
  if (pickColor == false)
  {
    let spotX = floor(mouseX / (width / rowX));
    let spotY = floor(mouseY / (height / rowY));
    if (spotX >= 0 && spotX <= rowX && spotY >= 0 && spotY <= rowY)
    {
      drawPixel(spotX, spotY, col);
      // send changed pixel to python program
      //socket.emit('msg',JSON.stringify('{"a":'+'[{'+"X:"+spotX+','+"Y:"+spotY+','+"color:"+col+'}]'+'}'));
      var object = {  SetValueFunction: "DrawingCanvas.setPixel", args : { X: spotX, Y: spotY, color: col}}

      socket.emit('msg',JSON.stringify(object));
    }
  }
  else if (pickColor)
  {
    let spotX = floor(mouseX / (width / rowX));
    let spotY = floor(mouseY / (height / rowY));
    if (spotX >= 0 && spotX <= rowX && spotY >= 0 && spotY <= rowY)
    {
      var hex = grid[spotX][spotY];
      SetColor(hex);
      pickColor = false;
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
  console.log("Set the picked color", grid, spotX, spotY);
  console.log("Set the picked color", grid[spotX][spotY]);
  grid[spotX][spotY] = pickedColor;
  fill(color(grid[spotX][spotY]));
  rect(spotX*(width / rowX),spotY*(height / rowY), width / rowX, height / rowY);
}

var names = []

function AddName(name)
{
  names.push(name);
  var btn = document.createElement("BUTTON");
  btn.innerHTML = name;
  btn.id = name;
  btn.onclick = function(){
    socket.emit('msg','{"DisplayImage":"'+name+'"}');
  };
  document.querySelector('ul2').appendChild(btn);
}

function ResetNames()
{
  names = [];
}

//only used for debugging
//Note: this doesnt refresh the led panel
function refresh()
{
  for (let x = 0; x < rowX; x++)
  {
    for (let y = 0; y < rowY; y++)
    {
      fill(color(grid[x][y]));
      rect(x*(width / rowX),y*(width / rowY),width / rowX,height / rowX);
    }
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

function ExecuteFunction(e)
{ 
  socket.emit('msg',JSON.stringify({ ExecuteFunction: e.id }));
}

function ClearPanel(e)
{ 
  socket.emit('msg',JSON.stringify({ ExecuteFunction: e.id }));
  Clear()
}

function SetValue(e)
{
  socket.emit('msg', JSON.stringify({  SetValueFunction: e.id, args : { arg0: e.value}}));
}

function SetOneValue(e)
{
  if (e.value != "")
  {
    socket.emit('msg', JSON.stringify({ SetOneValueFunction: e.id, value : e.value}));
  }
}

function StopProcesses()
{ 
  socket.emit('msg',JSON.stringify({ "StopProcesses": 1 }));
}