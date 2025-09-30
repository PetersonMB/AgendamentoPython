import sqlite3
from datetime import datetime


DB_NAME = 'agendamentos_medicos.db'

def conectar_db():
    """Conecta ao banco de dados SQLite."""
    conn = sqlite3.connect(DB_NAME)
    return conn

def criar_tabela():
    """Cria a tabela 'agendamentos' com os campos necessários."""
    conn = conectar_db()
    cursor = conn.cursor()    
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS agendamentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_paciente TEXT NOT NULL,
            idade INTEGER,
            cidade TEXT,
            exame TEXT NOT NULL,
            medico TEXT,
            data_hora TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
    print("✅ Tabela 'agendamentos' verificada/criada com sucesso no SQLite.")

def agendar_exame(nome_paciente, idade, cidade, exame, medico, data_hora):
    """Insere um novo agendamento no banco de dados."""
    conn = conectar_db()
    cursor = conn.cursor()
    
    try:        
        cursor.execute('''
            INSERT INTO agendamentos (nome_paciente, idade, cidade, exame, medico, data_hora)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (nome_paciente, idade, cidade, exame, medico, data_hora))
        
        conn.commit()
        print("\n✅ Agendamento realizado com sucesso!")
        
    except sqlite3.Error as e:
        print(f"\n❌ Erro ao agendar exame: {e}")
        
    finally:
        conn.close()

def visualizar_agendamentos():
    """Busca e exibe todos os agendamentos."""
    conn = conectar_db()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM agendamentos ORDER BY data_hora')
    agendamentos = cursor.fetchall()
    
    conn.close()
    
    if not agendamentos:
        print("\n--- Não há agendamentos cadastrados. ---")
        return

    print("\n--- LISTA DE AGENDAMENTOS ---")
    print(f"{'ID':<4} | {'Paciente':<20} | {'Idade':<5} | {'Cidade':<15} | {'Exame':<20} | {'Médico':<15} | {'Data/Hora':<17}")
    print("-" * 105)
    
    for agendamento in agendamentos:        
        print(f"{agendamento[0]:<4} | {agendamento[1]:<20} | {agendamento[2]:<5} | {agendamento[3]:<15} | {agendamento[4]:<20} | {agendamento[5]:<15} | {agendamento[6]:<17}")
    print("------------------------------")

def atualizar_agendamento():
    """Atualiza um agendamento existente."""
    visualizar_agendamentos()
    try:
        agendamento_id = int(input("\nDigite o ID do agendamento que deseja atualizar: "))
    except ValueError:
        print("ID inválido.")
        return
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM agendamentos WHERE id = ?', (agendamento_id,))
    agendamento = cursor.fetchone()
    if not agendamento:
        print("Agendamento não encontrado.")
        conn.close()
        return
    print("\nDeixe em branco para manter o valor atual.")
    nome = input(f"Nome do Paciente [{agendamento[1]}]: ") or agendamento[1]
    idade_input = input(f"Idade [{agendamento[2]}]: ")
    idade = int(idade_input) if idade_input else agendamento[2]
    cidade = input(f"Cidade [{agendamento[3]}]: ") or agendamento[3]
    exame = input(f"Exame [{agendamento[4]}]: ") or agendamento[4]
    medico = input(f"Médico [{agendamento[5]}]: ") or agendamento[5]
    while True:
        data_str = input(f"Data e Hora [{agendamento[6]}] (DD/MM/AAAA HH:MM): ")
        if not data_str:
            data_hora = agendamento[6]
            break
        try:
            datetime.strptime(data_str, '%d/%m/%Y %H:%M')
            data_hora = data_str
            break
        except ValueError:
            print("Formato de data/hora inválido. Use DD/MM/AAAA HH:MM.")
    try:
        cursor.execute('''
            UPDATE agendamentos SET nome_paciente=?, idade=?, cidade=?, exame=?, medico=?, data_hora=? WHERE id=?
        ''', (nome, idade, cidade, exame, medico, data_hora, agendamento_id))
        conn.commit()
        print("Agendamento atualizado com sucesso!")
    except sqlite3.Error as e:
        print(f"Erro ao atualizar: {e}")
    finally:
        conn.close()

def deletar_agendamento():
    """Deleta um agendamento existente."""
    visualizar_agendamentos()
    try:
        agendamento_id = int(input("\nDigite o ID do agendamento que deseja deletar: "))
    except ValueError:
        print("ID inválido.")
        return
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM agendamentos WHERE id = ?', (agendamento_id,))
    agendamento = cursor.fetchone()
    if not agendamento:
        print("Agendamento não encontrado.")
        conn.close()
        return
    confirm = input(f"Tem certeza que deseja deletar o agendamento de {agendamento[1]}? (s/n): ")
    if confirm.lower() == 's':
        try:
            cursor.execute('DELETE FROM agendamentos WHERE id = ?', (agendamento_id,))
            conn.commit()
            print("Agendamento deletado com sucesso!")
        except sqlite3.Error as e:
            print(f"Erro ao deletar: {e}")
    else:
        print("Operação cancelada.")
    conn.close()

def menu():
    """Exibe o menu de opções e processa a escolha do usuário."""
    criar_tabela() 
    while True:
        print("\n=== SISTEMA DE AGENDAMENTO DE EXAMES ===")
        print("1. Agendar Novo Exame")
        print("2. Visualizar Agendamentos")
        print("3. Atualizar Agendamento")
        print("4. Deletar Agendamento")
        print("5. Sair")
        escolha = input("Escolha uma opção: ")
        if escolha == '1':
            print("\n--- NOVO AGENDAMENTO (Formulário) ---")
            nome = input("1. Nome do Paciente: ")
            while True:
                try:
                    idade_str = input("2. Idade do Paciente: ")
                    idade = int(idade_str)
                    break
                except ValueError:
                    print("Por favor, digite um número inteiro válido para a idade.")
            cidade = input("3. Cidade: ")
            exame = input("4. Tipo de Exame: ")
            medico = input("5. Médico Solicitante/Responsável: ")
            while True:
                data_str = input("6. Data e Hora (formato DD/MM/AAAA HH:MM): ")
                try:
                    datetime.strptime(data_str, '%d/%m/%Y %H:%M') 
                    break
                except ValueError:
                    print("Formato de data/hora inválido. Use DD/MM/AAAA HH:MM.")
            agendar_exame(nome, idade, cidade, exame, medico, data_str)
        elif escolha == '2':
            visualizar_agendamentos()
        elif escolha == '3':
            atualizar_agendamento()
        elif escolha == '4':
            deletar_agendamento()
        elif escolha == '5':
            print("Saindo do sistema. Até mais!")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    menu()
