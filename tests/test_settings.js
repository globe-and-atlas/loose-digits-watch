const vm=require('node:vm'),fs=require('node:fs'),assert=require('node:assert/strict');
const events={},sent=[],storage={};let saves=0;
function Clay(config){this.generateUrl=()=> 'config';this.getSettings=(response)=>{saves++;storage['clay-settings']=response;};}
const ctx={module:{exports:{}},require:()=>Clay,Pebble:{addEventListener:(n,f)=>events[n]=f,sendAppMessage:v=>sent.push(v),openURL:()=>{}},localStorage:{getItem:k=>storage[k]||null},console};
vm.runInNewContext(fs.readFileSync('watchface/src/pkjs/index.js','utf8'),ctx);
const n=ctx.module.exports.normalize;
assert.equal(n({Motion:'0',DateFormat:'3'}).Motion,0);assert.equal(n({Motion:'0',DateFormat:'3'}).DateFormat,3);
assert.equal(n({Motion:99,DateFormat:-1}).Motion,1);assert.equal(n({Motion:99,DateFormat:-1}).DateFormat,0);
events.webviewclosed({response:''});events.webviewclosed({response:'CANCELLED'});assert.equal(sent.length,0);assert.equal(saves,0);
events.webviewclosed({response:'{"Motion":0,"DateFormat":2}'});assert.equal(sent.at(-1).Motion,0);assert.equal(sent.at(-1).DateFormat,2);
events.ready();assert.equal(sent.at(-1).DateFormat,2);
console.log('PASS: settings normalization, Save, Cancel, ready restore');

assert.equal(n({}).Trigger,0);assert.equal(n({Trigger:2}).Trigger,2);assert.equal(n({Trigger:3}).Trigger,0);
assert.equal(n({}).Background,0xFFFFAA);assert.equal(n({Background:0}).Background,0);
assert.equal(n({Background:'16777215',Foreground:'85',Accent:'16733440'}).Background,0xFFFFFF);
assert.equal(n({Background:-1,Foreground:true,Accent:null}).Background,0xFFFFAA);
assert.equal(n({Background:-1,Foreground:true,Accent:null}).Foreground,0);
assert.equal(n({Background:-1,Foreground:true,Accent:null}).Accent,0xFF5500);
events.webviewclosed({response:'{"Motion":1,"DateFormat":1,"Trigger":1,"Background":85,"Foreground":16777215,"Accent":16733440}'});
assert.equal(sent.at(-1).Trigger,1);assert.equal(sent.at(-1).Background,85);assert.equal(sent.at(-1).Foreground,16777215);assert.equal(sent.at(-1).Accent,16733440);
console.log('PASS: trigger migration/default, color range validation, custom color Save');
