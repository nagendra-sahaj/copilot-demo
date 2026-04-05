# How to submit a new issue in UAT

## Overview
The Unified Action Tracker (UAT) is the central system for logging and managing client issues. Any issue raised by a client — whether reported by phone, email, or directly — should be logged in UAT as soon as it is identified. This ensures full traceability, correct ownership, and timely resolution.

## Who should submit issues
- Support leads handling inbound client calls or emails
- Clients who have direct access to the UAT portal
- Account managers escalating issues on behalf of clients

## Step-by-step instructions

### Step 1 — Log in to UAT
Navigate to the UAT portal and sign in with your enterprise credentials. If you do not have access, contact your system administrator.

### Step 2 — Click "New Issue"
From the UAT dashboard, click the **New Issue** button in the top right corner. This opens the issue creation form.

### Step 3 — Fill in the issue title
Enter a concise, descriptive title for the issue. The title should clearly describe the problem without jargon. Examples:
- "Network connectivity failure affecting API calls — Contoso"
- "Billing invoice incorrect for March 2025 — Fabrikam"
- "Authentication timeout on login — Northwind"

### Step 4 — Select the client
From the dropdown, select the client associated with this issue. If the client is not listed, contact your administrator to have them added to the system.

### Step 5 — Select the category
Choose the most appropriate category from the following options:
- **Performance** — slow response times, latency, throughput issues
- **Security** — authentication failures, access control issues, vulnerabilities
- **Billing** — incorrect invoices, payment failures, subscription issues
- **Integration** — API failures, webhook issues, third-party connector problems
- **Compliance** — regulatory, audit, or data residency concerns
- **Feature Gap** — missing functionality that the client requires
- **Data Loss** — data corruption, missing records, sync failures

### Step 6 — Set the severity
Select the severity level based on the business impact:
- **Critical** — service is completely down or data loss is occurring. Client cannot operate.
- **High** — significant degradation affecting core operations. Workaround is difficult.
- **Medium** — partial degradation. Workaround exists but is inconvenient.
- **Low** — minor issue with minimal business impact. Cosmetic or edge case.

### Step 7 — Write the issue description
In the Description field, provide a detailed account of the issue. Include:
- What the client was trying to do
- What happened instead
- Any error messages or codes observed
- Steps to reproduce the issue
- How long the issue has been occurring
- Number of users affected

### Step 8 — Add business impact
In the Business Impact field, describe what the client stands to lose if this issue is not resolved. Be specific:
- How many users are affected?
- Which business processes are blocked?
- Is there a deadline or SLA at risk?

### Step 9 — Enter revenue impact
Enter the estimated revenue at risk in USD if this issue is not resolved. This figure is used by Sales and Marketing to prioritise issues. If unknown, enter 0 and update later.

### Step 10 — Assign the issue
Assign the issue to the appropriate support lead. If you are the submitting support lead, you may assign it to yourself.

### Step 11 — Submit the issue
Click **Submit**. The issue will be assigned a unique Issue ID and will appear in the UAT dashboard.

## After submission
- The assigned support lead will receive an email notification.
- The client will receive a confirmation email with the Issue ID.
- The issue status will be set to **Open** automatically.
- Sales and Marketing leads will be notified if the revenue impact exceeds $100,000.

## Tips
- Always fill in the description thoroughly — vague descriptions slow down resolution.
- If the client reports multiple unrelated issues in one call, create separate UAT entries for each.
- Use the Issue ID in all follow-up communications with the client.
