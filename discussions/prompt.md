Based on the existing content, the new request, and the additional context provided, I've generated an improved prompt that incorporates the requirements for sending messages on both Discord and Telegram using terminal commands. Here's the updated prompt:

# Prompt: Implement Discord and Telegram Messaging via Terminal Commands for AI-Driven Human Rights Advocacy

## Introduction and Context
As part of an AI-driven human rights advocacy project, we need to implement messaging capabilities for both Discord and Telegram, accessible through terminal commands. This feature will enable efficient distribution of human rights information, increase engagement with community members, and provide real-time responses to user queries across both platforms. The integration of these messaging systems is crucial for expanding the reach of human rights advocacy and creating vibrant online communities focused on human rights.

## Main Objective
Develop and implement robust command-line interfaces (CLIs) for both Discord and Telegram that can send messages, interact with users, and integrate with our existing Global Human Rights Observer (GHRO) system for content generation. The CLIs should be capable of distributing advocacy messages, responding to commands, and adhering to best practices for both Discord and Telegram bot development.

## Step-by-Step Instructions

### 1. Set Up Discord and Telegram Bots
1.1. Create a new Discord application and bot in the Discord Developer Portal.
1.2. Create a new Telegram bot using BotFather.
1.3. Obtain the bot tokens for both platforms and add them to your environment variables.
1.4. Invite the Discord bot to your server and set up the Telegram bot in relevant groups.

### 2. Develop Unified CLI Framework
2.1. Set up a new Python project and install required libraries (discord.py, python-telegram-bot, click for CLI).
2.2. Create a main CLI script:
   - Import necessary libraries
   - Load environment variables
   - Set up click commands for the root CLI
2.3. Implement authentication and connection management for both platforms.
2.4. Create a unified command structure that works for both Discord and Telegram.

### 3. Implement Message Sending Functionality
3.1. Develop commands for composing and sending messages:
   - Create a 'send' command with platform, target, and message content arguments
   - Implement platform-specific formatting options (e.g., Discord markdown, Telegram HTML)
   - Add support for file attachments
3.2. Implement targeting functionality:
   - Allow targeting by channel/chat ID or name
   - Enable user targeting by ID or username
   - Support bulk messaging through input files

### 4. Develop Scheduling and Queueing System
4.1. Implement message scheduling:
   - Create commands to schedule messages for future delivery
   - Develop a persistent storage system for scheduled messages
4.2. Create a queue management system:
   - Implement commands to view, edit, and delete queued messages
   - Develop a background worker to process the message queue

### 5. Implement Error Handling and Monitoring
5.1. Develop a comprehensive error handling system:
   - Implement try-except blocks for all API calls
   - Create a logging system for errors and important events
5.2. Implement a monitoring system:
   - Create commands to check the status of bot connections
   - Develop real-time alerts for critical failures

### 6. Develop Analytics and Reporting Features
6.1. Implement message tracking:
   - Create a database to store message delivery status and engagement metrics
   - Develop commands to retrieve analytics data
6.2. Create reporting functionality:
   - Implement commands to generate engagement reports
   - Develop A/B testing capabilities accessible via CLI

### 7. Integrate with GHRO for Content Generation
7.1. Implement API calls or database queries to retrieve human rights information from GHRO.
7.2. Create functions to format GHRO data for both Discord and Telegram messages.
7.3. Develop commands to generate and send advocacy messages using GHRO data.

### 8. Implement Advanced Features
8.1. Develop interactive commands for user queries:
   - Create command to set up auto-responses for specific keywords
   - Implement a basic NLP system to understand and categorize user queries
8.2. Implement multi-language support:
   - Develop a translation system for messages
   - Create commands to manage and switch between languages

### 9. Testing and Deployment
9.1. Conduct thorough testing:
   - Develop an automated testing suite for all CLI commands
   - Perform load testing to ensure stability
9.2. Deploy the CLI tool:
   - Set up a distribution system (e.g., PyPI)
   - Create installation and update scripts

## Guidelines for Verification and Validation
- Ensure the CLI successfully connects to both Discord and Telegram when provided with correct credentials.
- Verify that messages can be sent to both platforms using the same command structure.
- Test all CLI commands to ensure they provide the expected responses and actions.
- Check that the scheduling and queueing system works correctly across both platforms.
- Verify that the error handling and monitoring systems provide accurate and timely information.
- Test the analytics and reporting features to ensure they capture data from both platforms accurately.
- Ensure that the GHRO integration works correctly and provides up-to-date information.
- Verify that the multi-language support functions as expected.
- Test the CLI's performance under high load to ensure stability.

## Presentation Format of the Final Result
Present your solution as a well-structured Python project, including:
1. Main CLI script (cli.py)
2. Module for Discord integration (discord_integration.py)
3. Module for Telegram integration (telegram_integration.py)
4. Module for message handling (message_handler.py)
5. Module for scheduling and queueing (scheduler.py)
6. Module for error handling and monitoring (error_handler.py)
7. Module for analytics and reporting (analytics.py)
8. Module for GHRO integration (ghro_integration.py)
9. Configuration file (config.py) for bot settings and constants
10. Requirements file (requirements.txt) listing all necessary dependencies

Include a README.md file with:
- Project overview
- Installation instructions
- List of available CLI commands with examples
- Guidelines for contributors

Provide comprehensive documentation for each module, including function descriptions and usage examples. Use comments throughout the code to explain complex logic or important considerations. Adhere to PEP 8 style guidelines and follow best practices for both Discord and Telegram bot development.

Develop a user manual detailing the CLI usage, including:
- Getting started guide
- Detailed command reference
- Best practices for effective use
- Troubleshooting section

Create a quick reference card summarizing the most common commands and their syntax for easy reference by operators.