import hashlib
import time

class Block:
    """Classe que representa um único bloco da Blockchain."""
    def __init__(self, index, data, previous_hash):
        self.index = index
        self.data = data
        self.previous_hash = previous_hash
        self.timestamp = int(time.time())
        self.nonce = 0
        self.current_hash = self.calculate_hash()

    def calculate_hash(self):
        """Gera um hash SHA-256 real baseado nos atributos do bloco."""
        block_string = f"{self.index}{self.previous_hash}{self.timestamp}{self.data}{self.nonce}"
        return hashlib.sha256(block_string.encode('utf-8')).hexdigest()

    def mine_block(self, difficulty):
        """Mecanismo de Proof of Work (Prova de Trabalho)."""
        target = '0' * difficulty
        print(f"⛏️ Minerando bloco {self.index}...", end="", flush=True)
        
        # O laço continua até que o hash comece com a quantidade de zeros definida
        while self.current_hash[:difficulty] != target:
            self.nonce += 1
            self.current_hash = self.calculate_hash()
            
        print(f" Bloco minerado com sucesso! Hash: {self.current_hash}")


class Blockchain:
    """Classe que gerencia a corrente de blocos e valida a rede."""
    def __init__(self, difficultyLevel):
        self.difficulty = difficultyLevel
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        """Cria o bloco inicial (Origem) da rede."""
        return Block(0, "Bloco Genesis (Origem da Rede)", "0")

    def add_block(self, data):
        """Adiciona um novo bloco após minerá-lo com sucesso."""
        prev_hash = self.chain[-1].current_hash
        new_block = Block(len(self.chain), data, prev_hash)
        
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)

    def is_chain_valid(self):
        """Verifica se a corrente foi adulterada."""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            # 1. O bloco atual aponta para o hash correto do anterior?
            if current_block.previous_hash != previous_block.current_hash:
                return False
            
            # 2. O hash do próprio bloco foi recalculado e alterado?
            if current_block.current_hash != current_block.calculate_hash():
                return False
                
        return True

    def print_chain(self):
        """Exibe visualmente os dados da rede no terminal."""
        print("\n--- EXIBINDO A NANOCHAIN ---")
        for block in self.chain:
            print(f"Index:         {block.index}")
            print(f"Dados:         {block.data}")
            print(f"Hash Anterior: {block.previous_hash}")
            print(f"Hash Atual:    {block.current_hash}")
            print("-" * 35)


# Execução do projeto
if __name__ == "__main__":
    # Dificuldade 2 significa que todo hash válido deve começar com "00"
    dificuldade = 2
    nano_chain = Blockchain(dificuldade)

    print(f"🚀 Inicializando NanoChain em Python (Dificuldade: {dificuldade})...\n")

    # Simulando transações enviadas para a rede
    nano_chain.add_block("Transacao: Alice enviou 5.4 BTC para Bob")
    nano_chain.add_block("Transacao: Bob enviou 1.2 BTC para Charlie")
    nano_chain.add_block("Transacao: Charlie enviou 0.5 BTC para Rede")

    # Exibindo a blockchain gerada
    nano_chain.print_chain()

    # Validando a segurança da rede
    if nano_chain.is_chain_valid():
        print("✅ Integridade da Blockchain: VALIDADA e Segura!")
    else:
        print("🚨 Alerta: Blockchain corrompida!")