# How to search for similar issues in UAT

## Overview
Before spending time investigating a new issue, always search UAT for similar issues that have been reported and resolved previously. Finding a similar resolved issue can dramatically reduce resolution time — the root cause and fix may already be documented.

## Step-by-step instructions

### Step 1 — Use the search bar
On the UAT dashboard, click the search bar at the top of the page. You can search by:
- Keywords from the issue title or description
- Issue ID (for direct lookup)
- Client name
- Error message or error code

### Step 2 — Apply filters to narrow results
After entering a search term, use the filter panel on the left to narrow results:
- **Status** — filter by Open, In Progress, Resolved, or Closed
- **Category** — narrow to a specific issue type
- **Severity** — filter by Critical, High, Medium, or Low
- **Date range** — limit to issues created within a specific period
- **Client** — filter to a specific client or exclude your current client

### Step 3 — Sort results by relevance
By default, results are sorted by creation date. Change the sort order to **Relevance** to surface the most semantically similar issues first.

### Step 4 — Review similar issues
For each result, review:
- The issue title and description
- The resolution notes (for resolved/closed issues)
- The category and severity
- The client — similar clients in the same industry often face the same issues

### Step 5 — Use the Copilot for intelligent search
For a more powerful search experience, use the **Copilot** search bar. Instead of keywords, describe the issue in natural language:
- "Find issues where API calls are timing out for banking clients"
- "Show me resolved Critical security issues from the last 6 months"
- "What issues are similar to authentication failures on login?"

The Copilot uses semantic search to find issues that are conceptually similar, even if they use different terminology.

### Step 6 — Link related issues
If you find issues that are related to yours, link them using the **Link related issue** button on the issue detail page. This builds a knowledge graph of related problems and solutions.

## Search tips
- Search for the **error message** or **error code** exactly — these are often indexed verbatim
- If a keyword search returns too many results, add the **client industry** as a filter — similar industries often have the same issues
- Resolved issues with detailed resolution notes are the most valuable — prioritise reviewing these
- If you find a match, read the resolution notes carefully — the fix may not apply directly to your situation

## When not to use search
- For brand new issues with no precedent, search will return low-quality results. Move quickly to investigation.
- Do not spend more than 10 minutes searching before starting your own investigation.
