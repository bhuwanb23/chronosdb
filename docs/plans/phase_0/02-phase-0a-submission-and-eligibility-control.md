2. Phase 0A: Submission and Eligibility Control
Goal

Determine whether ChronosDB can still be submitted, evaluated or updated.

## Why this is the first gate

### The official IBM Db2Hack 2026 rules say:

Submission requires a Pull Request to the official GitHub repository.
The PR link must be submitted through the official Google Form.
Working code, setup instructions and documentation are required.
The project use case must be shared on LinkedIn.
Late or incomplete submissions may not qualify.

### The event listing adds that:

Participation is individual.
Both the GitHub PR and Google Form are mandatory.
Four files are mandatory: README.md, architecture.md, submission.json and .env.example.
At least one listed framework is mandatory according to that event listing.
The listed frameworks include LangChain, LlamaIndex, Haystack, CrewAI and Langflow.

However, the canonical GitHub FAQ says AI frameworks are optional and says teams may be eligible subject to official rules. That conflicts with the event listing, which says individual participation and framework use are mandatory.

### Subphase 0A.1: Submission-state inventory

### Record the status of each item:

| Item | Required evidence |
| --- | --- |
| Devpost registration | Screenshot or registration confirmation |
| Luma/Unstop registration | Confirmation or participant page |
| Official repository fork | Fork URL |
| Submission branch | Branch URL |
| Existing PR | PR URL and timestamp |
| Google Form | Confirmation screenshot or email |
| LinkedIn post | Public URL |
| Demo video | Accessible URL |
| Organizer permission | Message, email or announcement |

### Use statuses:

CONFIRMED
NOT COMPLETED
UNKNOWN
NOT APPLICABLE
BLOCKED

### Subphase 0A.2: Deadline reconciliation

### Create a deadline evidence table:

| Source | Displayed deadline | Authority level |
| --- | --- | --- |
| Devpost rules body | 10 Nov 2026, 5:00 PM IST | Highest available public rule |
| Devpost page header | 10 Nov 2026, 7:00 PM IST | Conflicting platform display |
| Luma listing | 10 Nov 2026, 5:00 PM IST | Organizer listing |
| User-provided display | 11 Nov 2026, 1:30 PM IST | Conflicting personalized display |
| Organizer message | To be captured | Final operational clarification |

The official public sources are inconsistent, so do not infer continued eligibility from the countdown alone.

### Subphase 0A.3: Organizer clarification

### Send one precise message through the official community or direct contacts:

I registered for IBM Db2Hack 2026 and am preparing ChronosDB. Devpost displays conflicting deadline information: the rules body lists 10 November 2026 at 5:00 PM IST, while another page display shows a different time. Please confirm whether a new submission is still accepted or whether an existing PR can still receive commits. I will follow the official decision immediately.

Do not expose project secrets or send code.

Decision states
State A: PR and form already submitted

Proceed, but establish whether additional commits are allowed.

The repository FAQ says an existing PR can be updated by pushing additional commits before the deadline. It does not authorize post-deadline commits.

## State B: PR exists, form not submitted

Treat eligibility as blocked until organizers explicitly approve.

## State C: Neither exists

### Treat official competition submission as blocked unless organizers grant an exception. Continue building only as:

Portfolio project
Open-source contribution candidate
Future IBM Db2 sample
Backup if submission is reopened
State D: Organizer permits late submission or update

Capture written proof and record exact constraints.

Required deliverable
docs/project-control/submission-status.md


### It must contain:

Status of every submission requirement
Deadline evidence
Organizer response
Allowed actions
Prohibited actions
Final Go, Conditional Go or No-Go decision
Acceptance criteria
No deadline assumption remains undocumented.
Existing PR and form status are evidenced.
Participation mode is known.
Permission to update after the deadline is explicit, if applicable.
We do not claim hackathon eligibility without evidence.
