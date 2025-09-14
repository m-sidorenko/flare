# 🎇 Flare — Real-time alert relay from Logfire to Telegram chats, groups, and channels.

### SQL queries for Logfire Alert
```sql
SELECT
  service_name,
  message,
  level
FROM records
WHERE level > 'notice'
```

### Webhooks endpoints
It's necessary to set up two webhooks. The first one is for Logfire to send alerts, and the second one is for Telegram to send updates:
1. https://your_domain.com/alert
2. https://your_domain.com/tg_webhook