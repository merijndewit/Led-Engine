const WebPort = 8080;

// set remote address and ports
const UdpListenPort = 3000;
const RemoteAddress = '127.0.0.1'
const UdpTransmitPort = 3001;

var http = require('http').createServer(handler);
var fs = require('fs');
var url = require('url');
var path = require('path');
var io = require('socket.io','net')(http) 
const dgram = require('dgram');
var formidable = require('formidable');


// start webserver
http.listen(WebPort, function() 
{
	console.log('Webserver on port: '+WebPort);
}); 

function handler (req, res) 
{ 
    var q = url.parse(req.url, true);
    var filename = "." + q.pathname;
    var extname = path.extname(filename);
    if (filename=='./') 
	{
    	filename= './index.html';
    }
    var contentType = 'text/html';
    
    switch(extname) 
	{
		case '.js':
		    contentType = 'text/javascript';
		    break;
		case '.css':
		    contentType = 'text/css';
		    break;
		case '.json':
		    contentType = 'application/json';
		    break;
		case '.png':
		    contentType = 'image/png';
		    break;
		case '.jpg':
		    contentType = 'image/jpg';
		    break;
		case '.ico':
		    contentType = 'image/png';
		    break;
    }
    
    fs.readFile(__dirname + '/public/' + filename, function(err, content) 
	{
		if(err) 
		{
		    console.log('File not found. Filename='+filename);
		    fs.readFile(__dirname + '/public/404.html', function(err, content) 
			{
				res.writeHead(200, {'Content-Type': 'text/html'}); 
				return res.end(content,'utf');
		    });
		}
		else {
		    res.writeHead(200, {'Content-Type': contentType}); 
		    return res.end(content,'utf8');
		}
    });
	
	if (req.url == '/FileUploaded.html') 
	{
		var form = new formidable.IncomingForm();
		form.parse(req, function (err, fields, files) 
		{
		  	var oldpath = files.filetoupload.filepath;
		  	var newpath = 'uploads/' + files.filetoupload.originalFilename;
		  	fs.rename(oldpath, newpath, function (err) 
			{
				if (err) throw err;
		  	});
	 	});
	}
}

process.on('SIGINT', function ()  //ctrl-c
{
	process.exit(); 
}); 

var clients = [];  

io.sockets.on('connection', function (socket) 
{
    console.log('A new client has connectioned.');
    var clientInfo = new Object();
    clientInfo.clientId = socket.id;
    clientInfo.logIn = false;
    clients.push(clientInfo);
    console.log(clientInfo);
    console.log(clients.length + ' clients are currently connected');
    
    Send2ComLink('{"NewClient":1}');  
    
    socket.on('msg', function(data) 
	{ 
		Send2ComLink(data);
    });

    socket.on('disconnect', function (data) 
	{
		for( var i=0, len=clients.length; i<len; ++i )
		{
		    var c = clients[i];
		    if(c.clientId == socket.id)
			{
				clients.splice(i,1);
				break;
		    }
		}
    });
    
});

const ComLink = dgram.createSocket('udp4');

ComLink.on('error', (err) => 
{
	console.log(`ComLink udp socket error:\n${err.stack}`);
	ComLink.close();
});

ComLink.on('message',function(msg,info)
{
    console.log('Received %d bytes from %s:%d',msg.length, info.address, info.port);

    if ((info.address == RemoteAddress)) 
	{
		try 
		{
		    var obj = JSON.parse(msg);
		} catch(error) 
		{
		    console.log('error: '+error);
		    obj = null;
		}

		if (obj !== null) 
		{
		    var data = JSON.stringify(obj);
		    console.log('Data='+data+'!');
		    io.emit('FB',data); 
		}
    }
    else 
	{
		console.log('Data received from Rogue device='+msg+'!');
    }
});

ComLink.on('listening', function() 
{
   const address = ComLink.address(); 
   console.log(`Pi is listening to UDP Port ${address.address}:${address.port}:${address.family}`);
   console.log("Pi is transmitting on UDP Port "+RemoteAddress+":"+UdpTransmitPort);
});

ComLink.on('close',function()
{
    console.log('UDP socket is closed!');
});

ComLink.bind(UdpListenPort);

function Send2ComLink (data) 
{ 
    ComLink.send(data+"\n",UdpTransmitPort,RemoteAddress,function(error)
	{
		if(error){
		    ComLink.close();
		    console.log('There was an error sending data');
		}else{
		    console.log('Data sent: '+data);
		}
    });   
}
