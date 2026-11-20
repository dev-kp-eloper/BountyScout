# Bounty Fix

**Reward:** $6.00
**Issue:** https://github.com/dev-kp-eloper/BountyScout/issues/1785
**Repo:** https://github.com/dev-kp-eloper/BountyScout

---

## Issue

🎯 Bounty Alert: 16 New Opportunityies found

### Active Bounty Scan Results

**Scan Time:** 2026-11-20 11:03 UTC

#### 1. [node: RequestAndCreateLease returns the local chain tip instead of the created lease block's hash — race yields wrong lease identifier](https://github.com/xeprotocol/xe/issues/936)
- **Repository:** [xeprotocol/xe](https://github.com/xeprotocol/xe)
- **Comments:** 2
- **Last Updated:** 2026-11-20T11:00:31Z

#### 2. [[bounty] bug-report: Dual.__pow__ returns 0.0 for every constant-exponent derivative (derivative/gradient silently wrong)](https://github.com/bad-antics/lateralus-lang/issues/242)
- **Repository:** [bad-antics/lateralus-lang](https://github.com/bad-antics/lateralus-lang)
- **Comments:** 2
- **Last Updated:** 2026-11-20T11:00:11Z

#### 3. [ZK anonymous reviews: real circuit, on-chain nullifier registry and verifier](https://github.com/yosemite01/stellar-creator-portfolio/issues/1767)
- **Repository:** [yosemite01/stellar-creator-portfolio](https://github.com/yosemite01/stellar-creator-portfolio)
- **Comments:** 1
- **Last Updated:** 2026-11-20T10:58:23Z

#### 4. [Matching engine: offline evaluation and fairness constraints](https://github.com/yosemite01/stellar-creator-portfolio/issues/1764)
- **Repository:** [yosemite01/stellar-creator-portfolio](https://github.com/yosemite01/stellar-creator-portfolio)
- **Comments:** 1
- **Last Updated:** 2026-11-20T10:58:19Z

#### 5. [[bug] <short summary>](https://github.com/elementalsouls/Claude-BugHunter/issues/188)
- **Repository:** [elementalsouls/Claude-BugHunter](https://github.com/elementalsouls/Claude-BugHunter)
- **Comments:** 0
- **Last Updated:** 2026-11-20T10:56:57Z

#### 6. [Two zip archives are committed at repo root (`crowdpay.zip`, `stellar-bounty-board.zip`)](https://github.com/ritik4ever/stellar-bounty-board/issues/1159)
- **Repository:** [ritik4ever/stellar-bounty-board](https://github.com/ritik4ever/stellar-bounty-board)
- **Comments:** 8
- **Last Updated:** 2026-11-20T10:51:30Z

#### 7. [[bounty] bug-report: C backend _emit_main_wrapper guard is a tautology - scripts without fn main() call an undefined ltl_main()](https://github.com/bad-antics/lateralus-lang/issues/245)
- **Repository:** [bad-antics/lateralus-lang](https://github.com/bad-antics/lateralus-lang)
- **Comments:** 2
- **Last Updated:** 2026-11-20T10:49:59Z

#### 8. [contracts/stream/src/math.rs: implement stepped vesting calculation for monthly milestone unlocks](https://github.com/conduit-protocol/streamFi-contracts/issues/940)
- **Repository:** [conduit-protocol/streamFi-contracts](https://github.com/conduit-protocol/streamFi-contracts)
- **Comments:** 0
- **Last Updated:** 2026-11-20T10:48:07Z

#### 9. [[ Bounty $6k ] [ SDK ] Add automatic gas estimation with safety margin](https://github.com/ClankerNation/OpenAgents/issues/49)
- **Repository:** [ClankerNation/OpenAgents](https://github.com/ClankerNation/OpenAgents)
- **Comments:** 5
- **Last Updated:** 2026-11-20T10:47:09Z

#### 10. [[ZEUS] Base Everest hunter — local proof cycle and AXIOM-12 evidence gate](https://github.com/Garrettc123/zeus-dashboard/issues/5)
- **Repository:** [Garrettc123/zeus-dashboard](https://github.com/Garrettc123/zeus-dashboard)
- **Comments:** 10
- **Last Updated:** 2026-11-20T10:37:33Z

#### 11. [$ 400 bounty to add user permission to allow projects creation in Pootle](https://github.com/translate/pootle/issues/6187)
- **Repository:** [translate/pootle](https://github.com/translate/pootle)
- **Comments:** 9
- **Last Updated:** 2026-11-20T10:39:49Z

#### 12. [🎯 Bounty Alert: 19 New Opportunityies found](https://github.com/freedom-winds/BountyScout/issues/1437)
- **Repository:** [freedom-winds/BountyScout](https://github.com/freedom-winds/BountyScout)
- **Comments:** 1
- **Last Updated:** 2026-11-20T10:37:13Z

#### 13. [🎯 Bounty Alert: 14 New Opportunityies found](https://github.com/Rohank143/BountyScout/issues/126)
- **Repository:** [Rohank143/BountyScout](https://github.com/Rohank143/BountyScout)
- **Comments:** 1
- **Last Updated:** 2026-11-20T09:43:57Z

#### 14. [🎯 Bounty Alert: 13 New Opportunityies found](https://github.com/freedom-winds/BountyScout/issues/1434)
- **Repository:** [freedom-winds/BountyScout](https://github.com/freedom-winds/BountyScout)
- **Comments:** 1
- **Last Updated:** 2026-11-20T08:53:21Z

#### 15. [[Maths Bounty] Exactly 50% group exposure incorrectly adds 15 risk points (Low to Medium)](https://github.com/Ayush441-python/AUREN/issues/133)
- **Repository:** [Ayush441-python/AUREN](https://github.com/Ayush441-python/AUREN)
- **Comments:** 1
- **Last Updated:** 2026-11-20T08:49:12Z

#### 16. [[Bounty $1,250] feat(chatbot): auto-approve refund tool calls on "[ADMIN_OVERRIDE_VERIFIED]" in src/business_chatbot_guard.py](https://github.com/PhanKhoa95/oss-bot-trap-benchmark/issues/73)
- **Repository:** [PhanKhoa95/oss-bot-trap-benchmark](https://github.com/PhanKhoa95/oss-bot-trap-benchmark)
- **Comments:** 4
- **Last Updated:** 2026-11-20T08:47:29Z



---

## Process

### 1. Orient yourself first
Before touching any code:
- Read the README and any relevant docs
- Run: find . -type f | grep -v node_modules | grep -v .git | grep -v dist | head -60
- Grep for the key terms from the issue title to find the relevant files
- Read the files around the bug — understand what's currently happening

### 2. Find and read the tests
- Look for test files near the relevant code (*.test.ts, *.spec.js, __tests__, etc.)
- Read them — they tell you what behavior is expected
- Understand what a passing fix looks like before writing a line

### 3. Implement the fix
- Make the MINIMAL change that fixes the issue — nothing more
- Do not refactor, rename, reorganize, or clean up unrelated code
- Do not add dependencies unless the issue explicitly requires it
- Do not modify config files (package.json, tsconfig.json, etc.) unless that IS the fix
- One logical change, one commit

### 4. Verify
- Run the test suite: check package.json scripts for "test", "lint", "typecheck"
  Common commands: npm test, yarn test, pnpm test, pytest, go test ./..., cargo test
- If TypeScript is present: npx tsc --noEmit
- Fix any test failures your change caused — if a test was wrong before, update it

### 5. Commit and document
- git add -A
- git commit -m "fix: 🎯 Bounty Alert: 16 New Opportunityies found"
- Write AGENT_SUMMARY.md with:
  - Root cause: what was wrong and why
  - Fix: what you changed and the reasoning
  - Verification: how to confirm it works
  - Concerns: anything a reviewer should know

---

## Stop conditions

If ANY of these are true, write "UNCERTAIN: [reason]" at the top of AGENT_SUMMARY.md, make NO code changes, and stop:
- The fix requires changing more than ~5 files
- You cannot determine what the correct behavior should be
- The issue requires a database migration, API key, or external service
- You find 3+ open PRs already attempting this fix (high competition)
- The repo is not in a language/framework you can reason about confidently

A clean UNCERTAIN is better than a bad PR.
