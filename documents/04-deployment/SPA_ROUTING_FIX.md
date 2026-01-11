# Fix for "Not Found" Error on Refresh (SPA Routing)

## Problem

When you refresh the dashboard (or any route) in the browser, you get a "Not Found" error.

This happens because:
- React Router handles routing on the client-side
- When you refresh `/dashboard`, the browser requests that path from the server
- The server doesn't have a `/dashboard` route, so it returns 404
- The server should instead return `index.html` so React Router can handle it

## Solution

### For Development (Vite Dev Server)

Vite's dev server already handles this automatically. If you're seeing the error in development:

1. **Make sure you're accessing via the Vite dev server**:
   - Use: `http://localhost:5173/dashboard` (NOT a direct file path)
   - The dev server should handle routing automatically

2. **If still not working**, check `vite.config.ts` - it should already handle SPA routing

### For Production (Static Site Deployment)

For production deployments (Render, Vercel, Netlify), you need to configure the server to serve `index.html` for all routes.

#### Option 1: Render.com Static Site (Recommended)

Render automatically handles SPA routing for static sites. Just ensure:
- **Publish Directory**: `dist`
- **Build Command**: `npm run build`

Render will automatically serve `index.html` for all routes.

#### Option 2: Netlify (if using Netlify)

Create `public/_redirects` file (already created):
```
/*    /index.html   200
```

#### Option 3: Vercel (if using Vercel)

Vercel automatically handles SPA routing for React apps. No configuration needed.

#### Option 4: Manual Server Configuration

If using a custom server, configure it to:
1. Serve static files from `dist/`
2. For any route that doesn't match a file, serve `dist/index.html`

**Example for Nginx**:
```nginx
location / {
  try_files $uri $uri/ /index.html;
}
```

**Example for Apache**:
```apache
<IfModule mod_rewrite.c>
  RewriteEngine On
  RewriteBase /
  RewriteRule ^index\.html$ - [L]
  RewriteCond %{REQUEST_FILENAME} !-f
  RewriteCond %{REQUEST_FILENAME} !-d
  RewriteRule . /index.html [L]
</IfModule>
```

## Quick Test

1. **Development**: 
   - Start dev server: `npm run dev`
   - Navigate to: `http://localhost:5173/dashboard`
   - Refresh the page - should work ✅

2. **Production**:
   - Build: `npm run build`
   - Deploy to Render/Vercel
   - Navigate to your deployed URL
   - Refresh any route - should work ✅

## Common Issues

### Issue: Still seeing 404 after deployment

**Solution**: 
- Check that you're deploying as a "Static Site" (not "Web Service")
- Verify "Publish Directory" is set to `dist`
- For Render, static sites automatically handle SPA routing
- For Vercel, it's automatic for React apps

### Issue: Routes work but refresh doesn't

**Solution**: This is the exact problem this fix addresses. Ensure:
- `_redirects` file exists in `public/` (for Netlify)
- Server is configured to serve `index.html` for all routes
- Using a platform that supports SPA routing (Render, Vercel)

---

**Status**: Fixed - `_redirects` file added for Netlify compatibility
