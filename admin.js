const Discord = require('discord.js');
const utils = require('./utils');

const devPrefix = {
    prefix: '+',
    commands: {
        eval: evaluate
    },
    author: '425182298280034305'
};

function runAsDevCommand(message=new Discord.Message()){
    if(!isDev(message)) return utils.gebug(utils.debugTypes.workerb,"error9","invalidDev");
    var messageTokens = message.content.split(' ');
    messageTokens.shift(); // prefix
    var command = messageTokens.shift();
    if(command in devPrefix.commands){
        return devPrefix.commands[command](message,messageTokens.join(' '));
    }
    utils.gebug(utils.debugTypes.workerb,"error20","invalidDevCommand",command);
    utils.sendMessage(message,`invalidDevCommand ${command}`,utils.types.code,null);
}

function evaluate(message=new Discord.Message(),rest=''){
    try{
        let evaled = eval(rest);
        if (typeof evaled !== "string") evaled = require("util").inspect(evaled);
        utils.sendMessage(message,clean(evaled),utils.types.code,null);
    }catch(err){
        utils.sendMessage(message,clean(err),utils.types.code,null);
        utils.gebug(utils.debugTypes.workera,"error31","evalError",`${err}`);
    }
}

function clean(text) {
    if (typeof(text) === "string")
        return text.replace(/`/g, "`" + String.fromCharCode(8203)).replace(/@/g, "@" + String.fromCharCode(8203));
    else
        return text;
}

function isDev(message=new Discord.Message()){
    var messageText = message.content;
    var messageTokens = messageText.split(' ');
    var prefix = messageTokens.shift();
    return prefix==devPrefix.prefix && message.author.id==devPrefix.author;
}

module.exports = {
    isDev: isDev,
    runAsDevCommand: runAsDevCommand
};