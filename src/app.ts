```typescript
import express from 'express';
import adminRoutes from './routes/admin';

const app = express();

app.use(express.json());

// Health check
app.get('/health', (_req, res) => {
  res.json({ status: 'ok' });
});

// Admin routes — all endpoints protected by authenticate + requireAdmin
app.use('/api/admin', adminRoutes);

export default app;
