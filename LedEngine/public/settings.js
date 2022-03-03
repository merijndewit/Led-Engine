var socket = io(); 

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
        document.getElementById("configPanelHeight").value = obj2.JSONdata[0].LEDPanelHeight;
      }
      if (obj2.JSONdata[0].LEDPanelWidth)
      {
        document.getElementById("configPanelWidth").value = obj2.JSONdata[0].LEDPanelWidth;
      }
      if (obj2.JSONdata[0].amountOfPanelsInWidth)
      {
        document.getElementById("amountOfPanelsInWidth").value = obj2.JSONdata[0].amountOfPanelsInWidth;
      }
      if (obj2.JSONdata[0].amountOfPanelsInHeight)
      {
        document.getElementById("amountOfPanelsInHeight").value = obj2.JSONdata[0].amountOfPanelsInHeight;
      }
      if (obj2.JSONdata[0].redCalibration)
      {
        document.getElementById("RedCalibrationPercentage").value = obj2.JSONdata[0].redCalibration;
      }
      if (obj2.JSONdata[0].greenCalibration)
      {
        document.getElementById("GreenCalibrationPercentage").value = obj2.JSONdata[0].greenCalibration;
      }
      if (obj2.JSONdata[0].blueCalibration)
      {
        document.getElementById("BlueCalibrationPercentage").value = obj2.JSONdata[0].blueCalibration;
      }
      if (obj2.JSONdata[0].LedCount)
      {
        document.getElementById("configPanelLedCount").value = obj2.JSONdata[0].LedCount;
      }
      if (obj2.JSONdata[0].brightnessValue)
      {
        document.getElementById("A1").value = obj2.JSONdata[0].brightnessValue;
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

function RedCalibrationChanged(value)
{
  if (value.value != 0)
  {
    socket.emit('msg','{"RedCalibration":"'+value.value+'"}');
  }
}

function GreenCalibrationChanged(value)
{
  if (value.value != 0)
  {
    socket.emit('msg','{"GreenCalibration":"'+value.value+'"}');
  }
}

function BlueCalibrationChanged(value)
{
  if (value.value != 0)
  {
    socket.emit('msg','{"BlueCalibration":"'+value.value+'"}');
  }
}

function configPanelLedCountChanged(value)
{
  if (value.value != 0)
  {
    socket.emit('msg','{"LedCount":"'+value.value+'"}');
  }
}


function configPanelWidthChanged(value)
{
  if (value.value != 0)
  {
    socket.emit('msg','{"setConfigPanelWidth":"'+value.value+'"}');
  }
}

function configPanelHeightChanged(value)
{
  if (value.value != 0)
  {
    socket.emit('msg','{"setConfigPanelHeight":"'+value.value+'"}');
  }
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

function Start()
{
  //here we read the json file for the previous settings
  socket.emit('msg','{"RequestJSONdata":"1"}');
}
Start();

