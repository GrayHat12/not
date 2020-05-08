const Discord = require('discord.js');
const types = {
    code : "code",
    lyrics: "lyrics",
    text: "text"
}
function sendMessage(message=new Discord.Message(),text="",type=types.text,attachment=null){
    ;
}
module.exports = {
    sendMessage: sendMessage,
    types: types
};