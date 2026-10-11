/**
 * Configuration module
 */

module.exports = {
  githubToken: process.env.GITHUB_TOKEN || "",
  discordWebhook: process.env.DISCORD_WEBHOOK || "",
  telegramBotToken: process.env.TELEGRAM_BOT_TOKEN || "",
  telegramChatId: process.env.TELEGRAM_CHAT_ID || "",
  scanInterval: parseInt(process.env.SCAN_INTERVAL || "3600", 10),
  targets: [
    { owner: "openscad", repo: "openscad" },
    { owner: "elementary", repo: "panel-power" },
    { owner: "useagenthq", repo: "useagent" },
    { owner: "HCTDIP", repo: "corps-jobs" },
    { owner: "relayhop", repo: "sn-monetization-runtime" },
    { owner: "SPLURT-Station", repo: "S.P.L.U.R.T-tg" },
    { owner: "SUSU-LABS", repo: "susu-web" },
    { owner: "SUSU-LABS", repo: "susu-indexer" },
    { owner: "codercops", repo: "toolbelt" },
  ],
};
