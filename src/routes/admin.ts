```typescript
import { Router, Request, Response } from 'express';
import { authenticate, requireAdmin } from '../middleware/auth';
import { getMetrics } from '../services/metrics';

const router = Router();

/**
 * GET /api/admin/metrics
 * Requires both authentication AND admin role authorization.
 */
router.get('/metrics', authenticate, requireAdmin, async (req: Request, res: Response) => {
  try {
    const metrics = await getMetrics();
    res.json(metrics);
  } catch (error) {
    const err = error as Error;
    res.status(500).json({ error: err.message });
  }
});

export default router;
