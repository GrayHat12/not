const Discord = require('discord.js');
const events = require('events');
const {sendMessage,types} = require('./util');
const axios = require('axios');

const twitterEvent = new events.EventEmitter();
var options = {
    'method': 'GET',
    'url': 'https://api.twitter.com/2/timeline/profile/id.json',
    'headers': {
        'x-guest-token': '1258733071592853504',
        'Authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
    }
};

async function startTwitter(profile='335540047'){
    setInterval(function() {
        Twitter(profile);
    }, 5*60*1000);
}
async function Twitter(profile){
    var url = options.url;
    url = url.replace('id',profile);
    axios.default.get(options.url,{headers: options.headers}).then((res)=>{
        instaEvent.emit("fetched",profile,res.data);
    }).catch((err)=>{
        instaEvent.emit("errorFetching",profile,err);
    });
}
function getLatestPost(profile="",data=require('./twitter.json')){
    var post = {
        key: '',
        tweet: {}
    };
    var tweets = data.globalObjects.tweets;
    for(var key in tweets){
        var tweet = tweets[key];
        if(post.key==''){
            post.key = key;
            post.tweet = tweet;
            continue;
        }
        var bigInt = BigInt(key);
        var prevInt = BigInt(post.key);
        if(bigInt>prevInt){
            post.key = key;
            post.tweet = tweet;
        }
    }
    return post;
}

function getProfile(profile="",data=require('./twitter.json')){
    var profile = data.globalObjects.users[profile];
    return profile;
}

module.exports = {
    twitterEvent: twitterEvent,
    startTwitter: startTwitter,
    getLatestPost: getLatestPost,
    getProfile: getProfile
};