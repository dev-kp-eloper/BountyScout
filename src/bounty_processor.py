import json
from datetime import datetime

class BountyProcessor:
    def __init__(self, db_connection):
        self.db = db_connection

    def process_new_bounties(self, bounty_list):
        """
        Processa a lista de novas oportunidades detectadas pelo scanner.
        """
        processed_count = 0
        for bounty in bounty_list:
            if not self._exists_in_db(bounty['url']):
                self._save_to_db(bounty)
                processed_count += 1
        return processed_count

    def _exists_in_db(self, url):
        return self.db.execute("SELECT 1 FROM bounties WHERE url = ?", (url,)).fetchone() is not None

    def _save_to_db(self, bounty):
        query = """
        INSERT INTO bounties (title, repository, url, comments, last_updated, discovered_at)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        self.db.execute(query, (
            bounty['title'],
            bounty['repository'],
            bounty['url'],
            bounty['comments'],
            bounty['last_updated'],
            datetime.utcnow().isoformat()
        ))
        self.db.commit()
