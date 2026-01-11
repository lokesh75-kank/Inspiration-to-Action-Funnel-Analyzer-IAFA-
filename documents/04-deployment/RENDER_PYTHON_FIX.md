# Fix for Render.com Python 3.13 Build Error

## Problem
Render is using Python 3.13.4 by default, which causes `pydantic-core` to try compiling from source using Rust, leading to filesystem permission errors.

## Solutions

### Solution 1: Use runtime.txt (Already Added)
The `backend/runtime.txt` file specifies Python 3.11.0:
```
python-3.11.0
```

**If this doesn't work**, Render might not be detecting it. Try:

1. **Manually set Python version in Render UI**:
   - Go to your service in Render dashboard
   - Click "Settings" → "Advanced"
   - Set "Python Version" to `3.11.0` or `3.12.0`
   - Save and redeploy

2. **Ensure runtime.txt is in the correct location**:
   - File should be at: `backend/runtime.txt` (in the Root Directory)
   - Render looks for `runtime.txt` in the Root Directory you specified
   - Since Root Directory is `backend`, the file should be at repo root: `backend/runtime.txt` ✅

### Solution 2: Update Pydantic Version (Alternative)
If Python 3.11 still has issues, update to newer pydantic versions with better wheel support:

Update `backend/requirements.txt`:
```txt
pydantic>=2.10.0  # Newer versions have better wheel support
pydantic-settings>=2.6.0
```

Then commit and push:
```bash
git add backend/requirements.txt
git commit -m "Update pydantic to newer version with better wheel support"
git push
```

### Solution 3: Force Python Version in Render (Recommended)
**Best approach**: Set it manually in Render dashboard:

1. Go to Render dashboard → Your service
2. Click "Settings"
3. Scroll to "Advanced" section
4. Find "Python Version" dropdown
5. Select `3.11.0` or `3.12.0`
6. Click "Save Changes"
7. Trigger a new deployment (or wait for auto-deploy)

This ensures Render uses the correct Python version regardless of runtime.txt.

## Why This Happens
- Python 3.13 is very new (released Oct 2024)
- Many packages don't have pre-built wheels for Python 3.13 yet
- `pydantic-core` needs to compile from source on Python 3.13
- Render's build environment has Rust toolchain permission issues
- Python 3.11/3.12 have excellent pre-built wheel support

## Recommended Action
1. ✅ `runtime.txt` is already added (will work on next deployment)
2. ✅ Update pydantic version (already done in requirements.txt)
3. ⚠️ **Manually set Python version in Render UI** (recommended for immediate fix)
4. Push changes and redeploy

After setting Python version in Render UI, the next deployment should succeed!
