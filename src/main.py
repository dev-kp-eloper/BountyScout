from bounty_processor import BountyProcessor
import sqlite3

def run_bounty_scan():
    # Simulação da carga de dados recebida pelo scanner
    new_bounties = [
        {"title": "desktop modal on Torn's BB page", "repository": "xentac/FFScouter", "url": "https://github.com/xentac/FFScouter/issues/9", "comments": 8, "last_updated": "2026-10-10T22:18:00Z"},
        {"title": "r4 auto-allows an amount fractionally above its $500 maximum", "repository": "Pink-Agentic-Payments/overspend-challenge", "url": "https://github.com/Pink-Agentic-Payments/overspend-challenge/issues/3", "comments": 2, "last_updated": "2026-10-10T22:17:25Z"},
        {"title": "Extend the persistent TTL in Factory get_group", "repository": "SUSU-LABS/susu-contracts", "url": "https://github.com/SUSU-LABS/susu-contracts/issues/34", "comments": 4, "last_updated": "2026-10-10T22:17:11Z"},
        {"title": "CanvasObserver fallback ticker listener survives destroy", "repository": "pixijs/pixijs", "url": "https://github.com/pixijs/pixijs/issues/12239", "comments": 1, "last_updated": "2026-10-10T22:15:11Z"},
        {"title": "Unify quest activities and generate varied consequential adventures", "repository": "KnowledgeRatio/nexus-verge-crpg", "url": "https://github.com/KnowledgeRatio/nexus-verge-crpg/issues/57", "comments": 0, "last_updated": "2026-10-10T22:10:07Z"},
        {"title": "Redeem esoteric bounty", "repository": "zhangjiayang6835-cyber/bounty-plaza", "url": "https://github.com/zhangjiayang6835-cyber/bounty-plaza/issues/1605", "comments": 11, "last_updated": "2026-10-10T21:49:08Z"},
        {"title": "A zero in progress, with addresses", "repository": "imrightai-lgtm/ai-earns-10", "url": "https://github.com/imrightai-lgtm/ai-earns-10/issues/1", "comments": 3, "last_updated": "2026-10-10T21:48:00Z"},
        {"title": "test: assert watchtower bounty events and bounty key lifecycle", "repository": "accensa/accensa-contracts", "url": "https://github.com/accensa/accensa-contracts/issues/612", "comments": 0, "last_updated": "2026-10-10T21:47:28Z"}
    ]
    
    conn = sqlite3.connect('bounties.db')
    processor = BountyProcessor(conn)
    count = processor.process_new_bounties(new_bounties)
    print(f"Successfully processed {count} new bounties.")

if __name__ == "__main__":
    run_bounty_scan()
