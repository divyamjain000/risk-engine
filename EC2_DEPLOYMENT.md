# EC2 Deployment Guide

## Initial Setup

### 1. Prepare EC2 Instance
```bash
# Install Docker
sudo apt-get update
sudo apt-get install -y docker.io docker-compose-plugin
sudo usermod -aG docker ubuntu
# Log out and back in for group changes to take effect
```

### 2. Transfer Code
```bash
# From your local machine
scp -r /path/to/risk-engine ubuntu@<ec2-ip>:~/
```

### 3. Configure Environment Variables
```bash
# On EC2
cd ~/risk-engine
nano .env
```

Add the following to `.env`:
```env
GROWW_API_KEY=your_actual_api_key
GROWW_API_SECRET=your_actual_api_secret
```

### 4. Start Services
```bash
# Build and start containers
docker compose up -d --build

# Check containers are running
docker compose ps
```

### 5. Run Database Migrations
```bash
# Apply all migrations
docker compose exec api alembic upgrade head

# Verify tables exist
docker compose exec postgres psql -U risk_user -d risk_engine -c "\dt"
```

### 6. Verify Deployment
```bash
# Check API health
curl http://localhost:8000/
# Should return: {"status":"ok"}

# Check logs
docker compose logs -f api

# Manually trigger a job to test
curl -X POST http://localhost:8000/groww/jobs/holdings
```

## Common Issues

### Issue: ProfileNotFound Error
**Symptoms:**
```
botocore.exceptions.ProfileNotFound: The config profile (default) could not be found
```

**Solution:**
Ensure `GROWW_API_KEY` and `GROWW_API_SECRET` are set in `.env`:
```bash
echo "GROWW_API_KEY=your_key" > .env
echo "GROWW_API_SECRET=your_secret" >> .env
docker compose restart api
```

### Issue: UndefinedTable (instruments)
**Symptoms:**
```
psycopg2.errors.UndefinedTable: relation "instruments" does not exist
```

**Solution:**
Run database migrations:
```bash
docker compose exec api alembic upgrade head
```

### Issue: GrowwAPIException
**Symptoms:**
```
growwapi.groww.exceptions.GrowwAPIException: The request to the Groww API failed
```

**Solution:**
Check that your Groww API credentials are correct and active:
```bash
# View current environment variables (credentials will be masked)
docker compose exec api env | grep GROWW

# If empty, recreate .env and restart
docker compose restart api
```

### Issue: Jobs Not Running
**Symptoms:**
No job logs in `docker compose logs api`

**Solution:**
1. Check scheduler is running:
   ```bash
   docker compose logs api | grep -i schedule
   ```

2. Manually trigger a job:
   ```bash
   curl -X POST http://localhost:8000/groww/jobs/holdings
   curl -X POST http://localhost:8000/groww/jobs/instruments
   ```

## Maintenance

### View Logs
```bash
# All API logs
docker compose logs -f api

# Filter for errors
docker compose logs api | grep -i error

# Filter for jobs
docker compose logs api | grep -i job
```

### Restart Services
```bash
# Restart API only
docker compose restart api

# Restart all services
docker compose restart

# Rebuild and restart (after code changes)
docker compose up -d --build
```

### Database Access
```bash
# Connect to PostgreSQL
docker compose exec postgres psql -U risk_user -d risk_engine

# Useful SQL commands:
# \dt                  - List tables
# \d holdings_daily    - Describe table
# SELECT * FROM holdings_daily;
# SELECT * FROM instruments LIMIT 10;
```

### Update Code
```bash
# On local machine, transfer updated code
scp -r /path/to/risk-engine ubuntu@<ec2-ip>:~/

# On EC2, rebuild
cd ~/risk-engine
docker compose down
docker compose up -d --build

# Run any new migrations
docker compose exec api alembic upgrade head
```

## Security Notes

1. **Credentials**: Never commit `.env` file. Use `.env.example` as template.
2. **Firewall**: Configure security group to allow only necessary ports
3. **HTTPS**: Use reverse proxy (nginx) with SSL for production
4. **Secrets**: For production, use AWS Secrets Manager instead of .env files

## Monitoring

### Check Application Health
```bash
# Health check
curl http://localhost:8000/

# API documentation
curl http://localhost:8000/docs

# Test portfolio endpoint
curl http://localhost:8000/groww/portfolio
```

### System Resources
```bash
# Docker container stats
docker stats

# Disk usage
docker system df
```

### Database Stats
```bash
docker compose exec postgres psql -U risk_user -d risk_engine -c "
SELECT 
  schemaname,
  tablename,
  pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables 
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
"
```
