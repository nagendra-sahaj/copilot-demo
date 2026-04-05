# How to link an issue to a feature request in UAT

## Overview
Some client issues arise not because something is broken, but because a capability does not yet exist in the product. In these cases, the issue should be linked to a feature request so that the engineering and product teams can understand the business context driving the feature. This linkage is critical for accurate prioritisation.

## When to link an issue to a feature request
- The client's issue cannot be resolved with the current product capabilities
- The resolution requires a new feature, enhancement, or configuration option
- The same issue has been raised by multiple clients and points to a product gap
- A workaround exists but the client considers it unacceptable long-term

## Step-by-step instructions

### Step 1 — Open the issue in UAT
Navigate to the issue you want to link. Use the search bar or filter by Issue ID, client name, or category.

### Step 2 — Scroll to the "Linked items" section
On the issue detail page, scroll down to the **Linked items** panel. This section shows all existing links — other issues, feature requests, or feedback records.

### Step 3 — Click "Link feature request"
Click the **Link feature request** button. A search dialog will appear.

### Step 4 — Search for an existing feature request
Type keywords related to the feature in the search box. The system will search across all feature titles and descriptions in UAT. If a matching feature request already exists:
- Review the feature description to confirm it matches the client's need
- Click **Link** to create the association

### Step 5 — Create a new feature request if none exists
If no matching feature request is found, click **Create new feature request**. Fill in:
- **Title** — a clear, product-focused description of the capability needed
- **Category** — AI/ML, Security, Performance, Integration, Analytics, Compliance, Developer Experience
- **Description** — what the feature should do, from the client's perspective
- **Complexity** — your estimate: Low, Medium, High, Very High
- The new feature will be created in Backlog status and linked automatically

### Step 6 — Add context to the link
After linking, add a comment to the issue explaining:
- Why this issue requires a new feature rather than a bug fix
- How the client is currently working around the limitation
- Whether this is blocking the client or merely inconvenient

### Step 7 — Update the issue status
If the issue cannot be resolved until the feature is built, update the status to **In Progress** and add a note that resolution is dependent on the linked feature request.

### Step 8 — Notify the client
Inform the client that their issue has been linked to a feature request. Explain:
- The feature is being reviewed by the product team
- They will be notified when the feature is prioritised and when it is released
- In the meantime, describe any available workaround

## How linked items affect prioritisation
When an issue is linked to a feature request, the revenue impact from the issue is automatically added to the feature's total revenue signal. This means:
- Features linked to many high-revenue issues rise in priority automatically
- Engineering leaders can see the business case for a feature directly in UAT
- Release managers use these signals when building the product roadmap

## Tips
- Always search for an existing feature request before creating a new one — duplicates dilute the revenue signal.
- The strength of the link depends on the quality of the business impact description. Be specific.
- If multiple clients raise the same issue, link all of them to the same feature request — the aggregated signal is more powerful than individual entries.
