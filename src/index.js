#!/usr/bin/env node
/**
 * BountyScout - Scans GitHub for bounty opportunities
 * 
 * This tool monitors repositories for issues with bounties and
 * generates alerts when new opportunities are found.
 */

const { Octokit } = require("@octokit/rest");
const config = require("./config");
const scanner = require("./scanner");
const notifier = require("./notifier");
const logger = require("./logger");

class BountyScout {
  constructor() {
    this.octokit = new Octokit({
      auth: config.githubToken,
    });
    this.config = config;
  }

  async run() {
    logger.info("Starting BountyScout scan...");
    
    try {
      const results = await scanner.scan(config.targets);
      logger.info(`Scan complete. Found ${results.length} opportunities.`);
      
      if (results.length > 0) {
        const alert = notifier.formatAlert(results);
        logger.info(alert);
        await notifier.send(alert);
      } else {
        logger.info("No new opportunities found.");
      }
    } catch (error) {
      logger.error(`Scan failed: ${error.message}`);
      process.exit(1);
    }
  }
}

const scout = new BountyScout();
scout.run().catch(console.error);
