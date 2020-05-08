const Discord = require('discord.js');
const client = new Discord.Client();
const settings = require("./settings.json");
const admin = require('./admin');
const utils = require('./utils');
const music = require('./music');

const validPrefix = "$";
const instaOutline = {
  username: '',
  postsBase: [],
  subscriptions: [],
  getPostBase: function(postUrl=''){
    return postUrl.substring(0,postUrl.indexOf('?'));
  },
  instagram: require('./instagram'),
  start: function(){
    this.instagram.instaEvent.on('fetched',this.fetched);
    this.instagram.instaEvent.on('errorFetching',this.errorFetching);
    this.instagram.instaEvent.on('gotPost',this.gotPost);
    this.instagram.startInsta(this.username);
  },
  firstTime: true,
  fetched: function(profile='',data){
    if(!profile.includes(this.username)) return;
    this.instagram.getAllImages(data);
    this.firstTime = false;
  },
  errorFetching: function(profile='',err){
    utils.gebug(utils.debugTypes.workerb,'error29',err,profile);
  },
  gotPost: function(url){
    var filtered = this.getPostBase(url);
    if(this.postsBase.includes(filtered)) return;
    this.postsBase.push(filtered);
    if(this.firstTime) return;
    utils.gebug(utils.debugTypes.workera,"gotInstaPost",url,filtered);
    var attachment = new Discord.MessageAttachment(url);
    for(var i=0;i<this.subscriptions.length;i++){
      var message = this.subscriptions[i];
      utils.sendMessage(message,"",utils.types.text,attachment);
    }
  }
}

var currentInstaSessions = new Map();

function addInstagram(username='',message = new Discord.Message()){
  if(currentInstaSessions.has(username)){
    currentInstaSessions.get(username).subscriptions.push(message);
  }else{
    var newInstaSession = instaOutline;
    newInstaSession.username = username;
    newInstaSession.postsBase = [];
    newInstaSession.subscriptions.push(message);
    newInstaSession.instagram = require('./instagram');
    newInstaSession.start();
    currentInstaSessions.set(username,newInstaSession);
  }
}

client.on("ready",()=>{
    console.log(`joined ${client.user.tag}`);
});

client.on("message",(message)=>{
  if(message.author.bot) return;
  if(admin.isDev(message)) return admin.runAsDevCommand(message);
  var messageText = message.content;
  var messageTokens = messageText.split(' ');
  var prefix = messageTokens.shift();
  if(prefix!=validPrefix) return;
  var command = messageTokens.shift();
  //#region instagram
  try{
    if(command=='instagram') addInstagram(messageTokens.shift(),message);
    return;
  }catch(err){
    utils.gebug(utils.debugTypes.workerb,"invalidCommandFormat",`${err}`);
    return;
  }
  //#endregion
  //#region music
  if(command=='play'){
    ;
  }
  //#endregion
  //#region twitter
  if(command=='twitter'){
    ;
  }
  //#endregion
  return;
});

client.login(settings.bot_token);