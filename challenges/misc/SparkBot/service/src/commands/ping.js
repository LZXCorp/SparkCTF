exports.run = async (client, message, args, level) => { // eslint-disable-line no-unused-vars
	const reply = await message.channel.send("Ping?");
	await reply.edit(`Pong! Latency is ${reply.createdTimestamp - message.createdTimestamp}ms. API Latency is ${Math.round(client.ws.ping)}ms.`);
};

// Set guildOnly to true if you want it to be available on guilds only.
// Otherwise false is global.
exports.conf = {
	enabled: true,
	guildOnly: true,
	aliases: [],
	permLevel: "User"
};

exports.help = {
	name: "ping",
	category: "Miscellaneous",
	description: "Retrieve Bot and API latency.",
	usage: "ping"
};