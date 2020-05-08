const Discord = require('discord.js');
var log = require('debug');
const types = {
    code : "code",
    lyrics: "lyrics",
    text: "text"
};
const debugTypes = {
    workera : 'worker:a',
    workerb : 'worker:a',
    html: 'html'
};
function sendMessage(message=new Discord.Message(),text="",type=types.text,attachment=null){
    if(type==types.text) return sendText(message,`${text}`,attachment);
    if(type==types.code) return sendCode(message,`${text}`,attachment);
    if(type==types.lyrics) return sendLyrics(true,message,`${text}`,attachment);
}

function gebug(debugType=debugTypes.workera,name="",...any){
    log(debugType)(name,...any);
}

function sendText(message=new Discord.Message(),text="",attachment=null){
    var toBeSent = text.substring(0,900);
    var rest = text.substring(900);
    if(attachment && typeof attachment == typeof (new Discord.MessageAttachment())){
        message.channel.send(attachment).then((res)=>{}).catch((err)=>{
            gebug(debugTypes.workera,"error33",err);
        });
    }
    if(toBeSent.length<=0) return;
    message.channel.send(toBeSent).then((res)=>{
        if(rest.length>0){
            sendText(message,rest,null);
        }
    }).catch((err)=>{
        gebug(debugTypes.workera,"error29",err);
    });
}

function sendCode(message=new Discord.Message(),text="",attachment=null){
    var toBeSent = "";
    var rest = "";
    var lines = text.split('\n');
    while(lines.length>0 && toBeSent.length<900){
        var line = lines.shift();
        toBeSent+=line+'\n';
    }
    rest = lines.join('\n');
    if(attachment && typeof attachment == typeof (new Discord.MessageAttachment())){
        message.channel.send(attachment).then((res)=>{
            if(toBeSent.length<=0) return;
            message.channel.send(toBeSent,{code:"xl"}).then((res)=>{
                if(rest.length>0){
                    sendCode(message,rest,null);
                }
            }).catch((err)=>{
                gebug(debugTypes.workera,"error48",err);
            });
        }).catch((err)=>{
            gebug(debugTypes.workera,"error51",err);
        });
    }else{
        if(toBeSent.length<=0) return;
        message.channel.send(toBeSent,{code:"xl"}).then((res)=>{
            if(rest.length>0){
                sendCode(message,rest,null);
            }
        }).catch((err)=>{
            gebug(debugTypes.workera,"error48",err);
        });
    }
}

function sendLyrics(first=true,message=new Discord.Message(),text="",attachment=null){
    var toBeSent = "";
    var rest = "";
    var lines = text.split('\n');
    while(lines.length>0 && toBeSent.length<900){
        var line = lines.shift();
        toBeSent+=line+'\n';
    }
    rest = lines.join('\n');
    if(toBeSent.length<=0) return;
    var embd = new Discord.MessageEmbed();
    embd.setColor('#32a852')
    .setDescription(toBeSent);
    if(first) embd.setAuthor("Lyrics",message.author.avatarURL({format: 'png',dynamic:true}));
    if(rest.length==0) embd.setTimestamp(new Date());
    message.channel.send(embd).then((res)=>{
        if(rest.length>0) sendLyrics(false,message,rest,null);
    }).catch((err)=>{
        gebug(debugTypes.workera,"error82",err);
    });
    if(attachment && typeof attachment == typeof (new Discord.MessageAttachment())){
        message.channel.send(attachment).then((res)=>{}).catch((err)=>{
            gebug(debugTypes.workera,"error86",err);
        });
    }
}

module.exports = {
    sendMessage: sendMessage,
    types: types,
    gebug: gebug,
    debugTypes: debugTypes
};