import sys
import random
import uuid
from datetime import date, timedelta
from pathlib import Path

import duckdb
import pandas as pd
from faker import Faker

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from shared.config import DB_PATH

fake = Faker()
Faker.seed(42)
random.seed(42)

# ---------------------------------------------------------------------------
# Client data
# ---------------------------------------------------------------------------

CLIENT_NAMES = [
    "Contoso", "Fabrikam", "Northwind", "AdventureWorks", "Tailwind Traders",
    "Litware", "Proseware", "Woodgrove Bank", "Datum Corporation", "Relecloud",
    "Alpine Ski House", "Bellows College", "City Power and Light",
    "Consolidated Messenger", "Fourth Coffee",
]

INDUSTRIES = {
    "Contoso": "Banking",
    "Fabrikam": "Manufacturing",
    "Northwind": "Retail",
    "AdventureWorks": "Manufacturing",
    "Tailwind Traders": "Retail",
    "Litware": "Healthcare",
    "Proseware": "Telecom",
    "Woodgrove Bank": "Banking",
    "Datum Corporation": "Insurance",
    "Relecloud": "Telecom",
    "Alpine Ski House": "Retail",
    "Bellows College": "Government",
    "City Power and Light": "Government",
    "Consolidated Messenger": "Insurance",
    "Fourth Coffee": "Healthcare",
}

REGIONS = {
    "Contoso": "Americas",
    "Fabrikam": "EMEA",
    "Northwind": "Americas",
    "AdventureWorks": "Americas",
    "Tailwind Traders": "APAC",
    "Litware": "Americas",
    "Proseware": "EMEA",
    "Woodgrove Bank": "EMEA",
    "Datum Corporation": "India",
    "Relecloud": "APAC",
    "Alpine Ski House": "EMEA",
    "Bellows College": "Americas",
    "City Power and Light": "Americas",
    "Consolidated Messenger": "India",
    "Fourth Coffee": "APAC",
}

# Exactly 5 Platinum, 6 Gold, 4 Silver
TIERS = {
    "Contoso": "Platinum",
    "Fabrikam": "Platinum",
    "Woodgrove Bank": "Platinum",
    "Datum Corporation": "Platinum",
    "Relecloud": "Platinum",
    "Northwind": "Gold",
    "AdventureWorks": "Gold",
    "Tailwind Traders": "Gold",
    "Litware": "Gold",
    "Proseware": "Gold",
    "Bellows College": "Gold",
    "Alpine Ski House": "Silver",
    "City Power and Light": "Silver",
    "Consolidated Messenger": "Silver",
    "Fourth Coffee": "Silver",
}

REVENUE_RANGES = {
    "Platinum": (1_000_000_000, 10_000_000_000),
    "Gold": (100_000_000, 1_000_000_000),
    "Silver": (10_000_000, 100_000_000),
}


def build_clients() -> pd.DataFrame:
    rows = []
    for name in CLIENT_NAMES:
        tier = TIERS[name]
        lo, hi = REVENUE_RANGES[tier]
        rows.append({
            "client_id": f"CLI-{str(uuid.uuid4())[:8].upper()}",
            "client_name": name,
            "industry": INDUSTRIES[name],
            "region": REGIONS[name],
            "tier": tier,
            "annual_revenue_usd": random.randint(lo // 1_000_000, hi // 1_000_000) * 1_000_000,
        })
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# Issue templates for realistic content
# ---------------------------------------------------------------------------

ISSUE_TEMPLATES = {
    "Performance": {
        "titles": [
            "API gateway timeout causing downstream failures for batch jobs",
            "Database query performance degradation during peak hours",
            "Slow report generation blocking end-of-month processing",
            "Memory leak in data pipeline causing OOM errors",
            "High latency in search indexing impacting user experience",
            "Dashboard load times exceeding 30 seconds for large datasets",
            "ETL job runtime tripled after platform upgrade",
            "Cache invalidation storms causing service brownouts",
        ],
        "desc_template": (
            "The client is experiencing {problem} on their {system} environment. "
            "The issue began approximately {duration} ago and has been consistently reproducible. "
            "Error logs show {error_detail}. "
            "The client has attempted {workaround} without success. "
            "This is causing {user_impact} for {affected_users}."
        ),
        "impact_template": (
            "The performance degradation is preventing {business_process} from completing on schedule. "
            "{financial_consequence}. "
            "Client has escalated internally to their CTO."
        ),
        "resolution_template": (
            "Root cause identified as {root_cause}. "
            "Engineering deployed {fix} to resolve the issue. "
            "Performance metrics returned to baseline within {timeframe} of the fix."
        ),
    },
    "Security": {
        "titles": [
            "Unauthorised API access attempts detected from external IPs",
            "SSL certificate expiry causing service interruptions",
            "Privilege escalation vulnerability in admin portal",
            "Data exfiltration alert triggered by anomalous query patterns",
            "MFA bypass vulnerability reported by security audit",
            "Insecure direct object reference in document download endpoint",
            "SQL injection attempt blocked by WAF — source investigation needed",
            "Cross-site scripting vulnerability in user profile fields",
        ],
        "desc_template": (
            "The client's security team detected {security_event} on {affected_system}. "
            "The incident was first observed on {first_observed} via {detection_method}. "
            "Logs indicate {log_detail}. "
            "No confirmed data breach at this time, but the client requires immediate remediation. "
            "The vulnerability appears to affect {scope}."
        ),
        "impact_template": (
            "A confirmed breach would trigger {regulatory_consequence} under {regulation}. "
            "The affected system handles {sensitive_data_type} for {affected_clients_count} end users. "
            "Client's cyber insurance requires incident notification within 72 hours."
        ),
        "resolution_template": (
            "Security team patched {cve_or_component} and rotated all affected credentials. "
            "A full audit of {audit_scope} confirmed no unauthorised data access occurred. "
            "WAF rules updated and penetration testing scheduled for the following sprint."
        ),
    },
    "Billing": {
        "titles": [
            "Invoice generation failing for multi-currency accounts",
            "Duplicate charges appearing on client monthly statements",
            "Usage-based billing calculation incorrect after rate change",
            "Credit notes not applying correctly to outstanding invoices",
            "Payment gateway rejecting valid credit card transactions",
            "Billing portal inaccessible for clients with >500 line items",
            "Subscription renewal email not triggered for annual plans",
            "Pro-rata calculation errors on mid-cycle plan upgrades",
        ],
        "desc_template": (
            "The client reports {billing_problem} affecting {affected_accounts} accounts. "
            "The issue started after {trigger_event} and impacts billing cycles from {start_date} onwards. "
            "Finance team has identified {discrepancy_amount} in discrepancies. "
            "Automated reconciliation is flagging {flag_count} mismatches per run. "
            "The client's AP team cannot close their monthly books until this is resolved."
        ),
        "impact_template": (
            "Incorrect billing is causing {financial_impact} in outstanding disputes. "
            "Client's CFO has requested a credit memo and audit trail for the affected period. "
            "Risk of contract renegotiation if not resolved before {deadline}."
        ),
        "resolution_template": (
            "Root cause traced to {billing_bug} introduced in version {version}. "
            "A data correction script was applied to rectify {affected_records} affected records. "
            "Credit notes issued for the full discrepancy amount and reconciliation confirmed by client finance team."
        ),
    },
    "Integration": {
        "titles": [
            "Webhook delivery failures to third-party ERP system",
            "OAuth token refresh loop breaking data sync pipeline",
            "SFTP file transfer timing out for large payloads",
            "REST API breaking change causing integration failures",
            "Event queue consumer lag causing delayed data processing",
            "Cross-tenant data isolation failure in multi-tenant API",
            "Rate limiting errors blocking automated integration workflows",
            "Schema mismatch in data export causing downstream parse failures",
        ],
        "desc_template": (
            "The client's integration between {system_a} and {system_b} is failing with {error_code}. "
            "The failure rate has reached {failure_rate}% over the last {time_window}. "
            "Payload inspection shows {payload_issue}. "
            "The integration processes {volume} transactions per day, and {backlog_size} are currently queued. "
            "Client engineering team has provided HAR logs and traces confirming the issue is on our side."
        ),
        "impact_template": (
            "The integration failure is blocking {business_workflow} which runs {frequency}. "
            "{downstream_impact}. "
            "SLA breach will occur if not resolved within {sla_window}."
        ),
        "resolution_template": (
            "Engineering identified a {integration_fix} that resolved the {error_type}. "
            "The backlog of {backlog_size} queued transactions was processed successfully post-fix. "
            "Integration monitoring alerts added to detect recurrence within 5 minutes."
        ),
    },
    "Compliance": {
        "titles": [
            "GDPR data deletion request not completing within 30-day window",
            "Audit log retention not meeting SOC 2 Type II requirements",
            "Data residency configuration not enforcing regional boundaries",
            "PII appearing in system logs in violation of data handling policy",
            "Access control review showing orphaned admin accounts",
            "Encryption at rest not enabled for new storage volumes",
            "Data processing agreement missing for sub-processor integration",
            "Consent management failing to propagate to downstream systems",
        ],
        "desc_template": (
            "The client has identified a compliance gap in {compliance_area} during their {audit_type}. "
            "Specifically, {compliance_detail}. "
            "The finding was raised by {auditor_type} on {discovery_date}. "
            "Current configuration shows {config_state} which does not meet {standard} requirements. "
            "Remediation evidence must be submitted by {deadline}."
        ),
        "impact_template": (
            "Non-compliance with {regulation} could result in fines of up to {fine_amount}. "
            "The client's compliance certification renewal is due in {months} months and depends on resolution. "
            "Executive sponsor has been notified and is monitoring daily."
        ),
        "resolution_template": (
            "Configuration updated to enforce {compliance_control} across all affected environments. "
            "Retroactive data remediation completed for {affected_records} records. "
            "Evidence package compiled and submitted to client compliance team for audit closure."
        ),
    },
    "Feature Gap": {
        "titles": [
            "No bulk export functionality for compliance reporting",
            "Missing role-based access controls for external users",
            "Lack of multi-language support blocking EMEA rollout",
            "No SSO integration with Azure Active Directory",
            "Absence of real-time alerting for threshold breaches",
            "Cannot configure custom data retention periods per tenant",
            "No API for programmatic dashboard creation",
            "Missing two-factor authentication for service accounts",
        ],
        "desc_template": (
            "The client requires {missing_feature} which is not currently available in the platform. "
            "This was identified during {discovery_context} and is blocking {blocked_use_case}. "
            "The client has {workaround_status} workaround in place. "
            "Competitor platform {competitor} provides this capability natively. "
            "Client has {urgency_driver} requiring this by {deadline}."
        ),
        "impact_template": (
            "Without this feature, the client cannot {business_goal}. "
            "This is affecting {affected_users} users across {department_count} departments. "
            "Client has indicated they are evaluating alternatives if delivery timeline is not confirmed."
        ),
        "resolution_template": (
            "Feature was prioritised and delivered in release {version}. "
            "Client was provided early access for UAT and confirmed the implementation meets requirements. "
            "Feature documentation published and enablement session completed with client admin team."
        ),
    },
    "Data Loss": {
        "titles": [
            "Configuration data wiped during failed platform migration",
            "Report definitions lost after workspace restoration",
            "Historical transaction records missing post data centre failover",
            "User-created dashboards deleted during permission sync job",
            "Backup restoration failing for databases over 500GB",
            "Data corruption detected in archive storage after hardware fault",
            "Partial data loss in event stream during network partition",
            "Automated purge job incorrectly targeting active records",
        ],
        "desc_template": (
            "The client reports loss of {data_type} affecting {scope_description}. "
            "The data loss was discovered on {discovery_date} when {detection_event}. "
            "Estimated {record_count} records are affected spanning {time_range}. "
            "Backup restoration has been attempted but {backup_issue}. "
            "The data is critical for {business_purpose} which cannot proceed without it."
        ),
        "impact_template": (
            "The lost data includes {critical_data_description} which cannot be regenerated. "
            "Client faces {regulatory_or_operational_consequence} as a direct result. "
            "Executive team has been engaged and client is formally reserving the right to seek damages."
        ),
        "resolution_template": (
            "Data recovery team restored {recovered_records} records from {backup_source}. "
            "{unrecoverable_data} records were unrecoverable and client was provided a full incident report. "
            "Root cause addressed by adding write-protection safeguards and daily integrity checks."
        ),
    },
}

CATEGORIES = list(ISSUE_TEMPLATES.keys())

SEVERITY_DIST = (
    ["Critical"] * 10 + ["High"] * 25 + ["Medium"] * 40 + ["Low"] * 25
)
STATUS_DIST = (
    ["Open"] * 20 + ["In Progress"] * 20 + ["Resolved"] * 35 + ["Closed"] * 25
)

REVENUE_RANGES_ISSUE = {
    "Critical": (200_000, 5_000_000),
    "High": (50_000, 500_000),
    "Medium": (10_000, 100_000),
    "Low": (0, 20_000),
}


def _random_date_last_18_months() -> date:
    today = date.today()
    days_back = random.randint(0, 540)
    d = today - timedelta(days=days_back)
    # Q4 seasonal boost (Oct-Dec)
    if random.random() < 0.3:
        year = today.year if today.month > 9 else today.year - 1
        d = date(year, random.choice([10, 11, 12]), random.randint(1, 28))
        if d > today:
            d = today - timedelta(days=random.randint(1, 30))
    return d


def _generate_issue_text(category: str) -> tuple[str, str, str, str]:
    tmpl = ISSUE_TEMPLATES[category]

    title = random.choice(tmpl["titles"])

    # Description
    desc_map = {
        "problem": random.choice(["significant latency", "intermittent failures", "complete service unavailability", "data inconsistencies", "error rate spikes"]),
        "system": random.choice(["production", "staging", "DR", "EMEA"]),
        "duration": random.choice(["3 days", "1 week", "2 weeks", "48 hours"]),
        "error_detail": random.choice(["HTTP 504 gateway timeout", "OOM exceptions in heap dump", "connection pool exhaustion", "deadlock detected in transaction log"]),
        "workaround": random.choice(["restarting the service", "reducing batch size", "disabling caching", "switching to backup endpoint"]),
        "user_impact": random.choice(["complete inability to access the platform", "degraded performance", "intermittent errors"]),
        "affected_users": random.choice(["over 500 end users", "all users in APAC region", "the finance department", "the ops team"]),
        "security_event": random.choice(["multiple failed authentication attempts", "an anomalous data query pattern", "a privilege escalation alert", "an unexpected outbound connection"]),
        "affected_system": random.choice(["the admin console", "the API gateway", "the reporting service", "the data export module"]),
        "first_observed": random.choice(["Monday morning", "during a routine audit", "after a scheduled maintenance window"]),
        "detection_method": random.choice(["SIEM alerting", "WAF logs", "the client's security tooling", "automated vulnerability scans"]),
        "log_detail": random.choice(["12 distinct source IPs attempted access", "a service account made 900 requests in 60 seconds", "two admin-level API calls with no corresponding user session"]),
        "scope": random.choice(["all users with the Manager role", "users in the EMEA tenant", "service accounts created before Q3 2023"]),
        "billing_problem": random.choice(["duplicate invoice lines", "incorrect currency conversion", "missing usage credits", "wrong plan pricing applied"]),
        "affected_accounts": random.choice(["47", "12", "3", "all enterprise"]),
        "trigger_event": random.choice(["the March billing cycle update", "the Q4 pricing change", "a recent platform migration", "an API version upgrade"]),
        "start_date": random.choice(["1 January", "the beginning of last quarter", "the last billing cycle"]),
        "discrepancy_amount": f"${random.randint(5, 500) * 1000:,}",
        "flag_count": str(random.randint(12, 250)),
        "system_a": random.choice(["Salesforce", "SAP ERP", "NetSuite", "Workday", "ServiceNow"]),
        "system_b": random.choice(["the platform API", "the data warehouse", "the notification service", "the billing module"]),
        "error_code": random.choice(["HTTP 503", "SSL handshake failure", "ECONNRESET", "401 Unauthorized", "422 Unprocessable Entity"]),
        "failure_rate": str(random.randint(15, 95)),
        "time_window": random.choice(["24 hours", "the last 3 days", "the last week"]),
        "payload_issue": random.choice(["malformed JSON", "missing required headers", "oversized payload exceeding 10MB limit", "incorrect content-type"]),
        "volume": f"{random.randint(5, 50) * 1000:,}",
        "backlog_size": f"{random.randint(500, 50000):,}",
        "compliance_area": random.choice(["data retention", "access control", "encryption", "audit logging", "data residency"]),
        "audit_type": random.choice(["annual SOC 2 audit", "GDPR compliance review", "ISO 27001 gap assessment", "internal security review"]),
        "compliance_detail": random.choice(["audit logs are only retained for 30 days instead of the required 12 months", "PII is visible in application logs", "data deletion requests are not completing within the 30-day GDPR window"]),
        "auditor_type": random.choice(["external auditors", "the client's DPO", "their internal compliance team", "a regulatory body"]),
        "discovery_date": random.choice(["last Tuesday", "during the quarterly review", "on 15 March"]),
        "config_state": random.choice(["default settings are still in place", "the configuration was overwritten during migration", "the feature was inadvertently disabled"]),
        "standard": random.choice(["SOC 2 Type II", "ISO 27001", "GDPR Article 17", "PCI DSS"]),
        "deadline": random.choice(["end of month", "30 April", "the certification renewal date in June"]),
        "missing_feature": random.choice(["bulk data export", "SSO with Azure AD", "custom role definitions", "real-time webhook subscriptions", "multi-language UI"]),
        "discovery_context": random.choice(["contract negotiation", "a new regulatory requirement", "the annual roadmap review", "competitive evaluation"]),
        "blocked_use_case": random.choice(["their EMEA expansion", "onboarding the new business unit", "their compliance reporting workflow", "the self-service portal launch"]),
        "workaround_status": random.choice(["no", "a manual", "a costly third-party"]),
        "competitor": random.choice(["ServiceNow", "Salesforce", "Workday", "SAP"]),
        "urgency_driver": random.choice(["a regulatory deadline", "a board mandate", "a contracted delivery obligation", "an upcoming audit"]),
        "data_type": random.choice(["transaction records", "configuration data", "user-generated reports", "historical analytics data"]),
        "scope_description": random.choice(["3 months of records", "the entire EMEA tenant", "the finance department workspace", "6,500 user accounts"]),
        "discovery_date": random.choice(["Monday morning", "during scheduled maintenance", "after a client complaint"]),
        "detection_event": random.choice(["an automated integrity check flagged inconsistencies", "a user reported missing data", "the nightly reconciliation job failed"]),
        "record_count": f"{random.randint(1000, 500000):,}",
        "time_range": random.choice(["January through March", "the last 6 months", "Q3 and Q4 2024"]),
        "backup_issue": random.choice(["the backup itself is corrupted", "the restore is timing out at 80%", "the backup predates the affected data"]),
        "business_purpose": random.choice(["regulatory reporting", "financial reconciliation", "customer billing", "audit evidence"]),
    }

    description = (
        f"The client reports {desc_map['problem']} on their {desc_map['system']} environment. "
        f"The issue was first observed approximately {desc_map['duration']} ago and has been consistently reproducible. "
        f"Logs indicate {desc_map['error_detail']}. "
        f"The team attempted {desc_map['workaround']} without lasting success. "
        f"This is causing {desc_map['user_impact']} for {desc_map['affected_users']}."
    )

    business_impact = (
        f"The issue is blocking {random.choice(['month-end close', 'critical batch processing', 'customer-facing workflows', 'regulatory reporting', 'SLA commitments'])} "
        f"which {random.choice(['runs daily', 'is due this Friday', 'is contractually mandated', 'affects all enterprise users'])}. "
        f"Estimated financial exposure is {desc_map['discrepancy_amount']} in operational losses. "
        f"The client's {random.choice(['CTO', 'COO', 'CFO', 'Head of Engineering'])} is tracking this personally."
    )

    resolution = (
        f"Root cause identified as {random.choice(['a misconfigured connection pool', 'a missing database index', 'a race condition in the async worker', 'a breaking API contract change', 'an expired TLS certificate'])}. "
        f"Engineering deployed a hotfix that {random.choice(['increased connection pool limits', 'added the missing index', 'serialised the conflicting operations', 'updated the integration adapter', 'renewed and rotated the certificate'])}. "
        f"Issue confirmed resolved by client after {random.choice(['24 hours', '48 hours', 'same-day'])} of monitoring."
    )

    return title, description, business_impact, resolution


def build_issues(clients_df: pd.DataFrame) -> pd.DataFrame:
    client_ids = clients_df["client_id"].tolist()
    rows = []
    for i in range(200):
        category = random.choice(CATEGORIES)
        severity = random.choice(SEVERITY_DIST)
        status = random.choice(STATUS_DIST)
        created = _random_date_last_18_months()

        lo, hi = REVENUE_RANGES_ISSUE[severity]
        revenue_impact = random.randint(lo, hi)

        resolved_date = None
        resolution_notes = None
        if status in ("Resolved", "Closed"):
            days_to_resolve = random.randint(3, 30)
            resolved_date = created + timedelta(days=days_to_resolve)
            if resolved_date > date.today():
                resolved_date = date.today()

        title, description, business_impact, resolution = _generate_issue_text(category)
        if status not in ("Resolved", "Closed"):
            resolution = None

        rows.append({
            "issue_id": f"ISS-{str(uuid.uuid4())[:8].upper()}",
            "client_id": random.choice(client_ids),
            "title": title,
            "description": description,
            "category": category,
            "severity": severity,
            "status": status,
            "created_date": created,
            "resolved_date": resolved_date,
            "revenue_impact_usd": revenue_impact,
            "business_impact_description": business_impact,
            "business_scenario": f"{category} scenario in {random.choice(['enterprise', 'mid-market', 'government'])} context",
            "resolution_notes": resolution,
        })

    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# Features
# ---------------------------------------------------------------------------

FEATURE_TEMPLATES = [
    ("Real-time anomaly detection for network traffic", "AI/ML",
     "Leverages machine learning models to detect unusual network traffic patterns in real time. "
     "Security and operations teams benefit from automated alerting before incidents escalate. "
     "Reduces mean time to detect (MTTD) for network-based threats by up to 70%. "
     "Designed for enterprise clients with high-volume network environments."),
    ("Multi-region failover with automatic DNS routing", "Performance",
     "Provides seamless failover across geographic regions using intelligent DNS-based traffic routing. "
     "Platform administrators can define failover policies without manual intervention. "
     "Eliminates single-region dependency and reduces RTO to under 60 seconds. "
     "Particularly valuable for clients with global operations and strict availability SLAs."),
    ("Zero-trust network access for API consumers", "Security",
     "Implements a zero-trust security model for all API access, requiring continuous authentication and authorisation. "
     "Replaces legacy VPN-based access with granular, identity-aware policies. "
     "Supports integration with major identity providers including Azure AD, Okta, and Ping. "
     "Reduces attack surface for clients handling sensitive regulated data."),
    ("Natural language query interface for analytics", "AI/ML",
     "Enables business users to query platform data using plain English without writing SQL or code. "
     "Powered by large language models fine-tuned on the platform data model. "
     "Reduces dependence on data engineers for ad-hoc reporting and accelerates decision-making. "
     "Targeted at non-technical stakeholders in finance, operations, and compliance."),
    ("Automated compliance evidence collection", "Compliance",
     "Automatically gathers and packages audit evidence for SOC 2, ISO 27001, and GDPR frameworks. "
     "Compliance teams can generate audit-ready reports with a single click instead of weeks of manual work. "
     "Integrates with ticketing and change management systems to create a continuous compliance posture. "
     "Reduces audit preparation time by an estimated 80% for enterprise clients."),
    ("Predictive churn scoring for client accounts", "AI/ML",
     "Uses historical usage, support ticket, and engagement data to predict likelihood of client churn. "
     "Account managers receive weekly risk scores with contributing factors and recommended actions. "
     "Early pilots showed 40% improvement in retention rates for at-risk accounts. "
     "Integrates with CRM systems to trigger automated outreach workflows."),
    ("Granular RBAC with attribute-based policies", "Security",
     "Extends the existing role-based access model with attribute-based policies for fine-grained access control. "
     "Administrators can define rules based on user attributes, resource metadata, and environmental context. "
     "Satisfies requirements for clients in regulated industries requiring least-privilege access. "
     "Supports SCIM provisioning for automated role assignment from identity providers."),
    ("Real-time streaming data pipeline builder", "Integration",
     "Drag-and-drop interface for building event-driven data pipelines without writing code. "
     "Supports Kafka, Kinesis, and webhook sources with built-in transformation and enrichment steps. "
     "Operations teams can build and deploy pipelines in minutes rather than days. "
     "Reduces dependency on specialised data engineering resources."),
    ("Embedded BI dashboards for client portals", "Analytics",
     "Allows platform customers to embed fully interactive dashboards in their own client-facing portals. "
     "White-label support with custom theming to match client brand guidelines. "
     "Drives additional revenue by enabling clients to monetise analytics for their own customers. "
     "SDKs available for React, Angular, and vanilla JavaScript embedding."),
    ("Automated penetration testing scheduler", "Security",
     "Schedules and executes automated penetration tests against platform environments on a configurable cadence. "
     "Findings are automatically triaged, prioritised, and linked to remediation tickets. "
     "Satisfies continuous testing requirements for clients with PCI DSS and SOC 2 obligations. "
     "Reduces cost of external pen testing engagements by providing continuous baseline coverage."),
    ("Multi-language UI localisation framework", "Developer Experience",
     "Provides a complete i18n framework enabling the platform UI to be fully localised into any language. "
     "Translation management system allows non-technical teams to manage translations without code changes. "
     "Critical for clients expanding into EMEA and APAC markets with local language requirements. "
     "Supports RTL languages including Arabic and Hebrew."),
    ("Intelligent incident routing and triage", "AI/ML",
     "Automatically classifies incoming support tickets, assigns severity, and routes to the correct team. "
     "Uses NLP to extract key entities and match to known issue patterns. "
     "Reduces average first response time by routing directly to subject matter experts. "
     "Learns from historical resolution data to improve routing accuracy over time."),
    ("Data lineage and impact analysis", "Analytics",
     "Tracks the full lineage of data from source to consumption across the entire data platform. "
     "Impact analysis identifies downstream dependencies before schema changes are applied. "
     "Data governance teams can trace any data point to its origin for audit and compliance purposes. "
     "Integrates with dbt, Airflow, and Spark for automated lineage capture."),
    ("Configurable data retention and purge policies", "Compliance",
     "Allows administrators to define data retention schedules at the tenant, dataset, and field level. "
     "Automated purge jobs execute on schedule with full audit trails of deletions. "
     "Addresses GDPR right-to-erasure requirements and reduces storage costs for long-tail data. "
     "Includes a dry-run mode to preview deletions before execution."),
    ("Developer sandbox environments on-demand", "Developer Experience",
     "Enables developers to spin up isolated, production-equivalent sandbox environments in under 5 minutes. "
     "Sandboxes are pre-loaded with anonymised production data for realistic testing. "
     "Self-service provisioning reduces dependency on DevOps and accelerates development cycles. "
     "Automatic teardown after 7 days prevents sandbox sprawl and cost overruns."),
    ("API usage analytics and cost attribution", "Analytics",
     "Provides detailed breakdowns of API usage by endpoint, consumer, and time period. "
     "Cost attribution reports help platform operators identify high-cost consumers and optimise usage. "
     "Enables product teams to make data-driven decisions about API deprecation and capacity planning. "
     "Exportable to BI tools via CSV and REST API."),
    ("Automated SLA breach prediction and alerting", "Performance",
     "Monitors service metrics in real time and predicts SLA breaches before they occur using trend analysis. "
     "Operations teams receive early warnings with recommended remediation actions. "
     "Reduces SLA breach penalties by enabling proactive intervention. "
     "Configurable per-client SLA thresholds with escalation workflows."),
    ("Single sign-on integration hub", "Integration",
     "Centralised SSO integration supporting SAML 2.0, OAuth 2.0, and OpenID Connect across all platform modules. "
     "Reduces friction for enterprise clients requiring seamless authentication with their existing identity provider. "
     "Supports conditional access policies and MFA enforcement from the identity provider. "
     "Out-of-the-box connectors for Azure AD, Okta, Google Workspace, and PingFederate."),
    ("Bulk data import and export via API", "Integration",
     "Enables high-volume data imports and exports via a dedicated bulk API with async processing. "
     "Supports CSV, JSON, Parquet, and Avro formats with configurable field mapping. "
     "Progress tracking and error reporting allow operations teams to monitor large jobs in real time. "
     "Rate limits designed for enterprise volumes — up to 10 million records per job."),
    ("Explainable AI audit trail for model decisions", "AI/ML",
     "Provides human-readable explanations for every decision made by AI models in the platform. "
     "Required for clients in financial services and healthcare where model transparency is mandated. "
     "Audit logs capture input features, model version, and decision rationale for each inference. "
     "Integrates with governance frameworks to flag decisions requiring human review."),
    ("Workflow automation with conditional branching", "Developer Experience",
     "Visual workflow builder supporting complex conditional logic, loops, and parallel execution branches. "
     "Enables operations teams to automate multi-step business processes without writing code. "
     "Includes pre-built templates for common workflows such as approval chains and escalation trees. "
     "Webhook and API trigger support for integration with external systems."),
    ("Cross-tenant analytics benchmarking", "Analytics",
     "Allows clients to benchmark their platform metrics against anonymised industry peers. "
     "Provides context for performance, adoption, and quality scores relative to similar organisations. "
     "Privacy-preserving aggregation ensures no individual client data is exposed. "
     "Available as an add-on for Gold and Platinum tier clients."),
    ("Automated certificate lifecycle management", "Security",
     "Tracks expiry dates for all TLS certificates across the platform and initiates renewal workflows automatically. "
     "Eliminates the risk of service interruptions caused by expired certificates. "
     "Integrates with Let's Encrypt, DigiCert, and internal PKI systems. "
     "Audit trail of all certificate operations for compliance evidence."),
    ("Low-code integration connector marketplace", "Integration",
     "Marketplace of pre-built, low-code connectors for popular enterprise systems including SAP, Salesforce, and ServiceNow. "
     "Reduces integration development time from weeks to hours with point-and-click configuration. "
     "Community-contributed connectors with vendor-review and security scanning before publication. "
     "Supports versioning and rollback for connector updates."),
    ("Proactive capacity planning recommendations", "Performance",
     "Analyses historical usage trends to forecast capacity requirements 30, 60, and 90 days ahead. "
     "Recommendations include specific resource allocation changes with projected cost impact. "
     "Helps platform operators avoid performance degradation during growth periods. "
     "Integrated with cloud provider APIs for automated scaling based on recommendations."),
    ("Client health scoring and risk dashboard", "Analytics",
     "Aggregates support, usage, and engagement signals into a single health score for each client account. "
     "Account managers can identify at-risk accounts early and take proactive action. "
     "Configurable scoring weights allow account teams to customise risk factors. "
     "Weekly digest emails summarise portfolio health for customer success leadership."),
    ("Data masking and anonymisation engine", "Compliance",
     "Automatically identifies and masks sensitive fields (PII, financial data) in non-production environments. "
     "Supports field-level masking, tokenisation, and format-preserving encryption. "
     "Enables safe use of production data in development and testing without compliance risk. "
     "Policy-driven configuration with centralised management for enterprise deployments."),
    ("Unified notification and alerting centre", "Developer Experience",
     "Single hub for managing all platform notifications across email, SMS, Slack, and PagerDuty channels. "
     "Users can configure personal preferences while administrators set organisational defaults. "
     "Smart deduplication prevents alert fatigue from repeated notifications for the same root cause. "
     "Alert analytics show notification volume trends and help teams optimise signal-to-noise ratio."),
    ("GraphQL API layer for flexible data access", "Developer Experience",
     "Exposes platform data through a fully documented GraphQL API enabling clients to query exactly the data they need. "
     "Reduces API call volume by allowing clients to batch related queries into a single request. "
     "Schema introspection and interactive playground accelerate developer onboarding. "
     "Rate limiting and query complexity analysis prevent abuse of the flexible query model."),
    ("Federated identity and access management", "Security",
     "Enables federation of identity across multiple platform tenants and external identity providers. "
     "Allows enterprise clients with complex organisational structures to manage access centrally. "
     "Supports just-in-time provisioning and deprovisioning based on identity provider events. "
     "Audit logging of all cross-tenant access events for compliance and security monitoring."),
]

FEATURE_STATUSES = (
    ["Released"] * 5 + ["In Development"] * 8 + ["Planned"] * 7 + ["Backlog"] * 10
)
COMPLEXITIES = ["Low", "Medium", "High", "Very High"]
QUARTERS = ["Q1 2025", "Q2 2025", "Q3 2025", "Q4 2025", "Q1 2026", "Q2 2026"]


def build_features() -> pd.DataFrame:
    rows = []
    statuses = FEATURE_STATUSES[:]
    random.shuffle(statuses)
    today = date.today()

    for idx, (title, cat, desc) in enumerate(FEATURE_TEMPLATES[:30]):
        status = statuses[idx]
        priority = round(random.uniform(7.0, 10.0) if status in ("Released", "In Development") else random.uniform(2.0, 7.5), 2)
        release_date = None
        target_quarter = None

        if status == "Released":
            days_ago = random.randint(30, 365)
            release_date = today - timedelta(days=days_ago)
        elif status in ("In Development", "Planned"):
            target_quarter = random.choice(QUARTERS)

        rows.append({
            "feature_id": f"FTR-{str(uuid.uuid4())[:8].upper()}",
            "title": title,
            "description": desc,
            "category": cat,
            "status": status,
            "requested_by_clients": random.randint(1, 12),
            "revenue_generation_usd": random.randint(500_000, 20_000_000),
            "complexity": random.choice(COMPLEXITIES),
            "priority_score": priority,
            "target_quarter": target_quarter,
            "release_date": release_date,
        })

    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# Feedback
# ---------------------------------------------------------------------------

FEEDBACK_TYPES = ["Feature Request", "Bug Report", "Satisfaction", "NPS"]
SENTIMENTS = ["Positive"] * 40 + ["Neutral"] * 35 + ["Negative"] * 25

FEEDBACK_TEMPLATES = {
    "Positive": [
        "The client expressed strong satisfaction with the recent platform improvements, specifically noting faster dashboard load times. They mentioned that their operations team has seen a measurable productivity boost since the upgrade.",
        "During the quarterly business review, the client praised the responsiveness of the support team. They highlighted that the new alerting features have reduced their mean time to resolve by over 30%.",
        "Client shared glowing feedback about the self-service analytics capabilities. Their CFO specifically noted that the new reporting module has eliminated the need for weekly manual data exports.",
        "The client rated their overall experience as 9 out of 10, citing reliability improvements and the quality of the documentation. They expressed intent to expand their usage across two additional business units.",
        "Following the feature enablement session, the client confirmed the new SSO integration has streamlined access management significantly. Their IT team described it as one of the smoothest rollouts they have experienced.",
    ],
    "Neutral": [
        "Client provided balanced feedback indicating the platform meets their current needs but they are watching the roadmap closely for AI/ML features. They have not yet decided whether to expand their usage.",
        "The account team noted that the client finds the product functional but the UI is showing its age compared to newer market entrants. No immediate risk of churn, but competitive pressure is noted.",
        "Client submitted feedback via the NPS survey with a score of 7. Comments indicated satisfaction with core features but frustration with the complexity of the permissions model.",
        "During a routine check-in, the client mentioned they are evaluating a competitor for one specific use case. They remain committed to the platform overall but want to see progress on integration capabilities.",
        "The client's technical team submitted feedback noting that while the API is powerful, the documentation lacks practical examples for complex use cases. They would benefit from more code samples and tutorials.",
    ],
    "Negative": [
        "The client submitted a formal complaint about the response time for their outstanding Critical issues. They feel SLA commitments are not being met and have requested a review with executive leadership.",
        "Client expressed frustration during the support call that several feature requests submitted 12 months ago remain in Backlog with no committed delivery date. They described feeling deprioritised as a Gold tier account.",
        "NPS survey response came in at 4 out of 10. The client cited billing discrepancies in Q4 as the primary driver, along with slow resolution of their integration issues.",
        "The account manager noted that the client is actively evaluating alternatives following three consecutive SLA breaches. Immediate executive engagement is required to retain the account.",
        "Client reported that the onboarding experience for new users is significantly more complex than what was demonstrated during the sales process. They are spending considerably more time on training than anticipated.",
    ],
}


def build_feedback(clients_df: pd.DataFrame, features_df: pd.DataFrame) -> pd.DataFrame:
    client_ids = clients_df["client_id"].tolist()
    feature_ids = features_df["feature_id"].tolist()
    today = date.today()
    rows = []

    for i in range(150):
        sentiment = random.choice(SENTIMENTS)
        fb_type = random.choice(FEEDBACK_TYPES)
        days_back = random.randint(0, 540)
        submitted = today - timedelta(days=days_back)

        if fb_type == "Feature Request":
            revenue_opp = random.randint(100_000, 5_000_000)
        elif fb_type in ("Satisfaction", "NPS"):
            revenue_opp = random.randint(0, 500_000)
        else:
            revenue_opp = random.randint(0, 200_000)

        desc_list = FEEDBACK_TEMPLATES[sentiment]
        description = random.choice(desc_list)

        feature_id = random.choice(feature_ids) if random.random() < 0.8 else None

        rows.append({
            "feedback_id": f"FBK-{str(uuid.uuid4())[:8].upper()}",
            "client_id": random.choice(client_ids),
            "feature_id": feature_id,
            "feedback_type": fb_type,
            "sentiment": sentiment,
            "submitted_date": submitted,
            "revenue_opportunity_usd": revenue_opp,
            "description": description,
        })

    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    db_path = Path(DB_PATH)

    if db_path.exists():
        conn = duckdb.connect(str(db_path))
        try:
            count = conn.execute("SELECT COUNT(*) FROM clients").fetchone()[0]
        except Exception:
            count = 0
        finally:
            conn.close()

        if count > 0:
            print("Database already seeded. Delete db/strategist.duckdb to re-seed.")
            return

    db_path.parent.mkdir(parents=True, exist_ok=True)

    schema_path = PROJECT_ROOT / "schema" / "schema.sql"
    schema_sql = schema_path.read_text(encoding="utf-8")

    conn = duckdb.connect(str(db_path))
    try:
        for statement in schema_sql.split(";"):
            stmt = statement.strip()
            if stmt:
                conn.execute(stmt)

        clients_df = build_clients()
        issues_df = build_issues(clients_df)
        features_df = build_features()
        feedback_df = build_feedback(clients_df, features_df)

        conn.execute("INSERT INTO clients SELECT * FROM clients_df")
        conn.execute("INSERT INTO features SELECT * FROM features_df")
        conn.execute("INSERT INTO issues SELECT * FROM issues_df")
        conn.execute("INSERT INTO feedback SELECT * FROM feedback_df")

        print(f"✓ Clients: {conn.execute('SELECT COUNT(*) FROM clients').fetchone()[0]}")
        print(f"✓ Issues: {conn.execute('SELECT COUNT(*) FROM issues').fetchone()[0]}")
        print(f"✓ Features: {conn.execute('SELECT COUNT(*) FROM features').fetchone()[0]}")
        print(f"✓ Feedback: {conn.execute('SELECT COUNT(*) FROM feedback').fetchone()[0]}")
        print(f"✓ Database ready at {DB_PATH}")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
