# Architecture

## Goal

Receive event-level experiment data, store it in SQL, aggregate the data, and recommend the traffic split for the next day.

## Flow

1. The API receives an event.
2. The payload is validated.
3. The raw event is stored in the database.
4. The daily aggregate is updated.
5. The recommendation query reads recent history.
6. Thompson Sampling estimates each variant win probability.
7. The API returns the recommended allocation.

## Algorithm choice

Thompson Sampling was selected because:

- it balances exploration and exploitation well;
- it works naturally for CTR;
- it scales to multiple variants;
- it is easy to explain in interviews.

