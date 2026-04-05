# How to close and resolve an issue in UAT

## Overview
Resolving and closing an issue in UAT is not just a housekeeping task — it is an important step that captures resolution knowledge, confirms client satisfaction, and keeps the dashboard accurate for reporting. Always close issues properly rather than leaving them in an open state once resolved.

## Difference between Resolved and Closed
- **Resolved** — the fix or workaround has been applied and the support lead believes the issue is fixed. The client has not yet confirmed.
- **Closed** — the client has confirmed that the issue is resolved to their satisfaction, or the issue has been resolved and the closure period has passed without the client re-opening it.

## Step-by-step instructions

### Step 1 — Confirm the resolution
Before marking an issue as resolved, confirm that:
- The root cause has been identified and addressed
- The fix has been deployed or the workaround has been communicated to the client
- The issue is no longer reproducible

### Step 2 — Add resolution notes
Navigate to the issue and scroll to the **Resolution notes** field. Enter a thorough description of:
- What the root cause was
- What steps were taken to fix it
- Any configuration changes made
- Whether this was a known issue with a standard fix
- Any follow-up actions required

Resolution notes are indexed by the Copilot and used to help support leads resolve similar issues in the future. The more detailed the notes, the more useful they are.

### Step 3 — Set the status to Resolved
Click **Mark as Resolved**. The system will:
- Record the resolved date and time
- Calculate the time-to-resolve for SLA reporting
- Send a confirmation email to the client asking them to verify the resolution

### Step 4 — Notify the client
Contact the client directly to confirm:
- What was done to resolve the issue
- Any actions they need to take on their side
- Who to contact if the issue recurs

### Step 5 — Wait for client confirmation
Allow the client 48 hours to confirm the resolution. If they confirm, proceed to Step 6. If they report the issue is still occurring, reopen it and continue the resolution process.

### Step 6 — Close the issue
Once the client confirms resolution — or after 48 hours without a response — click **Close Issue**. The status changes to **Closed** and the issue is removed from the active dashboard.

### Step 7 — Update revenue impact
If the resolved issue had a revenue impact recorded, update the field to reflect the actual impact that was avoided. This is used in QBR reporting.

## Auto-closure policy
Issues that have been in **Resolved** status for more than 7 days without client response are automatically closed by the system. A notification is sent to the client before auto-closure.

## Reopening a closed issue
If a client reports the same issue after closure, click **Reopen Issue** on the closed issue record. Add a comment explaining why it is being reopened. Do not create a new issue for the same problem — reopening preserves the history.

## Tips
- Never close an issue without resolution notes — future support leads depend on this knowledge.
- If the issue was resolved by a product fix rather than a workaround, note the fix version number.
- Issues closed without client confirmation should be flagged in the comment: "Auto-closed — client did not respond within 48 hours."
