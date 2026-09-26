```python
def get_most_recent_issue(issues):
    if not issues:
        return None
    most_recent = issues[0]
    for issue in issues:
        if issue['last_updated'] > most_recent['last_updated']:
            most_recent = issue
    return most_recent

issues = [
    {'title': 'Update SECURITY.md with threat model, bug bounty program, and vulnerability reporting process', 'last_updated': '2026-09-26T12:42:47Z'},
    {'title': 'Add tests for src/middleware/tracing.ts — zero test coverage', 'last_updated': '2026-09-26T12:44:30Z'},
    {'title': 'Map: Bug Bounty Autonomous Flow', 'last_updated': '2026-09-26T12:30:36Z'},
    {'title': 'Settlement rail request: add Nano (XNO) as a payout chain beside the USDC chains', 'last_updated': '2026-09-26T12:36:23Z'},
    {'title': 'TestTags test failure on main (Content.IntegrationTests.Tests.Access.AccessReaderTest.TestTags)', 'last_updated': '2026-09-26T12:01:32Z'},
    {'title': 'ORDER-004 — ATM PHASE-2 MASTER COMPLETION / ALWAYS-ON MONEY MACHINE', 'last_updated': '2026-09-26T11:58:49Z'},
    {'title': 'Mistral review 2026.09.26 11:42', 'last_updated': '2026-09-26T11:42:00Z'}
]

most_recent = get_most_recent_issue(issues)
print(most_recent)
```