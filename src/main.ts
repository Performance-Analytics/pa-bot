/**
 * Performance Analytics Bot
 * main.ts
 * Copyright (c) 2018 Performance Analytics
 * License: MIT
 */

const promptjs = require("prompt");

const Discord = require("discord.js");
const client = new Discord.Client();

// Enter your bot token here.
const bot_token: string = "NDg4NDI0MDI2NTkxNTkyNDYx.DoSdlA.YHbHxZiBPrgJOT6rjcJ6Fq_YG_U";

function command_prompt_loop(): void
{
    promptjs.start();

    function run_command(): void
    {
        promptjs.get("command", (err, result) => {
            if (err) {
                console.log(); // Print empty line.
                process.exit(); // Exit program.
            } else {
                console.log(result.command);
                run_command();
            }
        });
    }
    run_command();
}

client.on("ready", () => {
    console.log(`Logged in as ${client.user.tag}!`);

    command_prompt_loop();
});

client.on("message", (msg) => {
    console.log(`
        ${msg.author.username}#${msg.author.discriminator}@${msg.channel.guild.name}#${msg.channel.name}
        ${msg.content}
    `);
});

client.login(bot_token);
