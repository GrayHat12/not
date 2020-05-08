const Discord = require('discord.js');
const { Gtube, Item } = require("gtube");
const settings = require('./settings.json');
const utils = require('./utils');
const { getLyrics } = require('genius-lyrics-api');
const events = require('events');

const musicEvents = new events.EventEmitter();

function music(message=new Discord.Message()){
    var textMessage = message.content;
    var tokens = textMessage.split(' ');
    var prefix = tokens.shift();
    var command = tokens.shift();
    var option = tokens.shift();
    var rest = tokens.join(' ');
    if(command.toLowerCase()!='play'){
        return utils.sendMessage(message,"issue at music.js 12",utils.types.code,null);
    }
    if(option=='-l'){
        return Lyrics(rest,message);
    }
    if(option=='-a'){
        return Artist(rest,message);
    }
    if(option=='-s'){
        return Song(rest,message);
    }
}
async function Lyrics(rest="",message=new Discord.Message()){
    const options = {
        apiKey: settings.genius_api,
        title: '',
        artist: '',
        optimizeQuery: true
    };
    if(rest.includes('-artist')){
        var rst = rest.split('-artist');
        rst.shift();
        options['artist'] = rst[1];
        options['title'] = rst[0];
    }else{
        options['title'] = rest;
    }
    getLyrics(options).then((lyric)=>{
        utils.sendMessage(message,lyric,utils.types.lyrics,null);
    });
}
async function Artist(rest="",message=new Discord.Message()){
    var ob = new Gtube(rest);
    ob.on("cleared",()=>{
        musicEvents.emit("cleared");
    });
    ob.on("addedItem",(item)=>{
        musicEvents.emit("addedItem",item);
    });
    ob.process();
}
async function Song(rest="",message=new Discord.Message()){
    var ob = new Gtube(rest);
    var done=false;
    ob.on("cleared",()=>{
        musicEvents.emit("cleared");
    });
    ob.on("addedItem",(item)=>{
        if(!done)musicEvents.emit("addedItem",item);
        done=true;
    });
    ob.process();
}

module.exports = {
    music: music,
    musicEvents: musicEvents
}