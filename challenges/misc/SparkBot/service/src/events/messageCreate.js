const { getGuildDB, permlevel, defaultDB } = require("../modules/functions.js");

// The MESSAGE event runs anytime a message is received
// Note that due to the binding of client to every event, every event
// goes `client, other, args` when this function is run.

module.exports = async (client, message) => {

	// Grab the container from the client to reduce line length.
	const { container } = client;
	// It's good practice to ignore other bots. This also makes your bot ignore itself
	// and not get into a spam loop (we call that "botception").
	if (message.author.bot) return;

	// Grab the settings for this server from mongoose.
	// If there is no guild, get default conf (DMs) and create guild document
	const settings = await getGuildDB(message.guild) ? await getGuildDB(message.guild) : await defaultDB(message.guild);

	// Checks if the bot was mentioned via regex, with no message after it,
	// returns the prefix. The reason why we used regex here instead of
	// message.mentions is because of the mention prefix later on in the
	// code, would render it useless.
	const prefixMention = new RegExp(`^<@!?${client.user.id}> ?$`);
	if (message.content.match(prefixMention)) {
		return message.reply(`My prefix on this guild is \`${settings.prefix}\``);
	}

	// It's also good practice to ignore any and all messages that do not start
	// with our prefix, or a bot mention.
	const prefix = new RegExp(`^<@!?${client.user.id}> |^\\${settings.prefix}`).exec(message.content);
	// This will return and stop the code from continuing if it's missing
	// our prefix (be it mention or from the settings).
	if (!prefix) return;

	// Here we separate our "command" name, and our "arguments" for the command.
	// e.g. if we have the message "+say Is this the real life?" , we'll get the following:
	// command = say
	// args = ["Is", "this", "the", "real", "life?"]
	const args = message.content.slice(prefix[0].length).trim().split(/ +/g);
	const command = args.shift().toLowerCase();

	// If the member on a guild is invisible or not cached, fetch them.
	if (message.guild && !message.member) await message.guild.members.fetch(message.author);

	// Get the user or member's permission level from the elevation
	const level = await permlevel(message);

	// Check whether the command, or alias, exist in the collections defined
	// in app.js.
	const cmd = container.commands.get(command) || container.commands.get(container.aliases.get(command));
	// using this const varName = thing OR otherThing; is a pretty efficient
	// and clean way to grab one of 2 values!
	if (!cmd) return;

	// Some commands may not be useable in DMs. This check prevents those commands from running
	// and return a friendly error message.
	if (cmd && !message.guild && cmd.conf.guildOnly)
		return message.channel.send("This command is unavailable via private message. Please run this command in a guild.");

	if (!cmd.conf.enabled) return;

	// To simplify message arguments, the author's level is now put on level (not member so it is supported in DMs)
	// The "level" command module argument will be deprecated in the future.
	message.author.permLevel = level;

	message.flags = [];
	while (args[0] && args[0][0] === "-") {
		message.flags.push(args.shift().slice(1));
	}
	// If the command exists, **AND** the user has permission, run it.
	try {
		await cmd.run(client, message, args, level);
	} catch (e) {
		console.error(e);
		message.channel.send({ content: `There was a problem with your request.\n\`\`\`${e.message}\`\`\`` })
			.catch(e => console.error("An error occurred replying on an error", e));
	}
};
