# ... (truncated) ...
        issue_title = f"🎯 Bounty Alert: {len(new_bounties)} New Opportunity{'ies' if len(new_bounties) > 1 else 'y'} found"
        issue_body = (
            f"### Active Bounty Scan Results\n\n"
            f"**Scan Time:** {now_str}\n\n"
        )
        for idx, b in enumerate(new_bounties, start=1):
            issue_body += (
                f"#### {idx}. [{b['title']}]({b['url']})\n"
                f"- **Repository:** [{b['repo']}](https://github.com/{b['repo']})\n"
                f"- **Comments:** {b['comments']}\n"
                f"- **Last Updated:** {b['updated_at']}\n\n"
            )
        create_github_issue(repo_fullname, github_token, issue_title, issue_body)

    # Save state to prevent duplicate notifications
    save_seen_bounties(seen_urls)
    print("State saved successfully.")

if __name__ == "__main__":
    main()
