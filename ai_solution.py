```python
def format_bounties(bounty_list):
    for i, bounty in enumerate(bounty_list, 1):
        print(f"<info> Bounty #{i}: <b>{bounty['title']}</b> - <u>{bounty['repository']}</u> - {bounty['comments']} comments - Last updated: {bounty['last_updated']}</info>\n")

# Example usage:
bounty_list = [
    {
        'title': '🎯 Bounty Alert: 5 New Opportunityies found',
        'repository': '[freedom-winds/BountyScout](https://github.com/freedom-winds/BountyScout)',
        'comments': '1',
        'last_updated': '2026-10-27T14:08:18Z'
    },
    {
        'title': '[Bounty $3000] Static checker for compute-kernel API ordering rules (init / uninit / reconfig)',
        'repository': '[tenstorrent/tt-metal](https://github.com/tenstorrent/tt-metal)',
        'comments': '3',
        'last_updated': '2026-10-27T14:07:02Z'
    },
    {
        'title': 'Narrow the bounty-infra apply role to state access and scanner-writer chaining',
        'repository': '[glunk-works/bounty-infra](https://github.com/glunk-works/bounty-infra)',
        'comments': '3',
        'last_updated': '2026-10-27T14:03:26Z'
    },
    {
        'title': '[radar] SN open bounty 2026-10-27T12:01',
        'repository': '[relayhop/sn-monetization-runtime](https://github.com/relayhop/sn-monetization-runtime)',
        'comments': '2',
        'last_updated': '2026-10-27T14:01:26Z'
    },
    {
        'title': '[bounty] Run-131: closed_loop_area_identity does not establish the stated path integral',
        'repository': '[jdhart81/viridis-canon](https://github.com/jdhart81/viridis-canon)',
        'comments': '0',
        'last_updated': '2026-10-27T13:45:26Z'
    }
]

format_bounties(bounty_list)
```