/**
 * Notifier module - Formats and sends bounty alerts
 */

const config = require("./config");
const logger = require("./logger");

function formatAlert(bounties) {
  const scanTime = new Date().toISOString().replace("Z", " UTC");
  
  const lines = [`🎯 Bounty Alert: ${bounties.length} New Opportunities found`];
  lines.push("");
  lines.push(`### Active Bounty Scan Results`);
  lines.push("");
  lines.push(`**Scan Time:** ${scanTime}`);
  lines.push("");

  bounties.forEach((bounty, index) => {
    lines.push(`#### ${index + 1}. [${bounty.title}](${bounty.html_url})`);
    lines.push(`- **Repository:** [${bounty.repository}](${bounty.repository_url || `https://github.com/${bounty.repository}`})`);
    if (bounty.bounty) {
      lines.push(`- **Bounty:** $${bounty.bounty}`);
    }
    lines.push(`- **Comments:** ${bounty.comments}`);
    lines.push(`- **Last Updated:** ${bounty.updated_at}`);
    lines.push("");
  });

  return lines.join("\n");
}

async function send(alert) {
  if (config.discordWebhook) {
    await sendDiscord(alert);
  }
  if (config.telegramBotToken && config.telegramChatId) {
    await sendTelegram(alert);
  }
  logger.info("Alert sent successfully.");
}

async function sendDiscord(alert) {
  const res = await fetch(config.discordWebhook, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ content: alert }),
  });
  if (!res.ok) {
    throw new Error(`Discord webhook failed: ${res.status}`);
  }
}

async function sendTelegram(alert) {
  const url = `https://api.telegram.org/bot${config.telegramBotToken}/sendMessage`;
  const res = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      chat_id: config.telegramChatId,
      text: alert,
      parse_mode: "Markdown",
    }),
  });
  if (!res.ok) {
    throw new Error(`Telegram send failed: ${res.status}`);
  }
}

module.exports = { formatAlert, send };
