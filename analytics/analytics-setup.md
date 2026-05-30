javascript
/**
 * @fileoverview Campaign Builder block management with robust error handling,
 * type safety, logging, input validation, and security.
 * Required fix: Ensure DELETE requests use POST with proper data-method attribute.
 * @version 2.1.1
 */

// ---------------------------------------------------------------------------
// Custom Error Classes
// ---------------------------------------------------------------------------

/**
 * Error for validation failures.
 * @extends Error
 */
class ValidationError extends Error {
  /**
   * @param {string} message - Description of the validation failure.
   */
  constructor(message) {
    super(message);
    this.name = 'ValidationError';
    if (Error.captureStackTrace) {
      Error.captureStackTrace(this, ValidationError);
    }
  }
}

/**
 * Error for network failures.
 * @extends Error
 */
class NetworkError extends Error {
  /**
   * @param {string} message - Description of the network failure.
   * @param {number} [status] - HTTP status code if available.
   * @param {string} [statusText] - HTTP status text.
   */
  constructor(message, status, statusText) {
    super(message);
    this.name = 'NetworkError';
    /** @type {number|undefined} */
    this.status = status;
    /** @type {string|undefined} */
    this.statusText = statusText;
    if (Error.captureStackTrace) {
      Error.captureStackTrace(this, NetworkError);
    }
  }
}

/**
 * Error for security violations (e.g., missing CSRF token).
 * @extends Error
 */
class SecurityError extends Error {
  /**
   * @param {string} message - Description of the security violation.
   */
  constructor(message) {
    super(message);
    this.name = 'SecurityError';
    if (Error.captureStackTrace) {
      Error.captureStackTrace(this, SecurityError);
    }
  }
}

// ---------------------------------------------------------------------------
// Logger Interface
// ---------------------------------------------------------------------------

/**
 * @interface
 */
class Logger {
  /**
   * @param {string} message
   * @param {Object} [context]
   * @returns {void}
   */
  debug(message, context) { throw new Error('Not implemented'); }

  /**
   * @param {string} message
   * @param {Object} [context]
   * @returns {void}
   */
  info(message, context) { throw new Error('Not implemented'); }

  /**
   * @param {string} message
   * @param {Object|Error} [context]
   * @returns {void}
   */
  warn(message, context) { throw new Error('Not implemented'); }

  /**
   * @param {string} message
   * @param {Object|Error} [context]
   * @returns {void}
   */
  error(message, context) { throw new Error('Not implemented'); }
}

/**
 * Console-based logger implementation.
 * @implements {Logger}
 */
class ConsoleLogger {
  /** @inheritDoc */
  debug(message, context) {
    console.debug(`[DEBUG] ${message}`, context !== undefined ? context : '');
  }

  /** @inheritDoc */
  info(message, context) {
    console.info(`[INFO] ${message}`, context !== undefined ? context : '');
  }

  /** @inheritDoc */
  warn(message, context) {
    console.warn(`[WARN] ${message}`, context !== undefined ? context : '');
  }

  /** @inheritDoc */
  error(message, context) {
    console.error(`[ERROR] ${message}`, context !== undefined ? context : '');
  }
}

// ---------------------------------------------------------------------------
// Type Definitions
// ---------------------------------------------------------------------------

/**
 * @typedef {Object} BlockConfig
 * @property {string} blockId - Unique identifier for the block
 * @property {string} method - HTTP method for deletion (always 'POST')
 * @property {string} url - Endpoint URL for deletion
 * @property {boolean} [confirm] - Whether to prompt confirmation
 * @property {string} [csrfToken] - CSRF token for security
 */

/**
 * @typedef {Object} DeleteResult
 * @property {boolean} success
 * @property {string} [error]
 * @property {number} [status]
 */

/**
 * @typedef {Object} CampaignBlockManagerOptions
 * @property {Logger} [logger] - Custom logger instance
 * @property {Object} [csrfConfig] - CSRF token settings (header, param, token)
 * @property {number} [maxRetry] - Maximum number of retry attempts
 * @property {number} [retryDelayMs] - Base delay between retries (ms)
 * @property {number} [timeoutMs] - Request timeout in milliseconds
 */

// ---------------------------------------------------------------------------
// Campaign Block Manager
// ---------------------------------------------------------------------------

/**
 * Campaign Block Manager – handles deletion with maximum robustness.
 * Ensures all delete operations use POST with proper data-method attribute.
 * @class
 */
class CampaignBlockManager {
  /** @type {Logger} */
  #logger;

  /** @type {{ header: string, param: string, token: string }} */
  #csrfConfig;

  /** @type {Map<string, BlockConfig>} */
  #configCache;

  /** @type {number} */
  #maxRetry;

  /** @type {number} */
  #retryDelayMs;

  /** @type {number} */
  #timeoutMs;

  /** @type {WeakMap<Element, Function>} */
  #listenerMap;

  /**
   * @param {CampaignBlockManagerOptions} [options]
   */
  constructor(options = {}) {
    this.#logger = options.logger || new ConsoleLogger();
    this.#csrfConfig = {
      header: 'X-CSRF-Token',
      param: '_csrf_token',
      token: this.#extractCsrfToken(),
      ...options.csrfConfig
    };
    this.#configCache = new Map();
    this.#maxRetry = typeof options.maxRetry === 'number' ? Math.max(0, options.maxRetry) : 2;
    this.#retryDelayMs = typeof options.retryDelayMs === 'number' ? Math.max(100, options.retryDelayMs) : 1000;
    this.#timeoutMs = typeof options.timeoutMs === 'number' ? Math.max(1000, options.timeoutMs) : 15000;
    this.#listenerMap = new WeakMap();
  }

  // -----------------------------------------------------------------------
  // Private Helpers
  // -----------------------------------------------------------------------

  /**
   * Extract CSRF token from the document.
   * @returns {string} - The token value or empty string if not found.
   */
  #extractCsrfToken() {
    try {
      const meta = document.querySelector('meta[name="csrf-token"]');
      const token = meta ? meta.content : '';
      if (!token) {
        this.#logger.warn('CSRF token meta tag not found or empty');
      }
      return token;
    } catch (e) {
      this.#logger.warn('Failed to extract CSRF token from document', e);
      return '';
    }
  }

  /**
   * Validate that the provided element is a valid DOM element with required data attributes.
   * @param {Element} element - The DOM element to validate.
   * @returns {void}
   * @throws {ValidationError} if element is null, not an element, or missing required attributes.
   */
  #validateElement(element) {
    if (!element || !(element instanceof Element)) {
      throw new ValidationError('Invalid element: must be a non-null DOM element');
    }

    const blockId = element.dataset.blockId;
    if (!blockId || typeof blockId !== 'string') {
      throw new ValidationError('Element missing data-block-id attribute');
    }

    // Sanitize blockId to prevent XSS via dataset
    if (/[<>&"']/.test(blockId)) {
      throw new ValidationError('Invalid blockId: contains unsafe characters');
    }

    const url = element.dataset.url;
    if (!url) {
      throw new ValidationError('Element missing data-url attribute');
    }
    // Basic URL validation (relative or absolute)
    try {
      new URL(url, window.location.origin);
    } catch {
      throw new ValidationError('Invalid data-url: not a valid URL');
    }
  }

  /**
   * Extract block configuration from DOM element.
   * @param {Element} element - The DOM element.
   * @returns {BlockConfig} - Configuration object.
   * @throws {ValidationError} if config extraction fails.
   */
  #extractConfig(element) {
    const blockId = element.dataset.blockId;
    if (this.#configCache.has(blockId)) {
      return /** @type {BlockConfig} */ (this.#configCache.get(blockId));
    }

    // Validate and sanitize attributes
    const rawMethod = element.dataset.method || '';
    // Enforce the bug fix: always use POST for delete-like operations
    const method = rawMethod.toUpperCase() === 'POST' ? 'POST' : 'POST';
    const url = element.dataset.url;
    const confirmAttr = element.dataset.confirm;
    const confirm = confirmAttr === 'true' || confirmAttr === '1';
    const csrfToken = element.dataset.csrfToken || this.#csrfConfig.token;

    if (!url) {
      throw new ValidationError('Element missing data-url attribute');
    }

    const config = /** @type {BlockConfig} */ ({
      blockId,
      method,
      url,
      confirm,
      csrfToken
    });

    this.#configCache.set(blockId, config);
    this.#logger.debug(`Extracted config for block ${blockId}`, config);
    return config;
  }

  /**
   * Sanitize a string for safe use in URLs or messages.
   * @param {string} input - Raw string.
   * @returns {string} - Sanitized string.
   */
  #sanitizeInput(input) {
    if (typeof input !== 'string') return '';
    return input.replace(/[<>&"']/g, '').trim();
  }

  /**
   * Calculate delay for retry with exponential backoff.
   * @param {number} attempt - Current retry attempt (0-based).
   * @returns {number} - Delay in milliseconds.
   */
  #getRetryDelay(attempt) {
    const jitter = Math.random() * 300;
    return Math.min(this.#retryDelayMs * Math.pow(2, attempt) + jitter, 30000);
  }

  // -----------------------------------------------------------------------
  // Public API - Event Delegation
  // -----------------------------------------------------------------------

  /**
   * Attach delete handlers to all matching child elements within a root element.
   * Uses event delegation for performance.
   * @param {Element} rootElement - Parent element containing delete triggers.
   * @returns {void}
   * @throws {ValidationError} if rootElement is invalid.
   */
  attachDeleteHandlers(rootElement) {
    if (!rootElement || !(rootElement instanceof Element)) {
      throw new ValidationError('rootElement must be a valid DOM element');
    }

    // Check if a listener is already attached
    if (this.#listenerMap.has(rootElement)) {
      this.#logger.warn('Delete handlers already attached to this root, skipping');
      return;
    }

    const handler = (event) => this.#handleDeleteEvent(event);
    rootElement.addEventListener('click', handler);
    this.#listenerMap.set(rootElement, handler);
    this.#logger.info('Delete handlers attached via event delegation', { root: rootElement.tagName });
  }

  /**
   * Remove delete handlers from a root element.
   * @param {Element} rootElement - Parent element to detach.
   * @returns {void}
   */
  detachDeleteHandlers(rootElement) {
    const handler = this.#listenerMap.get(rootElement);
    if (handler) {
      rootElement.removeEventListener('click', handler);
      this.#listenerMap.delete(rootElement);
      this.#logger.info('Delete handlers detached', { root: rootElement.tagName });
    }
  }

  /**
   * Handle click events and perform block deletion if triggered.
   * @param {Event} event - Click event.
   * @returns {Promise<void>}
   */
  async #handleDeleteEvent(event) {
    const target = event.target;
    // Find the closest delete trigger (e.g. [data-block-id])
    const trigger = target.closest('[data-block-id]');
    if (!trigger) return;

    try {
      this.#validateElement(trigger);
      const config = this.#extractConfig(trigger);
      
      if (config.confirm) {
        const confirmed = await this.#confirmDelete(config);
        if (!confirmed) {
          this.#logger.info('User cancelled deletion', { blockId: config.blockId });
          return;
        }
      }

      await this.#deleteBlock(config);
    } catch (error) {
      this.#logger.error('Delete block failed', error);
      this.#showUserError(error);
    }

    event.preventDefault();
  }

  /**
   * Show confirmation dialog to user.
   * @param {BlockConfig} config - Block configuration.
   * @returns {Promise<boolean>} - Whether user confirmed.
   */
  async #confirmDelete(config) {
    const message = `Are you sure you want to delete block "${config.blockId}"? This action cannot be undone.`;
    return window.confirm(message);
  }

  /**
   * Display user-facing error message.
   * @param {Error} error - The error that occurred.
   * @returns {void}
   */
  #showUserError(error) {
    let message = 'An unexpected error occurred. Please try again.';
    if (error instanceof ValidationError) {
      message = `Invalid input: ${error.message}`;
    } else if (error instanceof NetworkError) {
      message = `Network error (${error.status || 'unknown'}): ${error.message}`;
    } else if (error instanceof SecurityError) {
      message = `Security error: ${error.message}`;
    }
    // In production, integrate with a toast/notification system
    alert(message);
  }

  // -----------------------------------------------------------------------
  // Core Deletion Logic
  // -----------------------------------------------------------------------

  /**
   * Perform the block deletion with retry and CSRF protection.
   * Always uses POST with proper data-method handling.
   * @param {BlockConfig} config - Configuration for the block to delete.
   * @returns {Promise<void>}
   * @throws {ValidationError|NetworkError|SecurityError}
   */
  async #deleteBlock(config) {
    const { blockId, url, method, csrfToken } = config;

    if (!csrfToken) {
      throw new SecurityError('CSRF token is missing. Cannot perform deletion.');
    }

    // Build form data (simulating a POST with a hidden _method field for frameworks like Symfony)
    const formData = new FormData();
    formData.append('_method', 'DELETE'); // Framework override
    formData.append(this.#csrfConfig.param, csrfToken);

    // Fetch options
    const fetchOptions = {
      method: method, // Always POST
      headers: {
        [this.#csrfConfig.header]: csrfToken,
        'X-Requested-With': 'XMLHttpRequest'
      },
      body: formData,
      credentials: 'same-origin',
      signal: AbortSignal.timeout(this.#timeoutMs) // Abort after timeout
    };

    let lastError;
    for (let attempt = 0; attempt <= this.#maxRetry; attempt++) {
      try {
        this.#logger.debug(`Delete attempt ${attempt + 1}/${this.#maxRetry + 1} for block ${blockId}`, { url, method });
        
        const response = await fetch(url, fetchOptions);

        if (!response.ok) {
          // If 403, likely CSRF or missing proper method (the bug fix scenario)
          if (response.status === 403) {
            throw new SecurityError(`CSRF validation failed or method mismatch. Ensure POST is used with data-method=DELETE. (Status: ${response.status})`);
          }
          throw new NetworkError(
            `Server returned error`,
            response.status,
            response.statusText
          );
        }

        // Parse response (optional: check for success field)
        const contentType = response.headers.get('content-type');
        if (contentType && contentType.includes('application/json')) {
          const data = await response.json();
          if (data.success === false) {
            throw new NetworkError(data.error || 'Deletion failed on server', response.status);
          }
        }

        this.#logger.info(`Block ${blockId} deleted successfully`);
        // In production, trigger UI update via event or callback
        this.#onDeleteSuccess(blockId);
        return;
      } catch (error) {
        lastError = error;
        if (error instanceof ValidationError || error instanceof SecurityError) {
          // Do not retry validation or security errors
          throw error;
        }
        if (attempt < this.#maxRetry) {
          const delay = this.#getRetryDelay(attempt);
          this.#logger.warn(`Retrying delete for block ${blockId} in ${delay}ms`, error);
          await new Promise(resolve => setTimeout(resolve, delay));
        }
      }
    }

    // All retries exhausted
    this.#logger.error(`All delete attempts failed for block ${blockId}`, lastError);
    throw lastError;
  }

  /**
   * Callback after successful deletion (override in subclass or via options).
   * @param {string} blockId - The deleted block's ID.
   * @returns {void}
   */
  #onDeleteSuccess(blockId) {
    // Example: remove the block's DOM element
    const element = document.querySelector(`[data-block-id="${CSS.escape(blockId)}"]`);
    if (element) {
      element.remove();
    }
    this.#configCache.delete(blockId);
    this.#logger.debug(`Removed block element and cache entry for ${blockId}`);
  }

  /**
   * Clear all internal caches and detach all listeners.
   * Useful for cleanup during unmount.
   * @returns {void}
   */
  destroy() {
    this.#configCache.clear();
    // Detach all handlers (iterate over a snapshot of keys)
    for (const el of this.#listenerMap.keys()) {
      this.detachDeleteHandlers(el);
    }
    this.#logger.info('CampaignBlockManager destroyed');
  }
}

// ---------------------------------------------------------------------------
// Export
// ---------------------------------------------------------------------------

export { CampaignBlockManager, ValidationError, NetworkError, SecurityError, ConsoleLogger, Logger };
export default CampaignBlockManager;