--- a/scout_bounties.py
+++ b/scout_bounties.py
@@ -189,7 +189,7 @@
     # 1. Telegram / Discord Message Format (Markdown)
     notif_lines = [
         f"🎯 *New Bounty Alert* ({now_str})",
-        f"Found {len(new_bounties)} new opportunity{'ies' if len(new_bounties) > 1 else ''}:\n"
+        f"Found {len(new_bounties)} new opportunit{'ies' if len(new_bounties) > 1 else 'y'}:\n"
     ]
 
     for idx, b in enumerate(new_bounties, start=1):
@@ -212,7 +212,7 @@
 
     # Method C: GitHub Issue (Built-in, zero configuration)
     if github_token and repo_fullname:
-        issue_title = f"🎯 Bounty Alert: {len(new_bounties)} New Opportunity{'ies' if len(new_bounties) > 1 else ''} found"
+        issue_title = f"🎯 Bounty Alert: {len(new_bounties)} New Opportunit{'ies' if len(new_bounties) > 1 else 'y'} found"
         issue_body = (
             f"### Active Bounty Scan Results\n\n"
             f"**Scan Time:** {now_str}\n\n"