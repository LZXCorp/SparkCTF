const mongoose = require("mongoose");

const guildSettingsSchema = mongoose.Schema({
	guildID: String,
	prefix: String,
	modRoles: {
		moderatorRole: [{ roleID: String }],
		administratorRole: [{ roleID: String }]
	},
});

module.exports = mongoose.model("guildSettings", guildSettingsSchema);
