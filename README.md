# Gitbot

## Description

This project checks if a specified user has made any commits to their GitHub repositories on a daily basis. If no commits are found for the day, the application sends an email notification using SendGrid.

## Features

- Lists all repositories of a specified GitHub user.
- Checks for commits made today in any of the user's repositories.
- Sends an email notification if no commits were made today.
- Scheduled to run automatically every day at 19:00 UTC using GitHub Actions.

## Technologies Used

- Python
- GitHub API
- SendGrid API
- GitHub Actions for scheduling

## Prerequisites

- A GitHub account
- A SendGrid account
- Python 3.10.12 installed locally (for development)