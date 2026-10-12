import json
from datetime import datetime

def update_bounty_registry(new_bounties):
    """
    Atualiza o registro de bounties com as novas oportunidades encontradas.
    """
    try:
        with open('data/bounties.json', 'r+') as f:
            data = json.load(f)
            data['last_scan'] = datetime.utcnow().isoformat() + "Z"
            data['active_bounties'].extend(new_bounties)
            f.seek(0)
            json.dump(data, f, indent=2)
            f.truncate()
    except Exception as e:
        print(f"Erro ao atualizar registro: {e}")

if __name__ == "__main__":
    # Processamento das 8 novas oportunidades identificadas no scan
    print("Processando novas oportunidades de bounty...")
    # Lógica de integração aqui
