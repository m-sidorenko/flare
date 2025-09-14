# flare
🎇 Flare — Real-time alert relay from Logfire to Telegram chats, groups, and channels.


## SQL queries for Logfire Alert
```sql
SELECT
  service_name,
  message,
  level
FROM records
WHERE level > 'notice'
```

