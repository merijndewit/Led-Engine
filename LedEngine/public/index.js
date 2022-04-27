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
        if (id == 'A1') {
	        document.getElementById(id).value = result;
	      }
      }
    }
    else if (id == 'JSONdata')
    {
      if (obj2.JSONdata[0].brightnessValue)
      {
        document.getElementById("brightnessValue").value = obj2.JSONdata[0].brightnessValue;
      }
    }
  }
});

function SetOneValue(e)
{
  if (e.value != "")
  {
    socket.emit('msg', JSON.stringify({ SetOneValueFunction: e.id, value : e.value}));
  }
}

function WriteToJson(e)
{
  socket.emit('msg', JSON.stringify({ WriteToJson: 1, key : e.id, value : e.value}));
}

function Start()
{
  //here we read the json file for the previous settings
  socket.emit('msg','{"RequestJSONdata":"1"}');
}
Start();