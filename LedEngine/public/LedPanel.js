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
  }
  else
  {
    //desktop
    document.addEventListener("touchstart", ReportTouchStart, false);
    document.addEventListener("touchend", ReportTouchEnd, false);
    document.addEventListener("touchmove", ReportTouchMove, false);
    document.addEventListener("mousedown", ReportMouseDown, false);
  }
  
});

function ReportOnClick(e) 
{
  socket.emit('msg','{"'+e.target.id+'":2}');
}

function ReportOnDblClick(e) 
{
  socket.emit('msg','{"'+e.target.id+'":3}');
}

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
	if (e.target.className != "serialtext") 
  { 
		e.preventDefault();  
	}
	if (e.target.className != 'range-slider') 
  {  
		socket.emit('msg','{"'+e.target.id+'":0}');	
	}
	
}

function ReportTouchMove(e) 
{
	if (e.target.className != "serialtext") 
  {
		e.preventDefault();
	}
	socket.emit('TouchMove',e.offsetX,e.offsetY);
}

function ReportMouseDown(e) 
{
  if (e.target.className != 'range-slider') 
  {
    socket.emit('msg','{"'+e.target.id+'":1}');
  }
}

function ReportMouseUp(e) 
{
  if (e.target.className === 'range-slider') 
  {
    console.log("volume class detected");
  } else 
  {
      socket.emit('msg','{"'+e.target.id+'":0}');
  }
}

function ReportMouseMove(e) 
{
  socket.emit('TouchMove',e.offsetX,e.offsetY); 
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
        else if (id == 'ImageName')
        {
          AddName(result);
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
      if (obj2.JSONdata[0].LEDPanelHeight && obj2.JSONdata[0].LEDPanelWidth)
      {
        rowX = obj2.JSONdata[0].LEDPanelWidth;
        rowY = obj2.JSONdata[0].LEDPanelHeight;
        setup2();
      }
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

function ImageNameChanged(e)
{
  socket.emit('msg','{"ImageName":"'+e.value+'"}');
}

function setup(){} //p5js setup

function setup2()
{
  console.log("start setup");
  Xwidth = waitForElement();
  if (Xwidth != 0 || rowY != 0)
  {
    createCanvas(200, 200);
    var row = new Array(rowY).fill('#000000');
    for (let i = 0; i < Xwidth; i++) 
    {
      grid[i] = row;
    }
    colorMode(RGB)
    renderBoard();
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
  if (pickColor == false)
  {
    let spotX = floor(mouseX / (width / rowX));
    let spotY = floor(mouseY / (height / rowY));
    if (spotX >= 0 && spotX <= rowX && spotY >= 0 && spotY <= rowY)
    {
      drawPixel(spotX, spotY, col);
      // send changed pixel to python program
      socket.emit('msg',JSON.stringify('{"a":'+'[{'+"X:"+spotX+','+"Y:"+spotY+','+"color:"+col+'}]'+'}'));
    }
  }
  else
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
    fill("#000000");
    rect(x*(width / rowX),y*(width / rowY),width / rowX,height / rowX);
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
  rect(spotX*(width / rowX),spotY*(width / rowY),width / rowX,height / rowX);
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

function urlChanged(value)
{
  socket.emit('msg','{"Url":"'+value.value+'"}');
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


