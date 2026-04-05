# How to review and prioritise feedback for engineering in FB360

## Overview
Periodically, product managers, engineering leaders, and release managers review FB360 to identify feedback that should be converted into actionable feature development. This guide explains how to conduct that review and how to signal priority to the engineering team.

## Who conducts the review
- **Product managers** — weekly review of new feedback
- **Engineering leaders** — monthly review of aggregated signals
- **Release managers** — quarterly review ahead of roadmap planning
- **Market researchers** — ongoing review to identify emerging themes

## Step-by-step instructions

### Step 1 — Access the prioritisation view
From the FB360 dashboard, click **Prioritisation** in the left navigation. This view shows feature requests sorted by their aggregated priority signal — a combination of:
- Total number of feedback entries linked
- Total revenue opportunity across all linked feedback
- Recency of feedback (recent feedback is weighted higher)
- Client tier (Platinum and Gold clients are weighted higher)

### Step 2 — Review the top feature requests
For each top-ranked feature request, review:
- The feature title and description
- The number of clients who have requested it
- The total revenue opportunity
- A sample of the linked feedback descriptions

Click **View linked feedback** to read the individual feedback entries.

### Step 3 — Assess feasibility
Before flagging a feature for engineering, assess:
- Is the feature technically feasible with the current architecture?
- What is the estimated complexity (Low / Medium / High / Very High)?
- Are there dependencies on other features or infrastructure?

If you are not technical, involve an engineering lead in this step.

### Step 4 — Set the priority score
On the feature request record, click **Set priority score**. Enter a score from 0.0 to 10.0. Use this rubric as a guide:
- **9.0 — 10.0** — critical feature with immediate high-revenue demand and low complexity
- **7.0 — 8.9** — high-demand feature with strong revenue signal
- **5.0 — 6.9** — moderate demand, worth scheduling in the next 2 quarters
- **3.0 — 4.9** — low demand or high complexity, schedule for later
- **0.0 — 2.9** — low priority, monitor for signal changes

### Step 5 — Update the feature status
Change the feature status as appropriate:
- **Backlog** → **Planned** if the feature has been approved for development
- **Planned** → **In Development** once engineering begins work
- Add a comment explaining the status change and who approved it

### Step 6 — Assign a target quarter
For features moving to Planned or In Development, assign a **Target quarter** (e.g. Q3 2025). This is used by the release manager to build the public roadmap.

### Step 7 — Notify the requesting clients
Once a feature moves to **Planned**, FB360 can automatically notify the clients who requested it. Click **Notify requesting clients** on the feature record. The notification includes:
- Confirmation that their feedback has been heard
- The target quarter for delivery
- A brief description of what will be built

## Prioritisation best practices
- Never prioritise based on a single client's request, no matter how loud they are. Look for aggregate signal.
- A feature with $10M revenue opportunity from 5 clients outweighs a feature with $15M from 1 client — diversity of demand signals stronger product-market fit.
- Revisit priority scores quarterly — market conditions and client needs change.
- Features that remain in Backlog for more than 12 months should be reviewed and either prioritised, deprioritised, or archived.

## Tips
- Use the **Compare features** view to evaluate two features side by side before deciding which to prioritise.
- Always document your reasoning when setting a priority score — future reviewers need to understand the decision.
- Coordinate with the release manager before setting target quarters — they have visibility of engineering capacity.
