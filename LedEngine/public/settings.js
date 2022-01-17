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

