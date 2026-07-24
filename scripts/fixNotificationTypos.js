#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const { fixTypos } = require('../src/utils/textFormatter');

/**
 * Script to fix typos in notification-related files
 */

const fileExtensions = ['.js', '.json', '.md', '.txt'];
const excludeDirs = ['node_modules', '.git', 'dist', 'build'];

/**
 * Recursively finds files in a directory
 * @param {string} dir - Directory to search
 * @param {Array} fileList - Accumulated file list
 * @returns {Array} - List of file paths
 */
function findFiles(dir, fileList = []) {
  const files = fs.readdirSync(dir);

  files.forEach(file => {
    const filePath = path.join(dir, file);
    const stat = fs.statSync(filePath);

    if (stat.isDirectory()) {
      if (!excludeDirs.includes(file)) {
        findFiles(filePath, fileList);
      }
    } else {
      const ext = path.extname(file);
      if (fileExtensions.includes(ext)) {
        fileList.push(filePath);
      }
    }
  });

  return fileList;
}

/**
 * Fixes typos in a file
 * @param {string} filePath - Path to the file
 * @returns {boolean} - Whether changes were made
 */
function fixFileTypos(filePath) {
  try {
    const content = fs.readFileSync(filePath, 'utf8');
    const fixedContent = fixTypos(content);

    if (content !== fixedContent) {
      fs.writeFileSync(filePath, fixedContent, 'utf8');
      console.log(`✓ Fixed typos in: ${filePath}`);
      return true;
    }
    return false;
  } catch (error) {
    console.error(`✗ Error processing ${filePath}:`, error.message);
    return false;
  }
}

/**
 * Main function
 */
function main() {
  console.log('🔍 Searching for files with typos...\n');

  const rootDir = process.cwd();
  const files = findFiles(rootDir);
  
  let fixedCount = 0;

  files.forEach(file => {
    if (fixFileTypos(file)) {
      fixedCount++;
    }
  });

  console.log(`\n✨ Fixed typos in ${fixedCount} file(s)`);
}

if (require.main === module) {
  main();
}

module.exports = { findFiles, fixFileTypos };
