# How to escalate a critical issue in UAT

## Overview
Escalation is the process of raising the priority of an issue so that it receives immediate attention from senior support staff, engineering teams, or leadership. Not all issues require escalation — reserve it for situations where the standard support process is insufficient given the business impact.

## When to escalate
Escalate an issue when one or more of the following conditions are met:
- The issue is **Critical** severity and has been open for more than 2 hours without progress
- The client is at risk of **SLA breach**
- The issue is affecting **multiple clients simultaneously**
- There is confirmed or suspected **data loss**
- The client has **executive involvement** and is requesting urgent resolution
- The revenue impact exceeds **$500,000**
- The issue has been **re-opened** more than twice without lasting resolution

## Step-by-step instructions

### Step 1 — Open the issue in UAT
Navigate to the issue you want to escalate. Use the search bar or filter by Issue ID.

### Step 2 — Change severity to Critical
If the issue is not already marked Critical, update the severity field to **Critical**. Add a note in the comments explaining why the severity has been increased.

### Step 3 — Update the business impact description
Ensure the Business Impact field is fully up to date. Include:
- Current number of users affected
- Business processes that are blocked
- Any SLA deadlines that are at risk
- Client's own escalation from their side (e.g. their CTO is involved)

### Step 4 — Update the revenue impact figure
Ensure the revenue impact figure reflects the current situation. Escalations with quantified revenue impact receive faster attention from senior stakeholders.

### Step 5 — Click "Escalate"
Click the **Escalate** button on the issue detail page. This triggers the following automatically:
- The issue is flagged with an escalation badge in the UAT dashboard
- The assigned support lead's manager is notified by email
- The engineering on-call team receives a Slack notification
- The Sales lead for the client account is notified

### Step 6 — Assign to a senior support lead
Reassign the issue to a senior support lead if the current assignee does not have the authority or access to resolve it. Use the **Reassign** button and select from the senior support lead list.

### Step 7 — Set the escalation reason
From the Escalation Reason dropdown, select the most appropriate reason:
- SLA at risk
- Data loss confirmed
- Multi-client impact
- Executive involvement
- Revenue threshold exceeded
- Repeat issue

### Step 8 — Add a comment
Add a detailed comment to the issue timeline explaining:
- Why you are escalating
- What has been tried so far
- What you need from the escalation (engineering involvement, leadership decision, etc.)

### Step 9 — Notify the client
Contact the client directly to let them know the issue has been escalated. Provide:
- The name of the senior support lead now handling the issue
- An estimated time for the next update
- Do not promise a resolution time unless you have confirmed it with engineering

## After escalation
- Escalated issues appear at the top of the UAT dashboard with a red escalation flag.
- Senior support leads are expected to provide an update within 1 hour of assignment.
- Engineering leads are notified automatically for Critical escalations.
- Directors and VPs can view all escalated issues in the executive dashboard.

## Removing an escalation
Once the issue is resolved or stabilised, click **Remove Escalation** on the issue detail page. Add a comment explaining why the escalation has been removed.

## Tips
- Do not escalate every Critical issue — escalation is for situations where normal processes are insufficient.
- Keep the client informed throughout. Regular updates prevent unnecessary re-escalations.
- If in doubt about whether to escalate, speak to your team lead before doing so.
