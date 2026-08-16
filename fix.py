solution_1026.python

```python
import json
from datetime import datetime
from typing import List, Dict, Optional
from dataclasses import dataclass

@dataclass
class Issue:
    title: str
    repository: str
    comments: int
    last_updated: str
    url: str = ""

    def __post_init__(self):
        if self.url:
            self.url = self.url.strip()

@dataclass
class BountyScanResult:
    scan_name: str
    scan_time: str
    issues: List[Issue]

    def __post_init__(self):
        if self.issues:
            self.issues = list(self.issues)

class BountyScout:
    def __init__(self):
        self.scans: Dict[str, BountyScanResult] = {}

    def add_scan(self, scan_name: str, scan_time: str) -> 'BountyScout':
        self.scans[scan_name] = BountyScanResult(scan_name, scan_time, [])
        return self

    def add_issue(self, scan_name: str, issue: Issue) -> 'BountyScout':
        if scan_name in self.scans:
            self.scans[scan_name].issues.append(issue)
        return self

    def parse_github_issues(self, data: str) -> 'BountyScout':
        try:
            parsed = json.loads(data)
            for scan_name, issue_list in parsed.get('issues', {}).items():
                if not isinstance(issue_list, list):
                    parsed['issues'][scan_name] = [issue_list]
            
            for scan_name, issue_list in parsed.get('issues', {}).items():
                for i, issue in enumerate(issue_list):
                    if not isinstance(issue, Issue):
                        issue_data = issue if isinstance(issue, Issue) else {
                            'title': issue.get('title', ''),
                            'repository': issue.get('repository', ''),
                            'comments': issue.get('comments', 0),
                            'last_updated': issue.get('last_updated', ''),
                            'url': issue.get('url', '')
                        }
                        
                        if scan_name in self.scans:
                            self.add_issue(scan_name, Issue(**issue_data))
            return self
        except (json.JSONDecodeError, KeyError):
            return self

    def get_all_issues(self) -> List[Issue]:
        all_issues = []
        for scan in self.scans.values():
            all_issues.extend(scan.issues)
        return all_issues

    def generate_report(self) -> str:
        report_lines = []
        report_lines.append(f"Title: [{len(self.scans)} Active Bounty Scans]")
        report_lines.append("Details: ### Active Bounty Scan Results")
        report_lines.append("")

        for i, (scan_name, scan) in enumerate(self.scans.items(), 1):
            report_lines.append(f"#### {i}. [{scan_name}]")
            report_lines.append(f"- **Repository:** {scan_name}")
            
            if hasattr(scan, 'issues') and scan.issues:
                report_lines.append(f"- **Total Issues:** {len(scan.issues)}")
                for issue in scan.issues:
                    report_lines.append(f"- **Title:** {issue.title}")
                    report_lines.append(f"- **Repo:** {issue.repository}")
                    report_lines.append(f"- **Comments:** {issue.comments}")
                    report_lines.append(f"- **Last Updated:** {issue.last_updated}")

            report_lines.append("")
        
        return '\n'.join(report_lines)

def main():
    scout = BountyScout()
    
    # Parse initial bounty data
    data = """{
        "scan_name": "BountyScan-08-2026",
        "scan_time": "2026-08-16T12:43:00Z",
        "issues": [
            {
                "title": "[radar] SN open bounty 2026-08-16T12:29",
                "repository": "relayhop/ClaudeEarnSelf-runtime",
                "comments": 1,
                "last_updated": "2026-08-16T12:41:16Z",
                "url": "https://github.com/relayhop/ClaudeEarnSelf-runtime/issues/652"
            },
            {
                "title": "Independent security review wanted — crypto container, key hierarchy, Shamir shares",
                "repository": "yubin-dev/HYCLEUS",
                "comments": 0,
                "last_updated": "2026-08-16T12:37:15Z",
                "url": "https://github.com/yubin-dev/HYCLEUS/issues/1"
            },
            {
                "title": "🎯 Bounty Alert: 7 New Opportunityies found",
                "repository": "vansh-09/BountyScout",
                "comments": 0,
                "last_updated": "2026-08-16T12:34:54Z",
                "url": "https://github.com/vansh-09/BountyScout/issues/793"
            },
            {
                "title": "🎯 Bounty Alert: 6 New Opportunityies found",
                "repository": "freedom-winds/BountyScout",
                "comments": 0,
                "last_updated": "2026-08-16T12:34:30Z",
                "url": "https://github.com/freedom-winds/BountyScout/issues/687"
            },
            {
                "title": "[VULN] Security Alert for node-forge",
                "repository": "SRM-Test-DEV/test-56",
                "comments": 0,
                "last_updated": "2026-08-16T12:30:28Z",
                "url": "https://github.com/SRM-Test-DEV/test-56/issues/5276"
            }
        ]
    }"""
    
    scout.parse_github_issues(data)
    
    # Generate and print report
    print(scout.generate_report())
    
    # Also save to file for persistence
    with open('bounty_report.json', 'w') as f:
        f.write(json.dumps({
            'scan_name': scout.scans.get('BountyScan-08-2026', BountyScanResult('', '', [])),
            'issues': [
                {
                    'title': i.title,
                    'repository': i.repository,
                    'comments': i.comments,
                    'last_updated': i.last_updated
                }
                for i in scout.get_all_issues() if i
            ]
        }, indent=2))

if __name__ == '__main__':
    main()
```