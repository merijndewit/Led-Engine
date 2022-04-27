var socket = io(); 

ledPanelsWidth = 0
ledPanelsHeight = 0

ledPanelOrderList = []

window.addEventListener("load", function()
{
  if(('ontouchstart' in window) || (navigator.MaxTouchPoints > 0) || (navigator.msMaxTouchPoints > 0)) 	
  {
    //mobile
    document.addEventListener("touchstart", ReportTouchStart, false);
    document.addEventListener("touchend", ReportTouchEnd, false);
    document.addEventListener("touchdown", ReportMouseDown, false);
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
        if (id == 'A1')
        {
          document.getElementById(id).value = result;
        }
        else if (id == 'color0')
        {
          valueHexChanged('#FFBC42');
        }
        else if (id == 'color1')
        {
          valueHexChanged('#D81159');
        }
        else if (id == 'color2')
        {
          valueHexChanged('#8F2D56');
        }
        else if (id == 'color3')
        {
          valueHexChanged('#218380');
        }
        else if (id == 'color4')
        {
          valueHexChanged('#73D2DE');
        }

      }
    }
    else if (id == 'JSONdata')
    {
      if (obj2.JSONdata[0].LEDPanelHeight)
      {
        document.getElementById("LEDPanelHeight").value = obj2.JSONdata[0].LEDPanelHeight;
      }
      if (obj2.JSONdata[0].LEDPanelWidth)
      {
        document.getElementById("LEDPanelWidth").value = obj2.JSONdata[0].LEDPanelWidth;
      }
      if (obj2.JSONdata[0].amountOfPanelsInWidth)
      {
        document.getElementById("amountOfPanelsInWidth").value = obj2.JSONdata[0].amountOfPanelsInWidth;
        ledPanelsWidth = obj2.JSONdata[0].amountOfPanelsInWidth;
        ledPanelOrderList = make2DArray(ledPanelsWidth, ledPanelsHeight)
        displayLedPanelGrid();
      }
      if (obj2.JSONdata[0].amountOfPanelsInHeight)
      {
        document.getElementById("amountOfPanelsInHeight").value = obj2.JSONdata[0].amountOfPanelsInHeight;
        ledPanelsHeight = obj2.JSONdata[0].amountOfPanelsInHeight;
        ledPanelOrderList = make2DArray(ledPanelsWidth, ledPanelsHeight)
        displayLedPanelGrid();
      }
      if (obj2.JSONdata[0].redCalibration)
      {
        document.getElementById("redCalibration").value = obj2.JSONdata[0].redCalibration;
      }
      if (obj2.JSONdata[0].greenCalibration)
      {
        document.getElementById("greenCalibration").value = obj2.JSONdata[0].greenCalibration;
      }
      if (obj2.JSONdata[0].blueCalibration)
      {
        document.getElementById("blueCalibration").value = obj2.JSONdata[0].blueCalibration;
      }
      if (obj2.JSONdata[0].LedCount)
      {
        document.getElementById("LedCount").value = obj2.JSONdata[0].LedCount;
      }
      if (obj2.JSONdata[0].brightnessValue)
      {
        document.getElementById("brightnessValue").value = obj2.JSONdata[0].brightnessValue;
      }
    }
  }
});

function valueChanged(e){
  let a = e.value;

  // this updates the brightness slider value
  var sliderDiv = document.getElementById("A1");
  sliderDiv.innerHTML = a;

  socket.emit('msg','{"A1":'+a+'}');
}

function valueHexChanged(value)
{
  socket.emit('msg','{"HEX":"'+value+'"}');
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

function valuePanelChanged(e)
{ 
  if (e.value != "")
  {
    var element = document.getElementById(e.id);
    var xPosition = e.id.substring(
      e.id.indexOf("F") + 1, 
      e.id.lastIndexOf("f")
    );
    var yPosition = e.id.substring(
      e.id.indexOf("L") + 1, 
      e.id.lastIndexOf("l")
    );
    element.innerHTML = e.value;
    ledPanelOrderList[xPosition][yPosition] = parseInt(e.value)
    
    socket.emit('msg', JSON.stringify({ WriteToJson: 1, key : "ledPanelOrderList", value : ledPanelOrderList}));
  }
}

function make2DArray(cols, rows)
{
  var listRow = []
  for (let i = 0; i < cols; i++) 
  {
    listRow.push(0)
  }  
  
  listCol = []
  for (let i = 0; i < rows; i++) 
  {
    listCol[i] = listRow.slice()
  }  
  return listCol
}


function amountOfLedPanelsChanged(value)
{
  if (value.id == "amountOfPanelsInWidth" && value.value != "")
  {
    var element = document.getElementById(value.id);
    element.innerHTML = value.value;
    socket.emit('msg', JSON.stringify({ WriteToJson: 1, key : value.id, value : value.value}));
    ledPanelsWidth = value.value;
    displayLedPanelGrid();
    ledPanelOrderList = make2DArray(ledPanelsWidth, ledPanelsHeight)
  }
  else if (value.id == "amountOfPanelsInHeight" && value.value != "")
  {
    var element = document.getElementById(value.id);
    element.innerHTML = value.value;
    socket.emit('msg', JSON.stringify({ WriteToJson: 1, key : value.id, value : value.value}));
    ledPanelsHeight = value.value;
    displayLedPanelGrid();
    ledPanelOrderList = make2DArray(ledPanelsWidth, ledPanelsHeight)
  }
}
function displayLedPanelGrid()
{
  var ledPanelArray = make2DArray(ledPanelsWidth, ledPanelsHeight);
  var gridContainer = document.getElementById("grid-container");
  while (gridContainer.firstChild) {
    gridContainer.removeChild(gridContainer.lastChild);
  }
  
  gridContainer.style.gridTemplateColumns = "repeat("+ledPanelsWidth+", 1fr)" //this is to set the amount of colums on the x position
  //var ledPanelPanel = document.createElement("INPUT");

    for (let x = 0; x < ledPanelArray.length; x++) 
    {
      for (let y = 0; y < ledPanelArray[x].length; y++) 
      {
        var gridPanel = document.createElement("INPUT");
        gridPanel.type = "text";
        gridPanel.value = 0;
        gridPanel.className = "grid-item";
        gridPanel.oninput = function(){valuePanelChanged(this)};
        gridPanel.id = "gridPan"+"F"+x+"f"+"L"+y+"l";
        document.getElementById('grid-container').appendChild(gridPanel);
      }
    }  
}

function SetOneValue(e)
{
  socket.emit('msg', JSON.stringify({ SetOneValueFunction: e.id, value : e.value}));
}

function WriteToJson(e)
{
  socket.emit('msg', JSON.stringify({ WriteToJson: 1, key : e.id, value : e.value}));
}

function Start()
{
  //here we read the json file for the previous settings
  socket.emit('msg','{"RequestJSONdata":"1"}');
  displayLedPanelGrid();
}
Start();

