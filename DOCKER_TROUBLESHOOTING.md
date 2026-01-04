# Docker Troubleshooting Guide

## Common Docker Errors and Solutions

### Error: "Cannot connect to the Docker daemon"

**Problem:** Docker daemon is not running.

**Solution:**
1. **On macOS/Windows:** Start Docker Desktop application
   - Open Docker Desktop from Applications
   - Wait for it to fully start (whale icon in menu bar should be steady)
   - Verify it's running: `docker ps`

2. **On Linux:**
   ```bash
   sudo systemctl start docker
   sudo systemctl enable docker  # To start on boot
   ```

3. **Verify Docker is running:**
   ```bash
   docker ps
   ```
   Should return a list of containers (or empty if none running), not an error.

### Error: "version is obsolete" Warning

**Problem:** Docker Compose v2 doesn't require the `version` field.

**Solution:** ✅ Already fixed! The `version: '3.8'` line has been removed from `docker-compose.yml`.

### Error: Port Already in Use

**Problem:** Port 8000 or 3000 is already in use.

**Solution:**
1. **Find what's using the port:**
   ```bash
   # macOS/Linux
   lsof -i :8000
   lsof -i :3000
   
   # Or use
   netstat -an | grep 8000
   ```

2. **Stop the process or change ports in docker-compose.yml:**
   ```yaml
   ports:
     - "8001:8000"  # Change host port
   ```

### Error: Build Fails

**Problem:** Docker build is failing.

**Solutions:**
1. **Clear Docker cache:**
   ```bash
   docker system prune -a
   ```

2. **Rebuild without cache:**
   ```bash
   docker-compose build --no-cache
   ```

3. **Check disk space:**
   ```bash
   docker system df
   ```

### Error: ChromeDriver Installation Fails

**Problem:** ChromeDriver download fails during build.

**Solution:**
1. **Check internet connection** - ChromeDriver is downloaded during build
2. **Try building again** - Sometimes network issues cause temporary failures
3. **Check Dockerfile** - Ensure ChromeDriver installation section is correct

### Error: Container Exits Immediately

**Problem:** Container starts then stops.

**Solution:**
1. **Check logs:**
   ```bash
   docker-compose logs backend
   docker-compose logs frontend
   ```

2. **Run container interactively:**
   ```bash
   docker-compose run --rm backend /bin/bash
   ```

### Error: Frontend Can't Connect to Backend

**Problem:** Frontend shows "Backend Disconnected".

**Solution:**
1. **Verify both containers are running:**
   ```bash
   docker-compose ps
   ```

2. **Check backend is accessible:**
   ```bash
   curl http://localhost:8000/health
   ```

3. **Check network:**
   ```bash
   docker network ls
   docker network inspect linkedinscraper_scraper-network
   ```

## Quick Diagnostic Commands

```bash
# Check Docker is running
docker ps

# Check Docker Compose version
docker-compose --version

# View all containers (including stopped)
docker ps -a

# View logs
docker-compose logs -f

# Restart services
docker-compose restart

# Stop and remove everything
docker-compose down

# Stop, remove, and rebuild
docker-compose down
docker-compose up --build
```

## Still Having Issues?

1. **Update Docker Desktop** to the latest version
2. **Check Docker Desktop resources** - Ensure enough memory/CPU allocated
3. **Restart Docker Desktop** completely
4. **Check system requirements** - Ensure your system meets Docker requirements

