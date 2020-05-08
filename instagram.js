const Discord = require('discord.js');
const events = require('events');
const utils = require('./utils');
const axios = require('axios');

const instaEvent = new events.EventEmitter();
const regex = /"display_url"\s*:\s*"([^"]*)"/gm;

async function startInsta(profile='nf._.memes'){
    profile = `https://www.instagram.com/${profile}/`;
    setInterval(function() {
        Instagram(profile);
    }, 5*60*1000);
}
async function Instagram(profile){
    axios.default.get(profile).then((res)=>{
        instaEvent.emit("fetched",profile,res.data);
    }).catch((err)=>{
        instaEvent.emit("errorFetching",profile,err);
    });
}
function getAllImages(data){
    let m;
    var images = [];
    while ((m = regex.exec(str)) !== null) {
        if (m.index === regex.lastIndex) {
            regex.lastIndex++;
        }
        var url = m[1];
        if(url){
            instaEvent.emit('gotPost',url);
            images.push(url);
        }
    }
    return images;
}
module.exports = {
    instaEvent: instaEvent,
    startInsta: startInsta,
    getAllImages: getAllImages
};