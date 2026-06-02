javascript
/**
 * data.js - Static data module containing active bounty scan results
 * @module data
 * @version 3.0.0
 * @author Production Team
 * @license MIT
 */

import { createLogger, format, transports } from 'winston';
import { z } from 'zod';
import { RateLimiter } from 'limiter';
import { createHash } from 'crypto';

// ============================================================================
// Logging Configuration
// ============================================================================

const logger = createLogger({
  level: process.env.LOG_LEVEL || 'info',
  format: format.combine(
    format.timestamp({ format: 'YYYY-MM-DD HH:mm:ss.SSS' }),
    format.errors({ stack: true }),
    format.json()
  ),
  defaultMeta: { 
    service: 'bounty-data-module',
    environment: process.env.NODE_ENV || 'development'
  },
  transports: [
    new transports.Console({
      format: format.combine(
        format.colorize(),
        format.printf(({ timestamp, level, message, ...meta }) => {
          const metaStr = Object.keys(meta).length ? ` ${JSON.stringify(meta, null, 2)}` : '';
          return `${timestamp} [${level}]: ${message}${metaStr}`;
        })
      )
    }),
    new transports.File({ 
      filename: 'logs/bounty-data-error.log', 
      level: 'error',
      maxsize: 5242880,
      maxFiles: 10,
      tailable: true
    }),
    new transports.File({ 
      filename: 'logs/bounty-data-combined.log',
      maxsize: 5242880,
      maxFiles: 10,
      tailable: true
    })
  ],
  exceptionHandlers: [
    new transports.File({ filename: 'logs/exceptions.log' })
  ],
  rejectionHandlers: [
    new transports.File({ filename: 'logs/rejections.log' })
  ]
});

// ============================================================================
// Type Definitions & Validation Schemas
// ============================================================================

/**
 * @typedef {Object} BountyItem
 * @property {number} id - Unique identifier (1-99999)
 * @property {string} title - Bounty title (1-500 chars)
 * @property {string} url - Full URL to the bounty issue
 * @property {string} repository - Repository owner/name
 * @property {string} repositoryUrl - Full URL to the repository
 * @property {number} comments - Number of comments (0-9999)
 * @property {string} lastUpdated - ISO 8601 timestamp
 * @property {string} [severity] - Optional severity level (e.g., "8.7")
 * @property {string} [level] - Optional difficulty level (e.g., "intermediate")
 * @property {string} [type] - Optional bounty type (e.g., "CLAIM", "BOUNTY", "Audit")
 */

/**
 * @typedef {Object} BountyStats
 * @property {number} totalBounties - Total number of bounties
 * @property {number} activeBounties - Number of active bounties
 * @property {Object} typeDistribution - Distribution of bounty types
 * @property {Object} severityDistribution - Distribution of severity levels
 * @property {Date} lastUpdated - Last update timestamp
 */

/**
 * @typedef {Object} CacheEntry
 * @property {unknown} data - Cached data
 * @property {number} timestamp - Cache entry timestamp
 * @property {string} hash - Content hash for integrity
 */

/**
 * Zod schema for runtime validation of bounty items
 */
const BountyItemSchema = z.object({
  id: z.number()
    .int()
    .positive()
    .max(99999)
    .describe('Unique identifier for the bounty'),
  
  title: z.string()
    .min(1, 'Title cannot be empty')
    .max(500, 'Title exceeds maximum length')
    .transform(val => val.replace(/[<>]/g, '').trim())
    .describe('Bounty title'),
  
  url: z.string()
    .url('Invalid URL format')
    .regex(/^https?:\/\/github\.com\//, 'URL must be a GitHub URL')
    .describe('Full URL to the bounty issue'),
  
  repository: z.string()
    .min(1, 'Repository name cannot be empty')
    .regex(/^[a-zA-Z0-9_.-]+\/[a-zA-Z0-9_.-]+$/, 'Invalid repository format (owner/repo)')
    .describe('Repository owner/name'),
  
  repositoryUrl: z.string()
    .url('Invalid repository URL format')
    .regex(/^https?:\/\/github\.com\//, 'Repository URL must be a GitHub URL')
    .describe('Full URL to the repository'),
  
  comments: z.number()
    .int()
    .min(0, 'Comments cannot be negative')
    .max(9999, 'Comments count exceeds maximum')
    .default(0)
    .describe('Number of comments'),
  
  lastUpdated: z.string()
    .datetime({ message: 'Invalid ISO 8601 datetime format' })
    .describe('ISO 8601 timestamp'),
  
  severity: z.string()
    .regex(/^\d+(\.\d+)?$/, 'Severity must be a numeric value')
    .optional()
    .describe('Optional severity level'),
  
  level: z.enum(['beginner', 'intermediate', 'advanced', 'expert'])
    .optional()
    .describe('Optional difficulty level'),
  
  type: z.enum(['CLAIM', 'BOUNTY', 'Audit', 'ISSUE'])
    .optional()
    .default('ISSUE')
    .describe('Optional bounty type')
});

/**
 * @typedef {z.infer<typeof BountyItemSchema>} ValidatedBountyItem
 */

// ============================================================================
// Constants
// ============================================================================

const VALID_TYPES = ['CLAIM', 'BOUNTY', 'Audit', 'ISSUE'] as const;
const VALID_LEVELS = ['beginner', 'intermediate', 'advanced', 'expert'] as const;
const MAX_BOUNTY_COUNT = 1000;
const CACHE_TTL = 5 * 60 * 1000;
const MAX_RETRIES = 3;
const RATE_LIMIT_TOKENS = 100;
const RATE_LIMIT_INTERVAL = 60000;

// ============================================================================
// Rate Limiter
// ============================================================================

const rateLimiter = new RateLimiter({
  tokensPerInterval: RATE_LIMIT_TOKENS,
  interval: RATE_LIMIT_INTERVAL
});

// ============================================================================
// Custom Error Classes
// ============================================================================

class BountyValidationError extends Error {
  constructor(message: string, public readonly details?: unknown) {
    super(message);
    this.name = 'BountyValidationError';
  }
}

class BountySecurityError extends Error {
  constructor(message: string, public readonly severity: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL') {
    super(message);
    this.name = 'BountySecurityError';
  }
}

class BountyCacheError extends Error {
  constructor(message: string, public readonly cacheKey?: string) {
    super(message);
    this.name = 'BountyCacheError';
  }
}

// ============================================================================
// Data Validation & Initialization
// ============================================================================

/**
 * Validates and sanitizes a single bounty item
 * @param {unknown} item - Raw bounty data to validate
 * @returns {ValidatedBountyItem} Validated and sanitized bounty item
 * @throws {BountyValidationError} If validation fails
 * @throws {BountySecurityError} If security check fails
 */
function validateBountyItem(item: unknown): ValidatedBountyItem {
  try {
    const validated = BountyItemSchema.parse(item);
    
    // Security checks
    const securityChecks = [
      { check: validated.title.includes('<script>'), message: 'Potential XSS attack detected in bounty title', severity: 'HIGH' as const },
      { check: validated.title.includes('javascript:'), message: 'Potential XSS attack detected in bounty title', severity: 'HIGH' as const },
      { check: validated.title.includes('onerror='), message: 'Potential XSS attack detected in bounty title', severity: 'HIGH' as const },
      { check: validated.title.includes('onload='), message: 'Potential XSS attack detected in bounty title', severity: 'HIGH' as const },
      { check: validated.url.includes('\\'), message: 'Potential path traversal in URL', severity: 'MEDIUM' as const },
      { check: validated.repositoryUrl.includes('\\'), message: 'Potential path traversal in repository URL', severity: 'MEDIUM' as const }
    ];
    
    for (const { check, message, severity } of securityChecks) {
      if (check) {
        logger.warn('Security check failed', { message, severity, item: validated.id });
        throw new BountySecurityError(message, severity);
      }
    }
    
    // Validate URL consistency
    const urlRepoMatch = validated.url.match(/github\.com\/([^/]+\/[^/]+)/);
    if (urlRepoMatch && urlRepoMatch[1] !== validated.repository) {
      logger.warn('URL repository mismatch', {
        urlRepo: urlRepoMatch[1],
        declaredRepo: validated.repository,
        itemId: validated.id
      });
    }
    
    return validated;
  } catch (error) {
    if (error instanceof z.ZodError) {
      logger.error('Bounty item validation failed', {
        errors: error.errors,
        item: item
      });
      throw new BountyValidationError(
        `Invalid bounty data: ${error.errors.map(e => e.message).join(', ')}`,
        error.errors
      );
    }
    throw error;
  }
}

/**
 * Validates the entire bounty data array
 * @param {unknown[]} data - Array of bounty items to validate
 * @returns {ValidatedBountyItem[]} Validated bounty items
 * @throws {BountyValidationError} If validation fails
 */
function validateBountyData(data: unknown[]): ValidatedBountyItem[] {
  if (!Array.isArray(data)) {
    throw new BountyValidationError('Bounty data must be an array');
  }
  
  if (data.length === 0) {
    logger.warn('Empty bounty data received');
    return [];
  }
  
  if (data.length > MAX_BOUNTY_COUNT) {
    throw new BountyValidationError(
      `Bounty data exceeds maximum count of ${MAX_BOUNTY_COUNT}. Received: ${data.length}`
    );
  }
  
  const validatedItems: ValidatedBountyItem[] = [];
  const errors: Array<{ index: number; error: Error }> = [];
  
  for (let i = 0; i < data.length; i++) {
    try {
      const validated = validateBountyItem(data[i]);
      validatedItems.push(validated);
    } catch (error) {
      if (error instanceof BountySecurityError) {
        logger.error('Security error in bounty item', {
          index: i,
          error: error.message,
          severity: error.severity
        });
        throw error;
      }
      errors.push({ index: i, error: error as Error });
    }
  }
  
  if (errors.length > 0) {
    logger.error('Validation errors in bounty data', {
      totalErrors: errors.length,
      totalItems: data.length,
      errors: errors.map(e => ({ index: e.index, message: e.error.message }))
    });
    
    if (errors.length > data.length * 0.5) {
      throw new BountyValidationError(
        `Too many validation errors: ${errors.length} out of ${data.length} items failed`
      );
    }
  }
  
  // Check for duplicate IDs
  const idMap = new Map<number, number[]>();
  validatedItems.forEach((item, index) => {
    const existing = idMap.get(item.id) || [];
    existing.push(index);
    idMap.set(item.id, existing);
  });
  
  const duplicates = Array.from(idMap.entries()).filter(([, indices]) => indices.length > 1);
  if (duplicates.length > 0) {
    const duplicateInfo = duplicates.map(([id, indices]) => ({
      id,
      indices,
      titles: indices.map(i => validatedItems[i].title)
    }));
    
    logger.warn('Duplicate bounty IDs found', { duplicates: duplicateInfo });
    
    // Remove duplicates, keeping the first occurrence
    const seenIds = new Set<number>();
    const deduplicated = validatedItems.filter(item => {
      if (seenIds.has(item.id)) {
        return false;
      }
      seenIds.add(item.id);
      return true;
    });
    
    return deduplicated;
  }
  
  return validatedItems;
}

// ============================================================================
// Cache Implementation
// ============================================================================

class BountyCache {
  private cache: Map<string, CacheEntry> = new Map();
  private readonly ttl: number;
  private hits: number = 0;
  private misses: number = 0;
  private evictions: number = 0;

  constructor(ttl: number = CACHE_TTL) {
    this.ttl = ttl;
    
    // Periodic cache cleanup
    setInterval(() => this.cleanup(), this.ttl / 2);
  }

  /**
   * Get cached data if valid
   * @param {string} key - Cache key
   * @returns {unknown | undefined} Cached data or undefined
   */
  get(key: string): unknown | undefined {
    const cached = this.cache.get(key);
    
    if (!cached) {
      this.misses++;
      return undefined;
    }
    
    if (Date.now() - cached.timestamp >= this.ttl) {
      this.cache.delete(key);
      this.evictions++;
      this.misses++;
      return undefined;
    }
    
    // Verify content integrity
    const currentHash = createHash('sha256').update(JSON.stringify(cached.data)).digest('hex');
    if (currentHash !== cached.hash) {
      logger.error('Cache integrity check failed', { key });
      this.cache.delete(key);
      this.evictions++;
      this.misses++;
      return undefined;
    }
    
    this.hits++;
    return cached.data;
  }

  /**
   * Set cache data
   * @param {string} key - Cache key
   * @param {unknown} data - Data to cache
   */
  set(key: string, data: unknown): void {
    const hash = createHash('sha256').update(JSON.stringify(data)).digest('hex');
    
    this.cache.set(key, {
      data,
      timestamp: Date.now(),
      hash
    });
    
    // Enforce cache size limit
    if (this.cache.size > 1000) {
      const oldestKey = this.cache.entries().next().value?.[0];
      if (oldestKey) {
        this.cache.delete(oldestKey);
        this.evictions++;
      }
    }
  }

  /**
   * Clear all cache
   */
  clear(): void {
    const size = this.cache.size;
    this.cache.clear();
    logger.info('Cache cleared', { previousSize: size });
  }

  /**
   * Remove expired entries
   */
  private cleanup(): void {
    const now = Date.now();
    let cleaned = 0;
    
    this.cache.forEach((entry, key) => {
      if (now - entry.timestamp >= this.ttl) {
        this.cache.delete(key);
        cleaned++;
        this.evictions++;
      }
    });
    
    if (cleaned > 0) {
      logger.debug('Cache cleanup completed', { removedEntries: cleaned });
    }
  }

  /**
   * Get cache statistics
   * @returns {Object} Cache statistics
   */
  getStats(): { 
    size: number; 
    hits: number; 
    misses: number; 
    evictions: number;
    hitRate: number;
    oldestEntry: number | null;
    memoryUsage: number;
  } {
    let oldestEntry: number | null = null;
    let memoryUsage = 0;
    
    this.cache.forEach(entry => {
      if (oldestEntry === null || entry.timestamp < oldestEntry) {
        oldestEntry = entry.timestamp;
      }
      memoryUsage += JSON.stringify(entry).length;
    });
    
    const totalRequests = this.hits + this.misses;
    
    return {
      size: this.cache.size,
      hits: this.hits,
      misses: this.misses,
      evictions: this.evictions,
      hitRate: totalRequests > 0 ? this.hits / totalRequests : 0,
      oldestEntry,
      memoryUsage
    };
  }
}

// ============================================================================
// Statistics Calculator
// ============================================================================

class BountyStatistics {
  /**
   * Calculate statistics from bounty data
   * @param {ValidatedBountyItem[]} bounties - Array of validated bounty items
   * @returns {BountyStats} Calculated statistics
   */
  static calculate(bounties: ValidatedBountyItem[]): BountyStats {
    const typeDistribution: Record<string, number> = {};
    const severityDistribution: Record<string, number> = {};
    
    for (const bounty of bounties) {
      // Type distribution
      const type = bounty.type || 'ISSUE';
      typeDistribution[type] = (typeDistribution[type] || 0) + 1;
      
      // Severity distribution
      if (bounty.severity) {
        const severityKey = parseFloat(bounty.severity).toFixed(1);
        severityDistribution[severityKey] = (severityDistribution[severityKey] || 0) + 1;
      }
    }
    
    return {
      totalBounties: bounties.length,
      activeBounties: bounties.filter(b => b.comments < 100).length,
      typeDistribution,
      severityDistribution,
      lastUpdated: new Date()
    };
  }
}

// ============================================================================
// Main Data Module
// ============================================================================

class BountyDataModule {
  private cache: BountyCache;
  private data: ValidatedBountyItem[] = [];
  private stats: BountyStats | null = null;
  private initialized: boolean = false;

  constructor() {
    this.cache = new BountyCache();
  }

  /**
   * Initialize the module with bounty data
   * @param {unknown[]} rawData - Raw bounty data
   * @returns {Promise<ValidatedBountyItem[]>} Validated bounty items
   */
  async initialize(rawData: unknown[]): Promise<