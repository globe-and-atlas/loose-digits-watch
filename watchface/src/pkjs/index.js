var Clay=require('@rebble/clay');
var config=[
 {type:'heading',defaultValue:'Loose Digits'},
 {type:'text',defaultValue:'Knock the watch case twice to tumble the digits. They reassemble in three seconds. Screen touch is not available to watchfaces.'},
 {type:'select',messageKey:'Motion',label:'Animation',defaultValue:'1',options:[{label:'On',value:'1'},{label:'Off · still clock',value:'0'}]},
 {type:'select',messageKey:'Trigger',label:'Trigger',defaultValue:'0',options:[{label:'Double case knock',value:'0'},{label:'Single case knock',value:'1'},{label:'Wrist roll',value:'2'}]},
 {type:'select',messageKey:'DateFormat',label:'Date',defaultValue:'0',options:[{label:'Off',value:'0'},{label:'YYYY-MM-DD',value:'1'},{label:'MM/DD/YYYY',value:'2'},{label:'DD/MM/YYYY',value:'3'}]},
 {type:'heading',defaultValue:'Colors'},
 {type:'color',messageKey:'Background',label:'Background',defaultValue:'FFFFAA',sunlight:false,allowGray:true},
 {type:'color',messageKey:'Foreground',label:'Digits & date',defaultValue:'000000',sunlight:false,allowGray:true},
 {type:'color',messageKey:'Accent',label:'Colon accent',defaultValue:'FF5500',sunlight:false,allowGray:true},
 {type:'text',defaultValue:'Colors use the Pebble palette. Matching digit and background colors get a readable fallback.'},
 {type:'submit',defaultValue:'Save to watch'}];
var clay=new Clay(config,null,{autoHandleEvents:false});
function integer(v,max,fallback){var n=Number(v);return v!==undefined&&v!==null&&v!==''&&typeof v!=='boolean'&&isFinite(n)&&Math.floor(n)===n&&n>=0&&n<=max?n:fallback;}
function normalize(raw){raw=raw||{};return {Motion:integer(raw.Motion,1,1),DateFormat:integer(raw.DateFormat,3,0),Trigger:integer(raw.Trigger,2,0),Background:integer(raw.Background,0xFFFFFF,0xFFFFAA),Foreground:integer(raw.Foreground,0xFFFFFF,0),Accent:integer(raw.Accent,0xFFFFFF,0xFF5500)};}
function send(){var saved;try{saved=JSON.parse(localStorage.getItem('clay-settings')||'{}');}catch(e){saved={};}Pebble.sendAppMessage(normalize(saved||{}));}
Pebble.addEventListener('ready',function(){if(localStorage.getItem('clay-settings'))send();});
Pebble.addEventListener('showConfiguration',function(){Pebble.openURL(clay.generateUrl());});
Pebble.addEventListener('webviewclosed',function(e){if(!e||!e.response||e.response==='CANCELLED')return;try{clay.getSettings(e.response);}catch(err){return;}send();});
module.exports={config:config,normalize:normalize};
