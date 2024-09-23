# Community Music Pattern Creator API Documentation

## Overview

This document provides details on how to integrate with the Community Music Pattern Creator API. The API allows developers to interact with music patterns, user profiles, and other features of the platform.

## Base URL

All API requests should be made to:

```
https://api.communitypatterns.synthsouls.com/v1
```

## Authentication

API requests require authentication using a bearer token. Include the token in the Authorization header of your requests:

```
Authorization: Bearer YOUR_API_TOKEN
```

## Endpoints

### Patterns

#### Get All Patterns

Retrieves a list of all available patterns.

- **URL:** `/patterns`
- **Method:** GET
- **Parameters:**
  - `page` (optional): Page number for pagination
  - `limit` (optional): Number of patterns per page (default: 20)
- **Response:**
  ```json
  {
    "patterns": [
      {
        "id": "pattern_id",
        "name": "Pattern Name",
        "creator": "Creator Username",
        "created_at": "2023-09-23T12:00:00Z",
        "genre": "Electronic",
        "rating": 4.5
      },
      ...
    ],
    "total": 100,
    "page": 1,
    "limit": 20
  }
  ```

#### Create a Pattern

Creates a new pattern.

- **URL:** `/patterns`
- **Method:** POST
- **Body:**
  ```json
  {
    "name": "New Pattern",
    "genre": "Electronic",
    "data": {
      // Pattern data structure
    }
  }
  ```
- **Response:**
  ```json
  {
    "id": "new_pattern_id",
    "name": "New Pattern",
    "creator": "Your Username",
    "created_at": "2023-09-23T12:30:00Z",
    "genre": "Electronic",
    "rating": null
  }
  ```

#### Get a Specific Pattern

Retrieves details of a specific pattern.

- **URL:** `/patterns/{pattern_id}`
- **Method:** GET
- **Response:**
  ```json
  {
    "id": "pattern_id",
    "name": "Pattern Name",
    "creator": "Creator Username",
    "created_at": "2023-09-23T12:00:00Z",
    "genre": "Electronic",
    "rating": 4.5,
    "data": {
      // Pattern data structure
    }
  }
  ```

#### Update a Pattern

Updates an existing pattern.

- **URL:** `/patterns/{pattern_id}`
- **Method:** PUT
- **Body:**
  ```json
  {
    "name": "Updated Pattern Name",
    "genre": "Jazz",
    "data": {
      // Updated pattern data structure
    }
  }
  ```
- **Response:**
  ```json
  {
    "id": "pattern_id",
    "name": "Updated Pattern Name",
    "creator": "Creator Username",
    "updated_at": "2023-09-23T13:00:00Z",
    "genre": "Jazz",
    "rating": 4.5
  }
  ```

#### Delete a Pattern

Deletes a specific pattern.

- **URL:** `/patterns/{pattern_id}`
- **Method:** DELETE
- **Response:** HTTP 204 No Content

### User Profiles

#### Get User Profile

Retrieves the profile of the authenticated user.

- **URL:** `/users/me`
- **Method:** GET
- **Response:**
  ```json
  {
    "id": "user_id",
    "username": "Your Username",
    "email": "your.email@example.com",
    "created_at": "2023-09-01T10:00:00Z",
    "patterns_created": 10,
    "patterns_used": 25
  }
  ```

#### Update User Profile

Updates the profile of the authenticated user.

- **URL:** `/users/me`
- **Method:** PUT
- **Body:**
  ```json
  {
    "username": "New Username",
    "email": "new.email@example.com"
  }
  ```
- **Response:**
  ```json
  {
    "id": "user_id",
    "username": "New Username",
    "email": "new.email@example.com",
    "updated_at": "2023-09-23T14:00:00Z"
  }
  ```

## Error Handling

The API uses standard HTTP status codes to indicate the success or failure of requests. In case of an error, the response will include a JSON object with an `error` field providing more details about the error.

Example error response:

```json
{
  "error": {
    "code": "invalid_request",
    "message": "The request was invalid or cannot be served."
  }
}
```

## Rate Limiting

The API implements rate limiting to ensure fair usage. The current limits are:

- 1000 requests per hour per API token

If you exceed the rate limit, you'll receive a 429 Too Many Requests response.

## Changelog

- **2023-09-23**: Initial API documentation release.

For any questions or support, please contact our developer support team at dev-support@synthsouls.com.
