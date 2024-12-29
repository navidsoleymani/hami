# Code Challenge: Social Network Engagement Bot

## Objective

Develop a Python-based Telegram bot with a simple RESTful API that tracks and provides engagement insights for social media accounts (e.g., Twitter or Instagram) based on user activity.
This bot allows users to monitor follower count changes and set alerts for specific engagement milestones.

## Key Functionalities

Telegram Bot Interface

* Users can interact with the bot to:
  * Add a social media profile to monitor (for example, Twitter or Instagram handles).
  * Set an engagement milestone alert (e.g., "Alert me when followers reach 1,000").
  * Check current follower count.

## API for Profile and Follower Data

Implement a RESTful API with endpoints to:

* Register or update a social media profile to monitor.
* Set or retrieve alert settings.
* Fetch the latest follower count and engagement insights.
* Use basic authentication to secure the API.

## Follower Count Monitoring and Milestone Alert

Use a mock or real social media API (such as a sample JSON endpoint) to fetch profile follower counts.

Implement a background task (e.g., using asyncio or a simple cron job) to periodically check the follower count.

If a milestone is reached (e.g., crossing the 1,000-follower threshold), send a notification to the user via the Telegram bot.

## Database (SQLite or PostgreSQL)
Store monitored profiles, follower count, and milestone alert settings.

Keep it minimal for simplicity.

## Example Workflow
A user starts the Telegram bot and adds a profile to track, setting an alert for when the profile reaches 1,000 followers.

The bot periodically checks the profile's follower count.

When the profile hits 1,000 followers, the bot sends an alert message to the user, celebrating the milestone.

## Requirements for Submission
Code Structure: Organized code with separate modules for bot logic, API, and background tasks.

Testing: Unit tests for adding profiles, setting alerts, and milestone notifications.

Documentation: A README with setup and usage instructions.

## Bonus Requirements
Top Follower Insights: Track the top follower count increases or decreases in the last 24 hours.

Mock Profile Data: Use mock data to simulate follower count changes for testing without real API dependencies.