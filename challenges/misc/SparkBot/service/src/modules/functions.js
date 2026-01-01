const logger = require("./Logger.js");
const config = require("../config.js");
const guildSettings = require("../models/guildSettings");
const { MessageEmbed } = require("discord.js");
// Let's start by getting some useful functions that we'll use throughout
// the bot, like logs and elevation features.

/*
  GUILD SETTINGS FUNCTION

  FIND guild's settings model in database

*/
async function getGuildDB(guild) {
	const guildDB = await guildSettings.findOne({ guildID: guild.id });
	return guildDB;
}

/*
  GUILD SETTINGS DEFAULT AND CREATE SETTINGS FUNCTION

  IF guild has no settings model in database,
  CREATE guild settings and
  RETURN default guild settings

*/
async function defaultDB(guild) {
	const prefix = config["defaultSettings"]["prefix"];
	logger.debug("Prefix:" + prefix);
	const newGuildDB = new guildSettings({
		guildID: guild.id,
		prefix: config["defaultSettings"]["prefix"]
	});
	await newGuildDB.save();

	return {
		guildID: String,
		prefix: String
	};
}

/*
  PERMISSION LEVEL FUNCTION

  This is a very basic permission system for commands which uses "levels"
  "spaces" are intentionally left black so you can add them if you want.
  NEVER GIVE ANYONE BUT OWNER THE LEVEL 10! By default this can run any
  command including the VERY DANGEROUS `eval` and `exec` commands!

  */
async function permlevel(message) {
	let permlvl = 0;

	const permOrder = config.permLevels.slice(0).sort((p, c) => p.level < c.level ? 1 : -1);
	const settings = await getGuildDB(message.guild) ? await getGuildDB(message.guild) : await defaultDB(message.guild);
	while (permOrder.length) {
		const currentLevel = permOrder.shift();
		if (message.guild && currentLevel.guildOnly) continue;
		if (currentLevel.check(message, settings)) {
			permlvl = currentLevel.level;
			break;
		}
	}
	return permlvl;
}

/*
  GET USER FROM PARAM

  FIND user from message through
  - mentions
  - id
  - name

*/
function getUser(client, param) {
	const mentionResolver = param.replace("<@", "").replace(">", "");
	logger.debug("Mention Resolved: " + mentionResolver);
	const userResolver = client.users.cache.get(mentionResolver) || client.users.cache.find(user => user.username === param);
	return userResolver;
}

/*
  GET CHANNEL FROM PARAM

  FIND channel from message through
  - mentions
  - id
  - name

*/
function getChannel(client, param) {
	const mentionResolver = param.replace("<#", "").replace(">", "");
	const channelResolver = client.channels.cache.get(mentionResolver) || client.channels.cache.find(c => c.name === param);
	return channelResolver;
}

/*
  GET ROLE FROM PARAM

  FIND role from message through
  - mentions
  - id
  - name

*/
function getRole(guild, param) {
	const mentionResolver = param.replace("<@&", "").replace(">", "");
	const roleResolver = guild.roles.cache.get(mentionResolver) || guild.roles.cache.find(r => r.name === param);
	return roleResolver;
}

/*
  GET EMOJI FROM PARAM

  FIND emoji from message through
  - <:emojiName:emojiID>

*/
function getEmoji(guild, param) {
	if (!param.includes(":")) return { name: param };
	const emojiName = param.replace("<", "").replace(">", "");
	const emojiResolver = guild.emojis.cache.find(emoji => emoji.name === emojiName);
	return emojiResolver;
}

/*
  PROMPT SUCCESS EMBED

  SEND a response in embed upon successful result

*/
async function promptSuccessEmbed(msg, content) {
	const successColor = "#8ef9a5";
	const successEmbed = new MessageEmbed()
		.setColor(successColor)
		.setTitle("✅ Success!")
		.setDescription(content);
	msg.channel.send({ embeds: [ successEmbed ]});
}

/*
  PROMPT FAILURE EMBED

  SEND a response in embed upon failed result

*/
async function promptFailureEmbed(msg, content) {
	const failColor = "#ff4d00";
	const failureEmbed = new MessageEmbed()
		.setColor(failColor)
		.setTitle("❌ Woops, something went wrong.")
		.setDescription(content);
	msg.channel.send({ embeds: [ failureEmbed ]});
}

//
/*
  PROMPT ALERT EMBED

  SEND a response in embed upon invalid parameters

*/
async function promptAlertEmbed(msg, content) {
	const alertColor = "#FFA700";
	const alertEmbed = new MessageEmbed()
		.setColor(alertColor)
		.setTitle("⚠️ Yikes, invalid Usage!")
		.setDescription(content);
	msg.channel.send({ embeds: [ alertEmbed ]});
}

/*
  PROMPT SUCCESS EMBED

  SEND a response in embed upon successful result

*/
async function promptSuccessEmbedOnSlash(interaction, content, ephemeral) {
	ephemeral ? null : ephemeral == false;
	const successColor = "#8ef9a5";
	const successEmbed = new MessageEmbed()
		.setColor(successColor)
		.setTitle("✅ Success!")
		.setDescription(content);
	interaction.reply({ embeds: [ successEmbed ], ephemeral: ephemeral });
}

/*
  PROMPT FAILURE EMBED

  SEND a response in embed upon failed result

*/
async function promptFailureEmbedOnSlash(interaction, content, ephemeral) {
	ephemeral ? null : ephemeral == false;
	const failColor = "#ff4d00";
	const failureEmbed = new MessageEmbed()
		.setColor(failColor)
		.setTitle("❌ Woops, something went wrong.")
		.setDescription(content);
	interaction.reply({ embeds: [ failureEmbed ], ephemeral: ephemeral});
}

//
/*
  PROMPT ALERT EMBED

  SEND a response in embed upon invalid parameters

*/
async function promptAlertEmbedOnSlash(interaction, content, ephemeral) {
	ephemeral ? null : ephemeral == false;
	ephemeral ? ephemeral == false : null;
	const alertColor = "#FFA700";
	const alertEmbed = new MessageEmbed()
		.setColor(alertColor)
		.setTitle("⚠️ Yikes, invalid Usage!")
		.setDescription(content);
	interaction.reply({ embeds: [ alertEmbed ], ephemeral: ephemeral});
}

/*
  SINGLE-LINE AWAIT MESSAGE

  A simple way to grab a single reply, from the user that initiated
  the command. Useful to get "precisions" on certain things...

  USAGE

  const response = await awaitReply(msg, "Favourite Color?");
  msg.reply(`Oh, I really love ${response} too!`);

*/
async function awaitReply(msg, question, limit = 60000) {
	const filter = m => m.author.id === msg.author.id;
	await msg.channel.send(question);
	try {
		const collected = await msg.channel.awaitMessages({ filter, max: 1, time: limit, errors: ["time"] });
		return collected.first().content;
	} catch (e) {
		return false;
	}
}


/* MISCELLANEOUS NON-CRITICAL FUNCTIONS */

// toProperCase(String) returns a proper-cased string such as:
// toProperCase("Mary had a little lamb") returns "Mary Had A Little Lamb"
function toProperCase(string) {
	return string.replace(/([^\W_]+[^\s-]*) */g, (txt) => txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase());
}

// These 2 process methods will catch exceptions and give *more details* about the error and stack trace.
process.on("uncaughtException", (err) => {
	const errorMsg = err.stack.replace(new RegExp(`${__dirname}/`, "g"), "./");
	logger.error(`Uncaught Exception: ${errorMsg}`);
	console.error(err);
	// Always best practice to let the code crash on uncaught exceptions.
	// Because you should be catching them anyway.
	process.exit(1);
});

process.on("unhandledRejection", err => {
	logger.error(`Unhandled rejection: ${err}`);
	console.error(err);
});

module.exports = {
	getGuildDB,
	getUser,
	getChannel,
	getRole,
	getEmoji,
	defaultDB,
	promptSuccessEmbed,
	promptFailureEmbed,
	promptAlertEmbed,
	promptSuccessEmbedOnSlash,
	promptFailureEmbedOnSlash,
	promptAlertEmbedOnSlash,
	permlevel,
	awaitReply,
	toProperCase
};
