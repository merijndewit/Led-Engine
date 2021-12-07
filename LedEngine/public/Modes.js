var socket = io(); 

window.addEventListener("load", function(){
  if(('ontouchstart' in window) || (navigator.MaxTouchPoints > 0) || (navigator.msMaxTouchPoints > 0)) 	{
    //mobile
    document.addEventListener("touchstart", ReportTouchStart, false);
    document.addEventListener("touchend", ReportTouchEnd, false);
  }else{
    //desktop
    document.addEventListener("touchstart", ReportTouchStart, false);
    document.addEventListener("touchend", ReportTouchEnd, false);
    document.addEventListener("touchmove", ReportTouchMove, false);
    document.addEventListener("mouseup", ReportMouseUp, false);
    document.addEventListener("mousedown", ReportMouseDown, false);
  }
  
});

function ReportOnClick(e) {
  socket.emit('msg','{"'+e.target.id+'":2}');
}

function ReportOnDblClick(e) {
  socket.emit('msg','{"'+e.target.id+'":3}');
}

function ReportOnMouseDown(e) {
  socket.emit('msg','{"'+e.target.id+'":1}');
}

function ReportOnMouseUp(e) {
  socket.emit('msg','{"'+e.target.id+'":0}');
}

function ReportTouchStart(e) {
	if (e.target.className != "serialtext") { 
		e.preventDefault();
	}
	if (e.target.className != 'range-slider') {
		socket.emit('msg','{"'+e.target.id+'":1}');
	}
}

function ReportTouchEnd(e) {
	if (e.target.className != "serialtext") { 
		e.preventDefault();  
	}
	if (e.target.className != 'range-slider') {  
		socket.emit('msg','{"'+e.target.id+'":0}');	
	}
	
}

function ReportTouchMove(e) {
	if (e.target.className != "serialtext") {
		e.preventDefault();
	}
	socket.emit('TouchMove',e.offsetX,e.offsetY);
}

function ReportMouseDown(e) {
  if (e.target.className != 'range-slider') {
    socket.emit('msg','{"'+e.target.id+'":1}');
  }
}


function ReportMouseUp(e) {
  if (e.target.className === 'range-slider') {
    console.log("volume class detected");
  } else {
      socket.emit('msg','{"'+e.target.id+'":0}');
  }
}

function ReportMouseMove(e) {
  socket.emit('TouchMove',e.offsetX,e.offsetY); 
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
      }
    }
  }
});

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

function WaveLengthInputChanged(e){
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