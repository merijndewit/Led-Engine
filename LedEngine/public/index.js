var socket = io();

window.addEventListener("load", function()//when page loads
{ 
    if(('ontouchstart' in window) || (navigator.MaxTouchPoints > 0) || (navigator.msMaxTouchPoints > 0)){
        //using touchscreen
        document.addEventListener("touchstart", ReportTouchStart, false);
        document.addEventListener("touchend", ReportTouchEnd, false);
    }else{
        //using mouse
        document.addEventListener("touchstart", ReportTouchStart, false);
        document.addEventListener("touchend", ReportTouchEnd, false);
        document.addEventListener("touchmove", ReportTouchMove, false);
        document.addEventListener("mouseup", ReportMouseUp, false);
        document.addEventListener("mousedown", ReportMouseDown, false);
    }
});


function ReportTouchStart(e) 
{
	if (e.target.className != "serialtext") 
    {
		e.preventDefault();
	}
	if (e.target.className != 'range-slider') 
    {
		socket.emit('msg','{"'+e.target.id+'":1}');
		document.getElementById("DebugData").innerHTML = '{"'+e.target.id+'":1}';
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
		document.getElementById("DebugData").innerHTML = '{"'+e.target.id+'":0}';
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
      document.getElementById("DebugData").innerHTML = '{"'+e.target.id+'":1}';
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
        document.getElementById("DebugData").innerHTML = '{"'+e.target.id+'":0}';
    }
}

var ConsoleText = "";

socket.on('FB',function (data) 
{  
    console.log('DataFromServer'+data.toString()+'!');
    var obj2 = JSON.parse(data.toString()); // Convert to JSON format
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
            {
    	        console.log('id='+id+'; className='+className)+" value="+result;	
    	        if (className.startsWith('switch'))  
                {
    	            if (result == 1) { document.getElementById(id).classList='switch active';}
    	            else document.getElementById(id).classList='switch inactive';
    	        }
    	        if (className == 'serialtext') 
                {
    	            document.getElementById(id).innerHTML = result;
    	            if (id==="S3") { // Reading serial text from DOM on IE does not work.  So we have to save text to a variable.
    	                ConsoleText += result;
    	                document.getElementById(id).value = ConsoleText;
    	            }
    	        }
            }
        }
    }
});
