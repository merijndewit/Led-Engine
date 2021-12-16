var socket = io(); 

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
    document.addEventListener("mouseup", ReportMouseUp, false);
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

function ReportOnMouseUp(e) 
{
  socket.emit('msg','{"'+e.target.id+'":0}');
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
  
  if (id != null) 
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
      }
    }
  }
});

function SetColor(colorValue)
{
  document.getElementById("PixelColorPicker").value = colorValue; //set the color of the color picker
  col = colorValue //even though the value of the color picker is changed we still need to update it manually
}

function brightnessSliderChanged(brightnessValue)
{
  // this updates the brightness slider value
  if (e.value != 0)
  {
    var sliderDiv = document.getElementById("A1");
    sliderDiv.innerHTML = brightnessValue.value;
    socket.emit('msg','{"A1":'+brightnessValue.value+'}');
  }
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
  print("set pixel color true")
}

//part for pixel drawer
var grid = [];
const rowX = 11;
const rowY = 11;
var col = ('#000000');

function PixelColorChanged(e)
{
  //updates the value of the pixel to draw
  col = e.value;
}

function setup() 
{
  createCanvas(200, 200);
  var row = new Array(rowY).fill('#000000');
  for (let i = 0; i < rowX; i++) 
  {
    grid[i] = row;
  }
  colorMode(RGB)
  renderBoard();
}

function mousePressed() 
{
  if (pickColor == false)
  {
    let spotX = floor(mouseX / (width / rowX));
    let spotY = floor(mouseY / (height / rowY));
    if (spotX >= 0 && spotX <= rowX && spotY >= 0 && spotY <= rowY)
    {
      drawPixel(spotX, spotY);
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

function drawPixel(spotX, spotY)
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
      gridY.push(col);
    }
  }
  grid[spotX] = gridY;
  fill(color(grid[spotX][spotY]));
  rect(spotX*(width / rowX),spotY*(width / rowY),width / rowX,height / rowX);
  print(grid);
}

//only used for debugging
//Note: this doesnt show on the led panel
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