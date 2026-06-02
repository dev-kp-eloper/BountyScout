javascript
// js/main.js
// Core JavaScript for dynamic content rendering, search/filter functionality, and dark mode toggle

(function () {
  'use strict';

  // ============================================================
  // Configuration & State
  // ============================================================

  const CONFIG = Object.freeze({
    storageKey: 'bountyScoutTheme',
    searchDebounceMs: 300,
    resultsPerPage: 10,
    selectors: Object.freeze({
      container: '#bounty-results',
      searchInput: '#bounty-search',
      filterSelect: '#bounty-filter',
      darkToggle: '#dark-mode-toggle',
      pagination: '#bounty-pagination',
      resultsCount: '#results-count',
      loadingIndicator: '#loading-indicator',
      errorMessage: '#error-message',
    }),
    apiEndpoint: '/api/bounties',
    severityThresholds: Object.freeze({
      critical: 9,
      high: 7,
      medium: 4,
      low: 0,
    }),
    pagination: Object.freeze({
      maxVisiblePages: 5,
      edgePages: 1,
    }),
    retryAttempts: 3,
    retryDelay: 1000,
    requestTimeout: 10000,
  });

  /** @type {Object<string, any>} */
  const state = {
    bounties: /** @type {Array<Bounty>} */ ([]),
    filteredBounties: /** @type {Array<Bounty>} */ ([]),
    currentPage: 1,
    isDarkMode: false,
    isLoading: false,
    error: /** @type {string|null} */ (null),
    searchTerm: '',
    filterValue: 'all',
    abortController: /** @type {AbortController|null} */ (null),
  };

  /**
   * @typedef {Object} Bounty
   * @property {string} title
   * @property {string} repository
   * @property {string} [description]
   * @property {string} [severity]
   * @property {string} [lastUpdated]
   * @property {number} [comments]
   * @property {string} [url]
   */

  /**
   * @typedef {Object} PaginationState
   * @property {number} currentPage
   * @property {number} totalPages
   * @property {number} totalResults
   * @property {number} startIndex
   * @property {number} endIndex
   */

  // ============================================================
  // Custom Error Classes
  // ============================================================

  /**
   * Custom error for DOM element not found
   * @extends Error
   */
  class ElementNotFoundError extends Error {
    /**
     * @param {string} selector - CSS selector of the missing element
     */
    constructor(selector) {
      super(`BountyScout: Required container element not found: ${selector}`);
      this.name = 'ElementNotFoundError';
      this.selector = selector;
    }
  }

  /**
   * Custom error for API failures
   * @extends Error
   */
  class ApiError extends Error {
    /**
     * @param {number} statusCode - HTTP status code
     * @param {string} statusText - HTTP status text
     */
    constructor(statusCode, statusText) {
      super(`HTTP ${statusCode}: ${statusText}`);
      this.name = 'ApiError';
      this.statusCode = statusCode;
      this.statusText = statusText;
    }
  }

  /**
   * Custom error for invalid response format
   * @extends Error
   */
  class InvalidResponseError extends Error {
    /**
     * @param {string} message - Error description
     */
    constructor(message = 'Invalid response format: expected an array') {
      super(message);
      this.name = 'InvalidResponseError';
    }
  }

  /**
   * Custom error for request timeout
   * @extends Error
   */
  class RequestTimeoutError extends Error {
    constructor() {
      super('Request timed out. Please try again.');
      this.name = 'RequestTimeoutError';
    }
  }

  // ============================================================
  // Logger
  // ============================================================

  const Logger = Object.freeze({
    /** @type {'debug'|'info'|'warn'|'error'} */
    level: 'info',

    /** @type {Map<string, number>} */
    _timers: new Map(),

    /**
     * Log levels in order of severity
     * @type {Object<string, number>}
     */
    _levels: Object.freeze({
      debug: 0,
      info: 1,
      warn: 2,
      error: 3,
    }),

    /**
     * Checks if a log level should be displayed
     * @param {string} level - Log level to check
     * @returns {boolean}
     */
    _shouldLog(level) {
      return this._levels[level] >= this._levels[this.level];
    },

    /**
     * Formats a log message with timestamp and prefix
     * @param {string} level - Log level
     * @param {string} message - Log message
     * @returns {string}
     */
    _formatMessage(level, message) {
      const timestamp = new Date().toISOString();
      return `[${timestamp}] [BountyScout] [${level.toUpperCase()}] ${message}`;
    },

    /**
     * @param {string} message
     * @param {...any} args
     */
    debug(message, ...args) {
      if (this._shouldLog('debug')) {
        console.debug(this._formatMessage('debug', message), ...args);
      }
    },

    /**
     * @param {string} message
     * @param {...any} args
     */
    info(message, ...args) {
      if (this._shouldLog('info')) {
        console.info(this._formatMessage('info', message), ...args);
      }
    },

    /**
     * @param {string} message
     * @param {...any} args
     */
    warn(message, ...args) {
      if (this._shouldLog('warn')) {
        console.warn(this._formatMessage('warn', message), ...args);
      }
    },

    /**
     * @param {string} message
     * @param {...any} args
     */
    error(message, ...args) {
      if (this._shouldLog('error')) {
        console.error(this._formatMessage('error', message), ...args);
      }
    },

    /**
     * Starts a performance timer
     * @param {string} label - Timer identifier
     */
    time(label) {
      if (this._shouldLog('debug')) {
        this._timers.set(label, performance.now());
      }
    },

    /**
     * Ends a performance timer and logs the duration
     * @param {string} label - Timer identifier
     */
    timeEnd(label) {
      if (this._shouldLog('debug')) {
        const start = this._timers.get(label);
        if (start !== undefined) {
          const duration = performance.now() - start;
          this.debug(`${label}: ${duration.toFixed(2)}ms`);
          this._timers.delete(label);
        }
      }
    },
  });

  // ============================================================
  // DOM References (cached after DOM ready)
  // ============================================================

  /** @type {Object<string, HTMLElement|null>} */
  let els = {};

  /**
   * Caches DOM element references for performance
   * @throws {ElementNotFoundError} If critical elements are missing
   */
  function cacheElements() {
    Logger.time('cacheElements');
    try {
      const s = CONFIG.selectors;
      els = {
        container: document.querySelector(s.container),
        searchInput: document.querySelector(s.searchInput),
        filterSelect: document.querySelector(s.filterSelect),
        darkToggle: document.querySelector(s.darkToggle),
        pagination: document.querySelector(s.pagination),
        resultsCount: document.querySelector(s.resultsCount),
        loadingIndicator: document.querySelector(s.loadingIndicator),
        errorMessage: document.querySelector(s.errorMessage),
      };

      if (!els.container) {
        throw new ElementNotFoundError(s.container);
      }

      Logger.debug('DOM elements cached successfully');
    } finally {
      Logger.timeEnd('cacheElements');
    }
  }

  // ============================================================
  // Utility Functions
  // ============================================================

  /**
   * Creates a debounced version of a function with leading option
   * @param {Function} fn - Function to debounce
   * @param {number} delay - Delay in milliseconds
   * @param {Object} [options] - Debounce options
   * @param {boolean} [options.leading=false] - Execute on leading edge
   * @param {boolean} [options.trailing=true] - Execute on trailing edge
   * @returns {Function & { cancel: Function, flush: Function }} Debounced function
   */
  function debounce(fn, delay, options = {}) {
    const { leading = false, trailing = true } = options;
    /** @type {number|null} */
    let timer = null;
    /** @type {any[]|null} */
    let lastArgs = null;
    /** @type {boolean} */
    let leadingCalled = false;

    /**
     * Clears the pending timeout
     */
    function cancel() {
      if (timer !== null) {
        clearTimeout(timer);
        timer = null;
      }
      leadingCalled = false;
      lastArgs = null;
    }

    /**
     * Immediately invokes the function with the last arguments
     */
    function flush() {
      if (lastArgs !== null) {
        const args = lastArgs;
        cancel();
        fn.apply(this, args);
      }
    }

    const debounced = function (...args) {
      lastArgs = args;
      
      if (leading && !leadingCalled) {
        leadingCalled = true;
        fn.apply(this, args);
      }

      if (timer !== null) {
        clearTimeout(timer);
      }

      if (trailing) {
        timer = window.setTimeout(() => {
          timer = null;
          leadingCalled = false;
          if (trailing && lastArgs) {
            fn.apply(this, lastArgs);
          }
          lastArgs = null;
        }, delay);
      }
    };

    debounced.cancel = cancel;
    debounced.flush = flush;

    return debounced;
  }

  /**
   * Creates a throttled version of a function
   * @param {Function} fn - Function to throttle
   * @param {number} limit - Minimum interval between executions
   * @returns {Function} Throttled function
   */
  function throttle(fn, limit) {
    /** @type {boolean} */
    let inThrottle = false;
    /** @type {any[]|null} */
    let lastArgs = null;

    return function (...args) {
      if (inThrottle) {
        lastArgs = args;
        return;
      }

      fn.apply(this, args);
      inThrottle = true;
      lastArgs = null;

      window.setTimeout(() => {
        inThrottle = false;
        if (lastArgs) {
          fn.apply(this, lastArgs);
          lastArgs = null;
        }
      }, limit);
    };
  }

  /**
   * Escapes HTML special characters to prevent XSS
   * @param {string} text - Text to escape
   * @returns {string} Escaped HTML string
   */
  function escapeHtml(text) {
    if (typeof text !== 'string') {
      return String(text);
    }
    const div = document.createElement('div');
    div.appendChild(document.createTextNode(text));
    return div.innerHTML;
  }

  /**
   * Sanitizes a string for use in HTML attributes
   * @param {string} value - Value to sanitize
   * @returns {string} Sanitized value
   */
  function sanitizeAttribute(value) {
    if (typeof value !== 'string') {
      return String(value);
    }
    return value.replace(/["'&<>]/g, (char) => {
      switch (char) {
        case '"': return '&quot;';
        case "'": return '&#39;';
        case '&': return '&amp;';
        case '<': return '&lt;';
        case '>': return '&gt;';
        default: return char;
      }
    });
  }

  /**
   * Formats an ISO date string to a human-readable format
   * @param {string|null|undefined} isoString - ISO date string
   * @returns {string} Formatted date string
   */
  function formatDate(isoString) {
    if (!isoString) return 'N/A';
    try {
      const date = new Date(isoString);
      if (isNaN(date.getTime())) {
        Logger.warn('Invalid date format:', isoString);
        return isoString;
      }
      return date.toLocaleString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        timeZoneName: 'short',
      });
    } catch (error) {
      Logger.error('Date formatting error:', error);
      return isoString;
    }
  }

  /**
   * Returns a color for a given severity value
   * @param {string|null|undefined} severity - Severity value
   * @returns {string} CSS color value
   */
  function getSeverityColor(severity) {
    if (!severity) return 'var(--text-secondary)';
    const num = parseFloat(severity);
    if (isNaN(num)) return 'var(--text-secondary)';
    if (num >= CONFIG.severityThresholds.critical) return '#d93025';
    if (num >= CONFIG.severityThresholds.high) return '#ea4335';
    if (num >= CONFIG.severityThresholds.medium) return '#f9ab00';
    return '#34a853';
  }

  /**
   * Validates that a value is a non-empty string
   * @param {any} value - Value to validate
   * @param {string} name - Name of the parameter for error messages
   * @returns {string} Validated string
   * @throws {TypeError} If value is not a non-empty string
   */
  function validateNonEmptyString(value, name) {
    if (typeof value !== 'string' || value.trim().length === 0) {
      throw new TypeError(`${name} must be a non-empty string`);
    }
    return value.trim();
  }

  /**
   * Validates that a value is a positive integer
   * @param {any} value - Value to validate
   * @param {string} name - Name of the parameter for error messages
   * @returns {number} Validated integer
   * @throws {TypeError} If value is not a positive integer
   */
  function validatePositiveInteger(value, name) {
    const num = Number(value);
    if (!Number.isInteger(num) || num <= 0) {
      throw new TypeError(`${name} must be a positive integer`);
    }
    return num;
  }

  // ============================================================
  // Dark Mode
  // ============================================================

  /**
   * Applies the dark/light theme to the document
   * @param {boolean} isDark - Whether dark mode should be enabled
   * @returns {void}
   */
  function applyTheme(isDark) {
    Logger.time('applyTheme');
    try {
      if (typeof isDark !== 'boolean') {
        throw new TypeError('isDark must be a boolean');
      }

      document.documentElement.setAttribute('data-theme', isDark ? 'dark' : 'light');
      
      if (els.darkToggle) {
        els.darkToggle.setAttribute('aria-pressed', String(isDark));
        els.darkToggle.setAttribute('aria-label', isDark ? 'Switch to light mode' : 'Switch to dark mode');
      }
      
      state.isDarkMode = isDark;
      localStorage.setItem(CONFIG.storageKey, isDark ? 'dark' : 'light');
      
      Logger.info(`Theme changed to ${isDark ? 'dark' : 'light'} mode`);
    } catch (error) {
      Logger.error('Failed to apply theme:', error);
    } finally {
      Logger.timeEnd('applyTheme');
    }
  }

  /**
   * Toggles between dark and light mode
   * @returns {void}
   */
  function toggleDarkMode() {
    applyTheme(!state.isDarkMode);
  }

  /**
   * Loads the saved theme preference or detects system preference
   * @returns {void}
   */
  function loadSavedTheme() {
    Logger.time('loadSavedTheme');
    try {
      const saved = localStorage.getItem(CONFIG.storageKey);
      const prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
      const isDark = saved === 'dark' || (!saved && prefersDark);
      applyTheme(isDark);
      
      // Listen for system preference changes
      if (window.matchMedia) {
        const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
        const handleChange = (e) => {
          if (!localStorage.getItem(CONFIG.storageKey)) {
            applyTheme(e.matches);
          }
        };
        
        try {
          mediaQuery.addEventListener('change', handleChange);
        } catch (e) {
          // Fallback for older browsers
          mediaQuery.addListener(handleChange);
        }
      }
    } catch (error) {
      Logger.error('Failed to load saved theme:', error);
      applyTheme(false);
    } finally {
      Logger.timeEnd('loadSavedTheme');
    }
  }

  // ============================================================
  // Data Fetching with Retry Logic
  // ============================================================

  /**
   * Sleep for a given duration
   * @param {number} ms - Milliseconds to sleep
   * @returns {Promise<void>}
   */
  function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  /**
   * Fetches bounty data from the API with retry logic
   * @param {number} [attempt=1] - Current attempt number
   * @returns {Promise<Array<Bounty>>}
   * @throws {ApiError|InvalidResponseError|RequestTimeoutError}
   */
  async function fetchBountiesWithRetry(attempt = 1) {
    Logger.time(`fetchBountiesWithRetry-attempt-${attempt}`);
    
    try {
      // Cancel any existing request
      if (state.abortController) {
        state.abortController.abort();
      }
      
      state.abortController = new AbortController();
      const {