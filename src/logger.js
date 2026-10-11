/**
 * Logger module
 */

const LogLevel = { DEBUG: 0, INFO: 1, WARN: 2, ERROR: 3 };
const currentLevel = parseInt(process.env.LOG_LEVEL || "1", 10);

function log(level, message, ...args) {
  if (level >= currentLevel) {
    const timestamp = new Date().toISOString();
    console.log(`[${timestamp}] [${LogLevel[level] ?? "INFO"}] ${message}`, ...args);
  }
}

module.exports = {
  debug: (msg, ...args) => log(LogLevel.DEBUG, msg, ...args),
  info: (msg, ...args) => log(LogLevel.INFO, msg, ...args),
  warn: (msg, ...args) => log(LogLevel.WARN, msg, ...args),
  error: (msg, ...args) => log(LogLevel.ERROR, msg, ...args),
};
