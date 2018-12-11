#!/usr/local/bin/node
"use strict";
const myMod       = require("./node_modules/my.node.module.config");
let myConfig = myMod.config;

const express  = require(myConfig.moduleDIR+"express");
//const express  = require("/usr/local/lib/node_modules/express");
const execSync = require("child_process").execSync;
const exec = require("child_process").exec;
const spawn = require('child_process');
const fs       = require("fs");
const DS = "/";
const app = express();
const port = 5555;
let serverPS = null;
let selfIP = null;

/***************/
   let watki=0;
   var tempo = 1000;
   var banki = '1111';
/***************/

function readWaves(path){
	let data =[]
	var files = fs.readdirSync(path).sort();
	files.forEach(function(x){
		if (x!='lost+found') data.push(path+ x)
	});
	return data;
}


function ustawGlosy(banki){
   let g=[];
   let i=1;
   banki.split('').forEach(l => {
     console.log(i,banki,l);
     if (l==='1'){
         console.log('/media/ram'+i+'/')
         let ibank = readWaves('/media/ram'+i+'/')
         g = g.concat(ibank);
         console.log('ibank=',ibank.length,g.length);
     }
      i++;
   });   
   //console.log(g)
   console.log('glosy length=',g.length)
   return g;
}
var glosy = ustawGlosy(banki);

/**********************/      
      let comm1 = "ps -ef | grep /voices/sound.js | grep -v grep | awk '{print $2}'";
      let comm2 = "sudo hostname -I";
      //let comm3 = "sudo ifconfig wlan0 | sed -En -e 's/.*inet ([0-9.]+).*/\1/p'";
      try {
         serverPS = execSync(comm1).toString().trim();    
            //console.log('serverPS=',serverPS);
         selfIP = execSync(comm2).toString().trim().split(' ')[0];    
            //console.log('selfIP=',selfIP);
        // let info3 = execSync(comm3).toString().trim();    console.log(3,info);
      } catch(err) {console.log(err);}




function audioPlay(nr,delay){
	delay = Math.round( (tempo/8) + (Math.random()*tempo) );
	nr = Math.floor(Math.random()*glosy.length);
   if (!glosy[nr]) return;   
   exec('ps -ef | grep mpg123 | grep -v grep | wc -l',function(error, stdout, stderr){      
         watki = parseInt(stdout);
         console.log('@WC==='+watki,'tempo='+tempo,glosy[nr]);
         if (watki<7){
            setTimeout(function(){
               exec('mpg123 -q "'+glosy[nr]+'"',function(error, stdout, stderr){
                  if (error)  console.log('error=',error);
                  if (stdout) console.log('stdout=',stdout);
                  if (stderr) console.log('stderr=',stderr);
               })
            },delay)
         }
   })    
}

audioPlay(0,0)
let mainInterval = setInterval(function(){audioPlay(null,null)},tempo)

/**/	  
	  
app.use(express.static(__dirname+DS+'public'));

app.use((req, res, next) => {
    //console.log('#13    Time: ', Date.now(),(new Date()).getTime());
    //console.log('Time: ', Date.now(),(new Date()).toLocaleString());
    next();
});

app.use((req, res, next) => {
    //console.log('#19 newTime: ', Date.now(),(new Date()).toLocaleString());
    next();
});


//qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq		
Buffer.prototype.pars = function() {return this.toString().trim();};
var actualPlaylist = "radio";

function parseMpcInfo(f){
	var ret = {"type":"info","active":"","title":"???","info":f,"vol":"","extra":"","actualPlaylist":actualPlaylist};
	if (f.length===0) {return ret;}
	
			var mm = f.match(/\.*?#(.*?)\/.*?\nvolume: (.*?)% .*?repeat: (.*?) .*?random: (.*?) .*?single: (.*?) .*?/m);	 	
			//console.log('mm=',mm);
			if (mm) {
				ret.mm = mm;
				if (mm[1]) ret.active = mm[1];
				if (mm[2]) ret.vol    = mm[2];
				if (mm[3]) ret.rnd   = mm[3]; 
				if (mm[4]) ret.repeat   = mm[4]; 
				if (mm[5]) ret.single   = mm[5]; 
			}
	
	var infoarr = String(f).split("\n");
	if (infoarr.length==4) {ret.title="ERROR"; ret.info=infoarr[3]; return ret;}
	ret.title = infoarr[0];
	return ret;
}


	function sendInfo(res,ret){
		var j = JSON.stringify([ret]);
		res.setHeader("Access-Control-Allow-Origin", "*");
		res.setHeader("Access-Control-Allow-Methods", "*");
		res.setHeader("Access-Control-Allow-Headers", "*");
		res.send(JSON.stringify(ret));
	}	

app.get("/tempo/*", function(req, res){
	console.log(req.params);
	if (req.params[0]) tempo = req.params[0];
	console.log(tempo); 
   let info={'tempo':tempo}
   mainInterval = clearInterval(mainInterval)
   mainInterval = setInterval(function(){audioPlay(null,null)},tempo)
	sendInfo(res,info);
});



app.get("/banks/*", function(req, res){
	console.log(req.params);
	if (req.params[0]) banki = req.params[0];
	console.log(banki);
   glosy = ustawGlosy(banki);
   let info={'tempo':tempo,'banki':banki,'ile':glosy.length}
	sendInfo(res,info);
});

/***********************************************/
/***********************************************/
/***********************************************/

app.get("/radio/*", function(req, res){
	var param=req.params[0];
	if (param=="0") param="stop";
	var mpcexe = "mpc play "+param;
	if (param=="stop" || param=="play" || param=="current" || param=="next" || param=="prev" || param=="pause"|| param=="playlist" ) mpcexe = "mpc "+param;
	if (param=="info") mpcexe = "mpc";
	if (param=="seek") mpcexe = "mpc seek +20%";
	//console.log('#66 PARAM=',param);
	//console.log('#67 mpcexe=',mpcexe);
		try {
			var info = execSync(mpcexe).pars();
		} catch(err) {
			var info = err.stderr.toString();
		}
	var ret  = parseMpcInfo(info);
	sendInfo(res,ret);
});


app.get("/df", function(req, res){
   let info = "?";
	try {info = execSync("df -h").pars();} catch(err) {info = err.stderr.toString();}
	sendInfo(res,info);
});
app.get("/temp", function(req, res){
   let info = "?";
	try {info = execSync("/opt/vc/bin/vcgencmd measure_temp").pars();} catch(err) {info = err.stderr.toString();}
	sendInfo(res,info);
});
app.get("/wifi", function(req, res){
   let info = "?";
	try {info = execSync("cat /proc/net/wireless | grep wlan0 | awk '{print $4}'").pars();} catch(err) {info = err.stderr.toString();}
    //echo  -en "\r$(cat /proc/net/wireless | grep wlan0 | awk '{print $4}')\b "
	sendInfo(res,info);
});
app.get("/cpu", function(req, res){
   let info = "?";
	try {info = execSync("top -bn 1 | awk '{print $9}' | tail -n +8 | awk '{s+=$1} END {print s}'").pars();} catch(err) {info = err.stderr.toString();}
	sendInfo(res,info);
});
app.get("/all", function(req, res){
   let info = "";
	try {info += ' T='+execSync("/opt/vc/bin/vcgencmd measure_temp").pars();} catch(err) {info += err.stderr.toString();}
   try {info += ' W='+execSync("cat /proc/net/wireless | grep wlan0 | awk '{print $4}'").pars();} catch(err) {info += err.stderr.toString();}
	try {info += ' U='+execSync("top -bn 1 | awk '{print $9}' | tail -n +8 | awk '{s+=$1} END {print s}'").pars()+'%';} catch(err) {info += err.stderr.toString();}
	sendInfo(res,info);
});
app.get("/frq", function(req, res){
   let info = "?";
	try {info = execSync("cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq").pars();} catch(err) {info = err.stderr.toString();}
	sendInfo(res,info);
});
app.get("/playlist", function(req, res){
   let info = "?";
	try {info = execSync("mpc playlist").pars();} catch(err) {info = err.stderr.toString();}
	sendInfo(res,info);
});
app.get("/reboot", function(req, res){
   let info = "?";
	try {info = execSync("sudo reboot").pars();} catch(err) {info = err.stderr.toString();}
	sendInfo(res,info);
});
app.get("/poweroff", function(req, res){
   let info = "?";
	try {info = execSync("sudo poweroff").pars();} catch(err) {info = err.stderr.toString();}
	sendInfo(res,info);
});
app.get("/exit", function(req, res){
   let info = "?";
   let killkiosk = "ps -ef | grep kiosk | grep -v grep | awk '{print \"sudo kill -9 \"$2}' | sh";
	try {info = execSync(killkiosk).pars();} catch(err) {info = err.stderr.toString();}
	sendInfo(res,info);
});
 



/*
app.get('/*', (req, res) => {
	//console.log('#24=',req);
	console.log('#25=',req.params);
	console.log('#26=',req.path);
	console.log('#27=',req.query);
	console.log('#28=',req.search);
	let param = req.params[0];
	console.log('#30 param=',param);
	res.send('list/'+param)
})
app.get('/?', (req, res) => {
	//console.log('#24=',req);
	console.log('?#25=',req.params);
	console.log('?#26=',req.path);
	console.log('?#27=',req.query);
	console.log('?#28=',req.search);
	let param = req.params[0];
	console.log('?#30 param=',param);
	res.send('list/'+param)
})
*/
app.get('/:id', function(req, res) {
 var id = req.params.id; //or use req.param('id')
 var id2 = req.query.id; 
	console.log('?#47 params=',req.params);
	console.log(id,id2);
	res.send('list/'+id+id2)

});
 
app.get('/favicon.ico', (req, res) => res.send('*'))

app.get('/list', (req, res) => res.send('list'))

app.get('/list/*', (req, res) => {
	console.log(req.params);
	let param = req.params[0];
	console.log(param);
	res.send('list/'+param)
})


app.listen(port, () => {
	serverPS = execSync("ps -ef | grep /voices/sound.js | grep -v grep | awk '{print $2}'").toString().trim();//    console.log('serverPS=',serverPS);
	console.log("\n====================================");
	console.log(`Server listening on port ${port}! PS: ${serverPS}`);
	console.log('http://'+selfIP+':'+port)
	//console.log(myConfig);
	console.log(myConfig.name,myConfig.location,myMod.czas(),myMod.toDate(),myMod.plDate());
});


		//exec('aplay -q '+glosy[nr],function(a,b,c){		// tylko wavy
		//exec('mplayer '+glosy[nr],function(a,b,c){
		//exec('omxplayer -local '+glosy[nr],function(a,b,c){
		//exec('mpg321 -q '+glosy[nr]+' &',function(a,b,c){
