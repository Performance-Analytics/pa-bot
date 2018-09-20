/**
 * Performance Analytics Bot
 * main.ts
 * Copyright (c) 2018 Performance Analytics
 * License: MIT
 */

const Discord = require("discord.js");
const client = new Discord.Client();

// Enter your bot token here.
const bot_token: string = null;

client.on("ready", () => {
    console.log(`Logged in as ${client.user.tag}!`);
});

client.on("message", (msg) => {
    console.log(`
        ${msg.author.username}#${msg.author.discriminator}@${msg.channel.guild.name}#${msg.channel.name}
        ${msg.content}
    `);
});

client.login(bot_token);
