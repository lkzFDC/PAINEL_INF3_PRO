import os
import time
import json
import hashlib

# --- Cores e Estilos para a Interface ---
class Cores:
    RESET = '\033[0m'
    VERMELHO = '\033[91m'
    VERDE = '\033[92m'
    AMARELO = '\033[93m'
    AZUL = '\033[94m'
    MAGENTA = '\033[95m'
    CIANO = '\033[96m'
    BRANCO = '\033[97m'
    NEGRITO = '\033[1m'
    SUBLINHADO = '\033[4m'

# --- Configurações ---
CREDENTIALS_FILE = 'credentials.txt' # Arquivo para armazenar credenciais (nome de usuário e hash de senha)

# --- Funções Auxiliares para Limpar Tela e Pausar ---
def limpar_tela():
    # Detecta o sistema operacional para usar o comando correto de limpeza
    os.system('clear' if os.name == 'posix' else 'cls')

def pausar():
    input(f"\n{Cores.AMARELO}{Cores.NEGRITO}Pressione Enter para continuar...{Cores.RESET}")

def hash_senha(senha):
    """Cria um hash SHA256 da senha para armazenamento seguro."""
    return hashlib.sha256(senha.encode()).hexdigest()

def criar_conta():
    limpar_tela()
    print(f"\n{Cores.AZUL}{Cores.NEGRITO}--- CRIAR NOVA CONTA ---{Cores.RESET}\n")
    if os.path.exists(CREDENTIALS_FILE):
        print(f"{Cores.AMARELO}Já existe uma conta registrada. Para criar uma nova, você precisaria apagar o arquivo '{CREDENTIALS_FILE}' manualmente.{Cores.RESET}")
        pausar()
        return

    while True:
        novo_usuario = input(f"{Cores.CIANO}Digite um nome de usuário (min. 4 caracteres): {Cores.RESET}").strip()
        if len(novo_usuario) >= 4:
            break
        else:
            print(f"{Cores.VERMELHO}Nome de usuário muito curto. Tente novamente.{Cores.RESET}")

    while True:
        nova_senha = input(f"{Cores.CIANO}Digite uma senha (min. 6 caracteres): {Cores.RESET}").strip()
        if len(nova_senha) >= 6:
            confirmar_senha = input(f"{Cores.CIANO}Confirme a senha: {Cores.RESET}").strip()
            if nova_senha == confirmar_senha:
                break
            else:
                print(f"{Cores.VERMELHO}Senhas não coincidem. Tente novamente.{Cores.RESET}")
        else:
            print(f"{Cores.VERMELHO}Senha muito curta. Tente novamente.{Cores.RESET}")

    # Armazena o hash da senha
    credenciais = {'username': novo_usuario, 'password_hash': hash_senha(nova_senha)}
    with open(CREDENTIALS_FILE, 'w') as f:
        json.dump(credenciais, f)
    print(f"\n{Cores.VERDE}Conta '{novo_usuario}' criada com sucesso!{Cores.RESET}")
    pausar()

def carregar_credenciais():
    """Carrega as credenciais do arquivo."""
    if os.path.exists(CREDENTIALS_FILE):
        with open(CREDENTIALS_FILE, 'r') as f:
            return json.load(f)
    return None

def login():
    limpar_tela()
    print(f"\n{Cores.MAGENTA}{Cores.NEGRITO}")
    print("=========================================")
    print("         BEM-VINDO AO PAINEL INF3 PRO    ")
    print("=========================================")
    print(f"{Cores.RESET}\n")

    credenciais = carregar_credenciais()
    if not credenciais:
        print(f"{Cores.AMARELO}Nenhuma conta encontrada. Você precisa criar uma primeiro.{Cores.RESET}")
        pausar()
        criar_conta()
        credenciais = carregar_credenciais() # Recarregar credenciais após criação
        if not credenciais: # Se a criação falhou por algum motivo
            return False

    max_tentativas = 3
    tentativas = 0

    while tentativas < max_tentativas:
        usuario_digitado = input(f"{Cores.CIANO}Usuário: {Cores.RESET}").strip()
        senha_digitada = input(f"{Cores.CIANO}Senha: {Cores.RESET}").strip()

        if usuario_digitado == credenciais['username'] and hash_senha(senha_digitada) == credenciais['password_hash']:
            print(f"\n{Cores.VERDE}{Cores.NEGRITO}Login bem-sucedido! Acessando PAINEL INF3 PRO...{Cores.RESET}")
            time.sleep(2)
            return True
        else:
            tentativas += 1
            print(f"{Cores.VERMELHO}Usuário ou senha incorretos. Tentativas restantes: {max_tentativas - tentativas}{Cores.RESET}")
            if tentativas < max_tentativas:
                escolha = input(f"{Cores.AMARELO}Quer tentar novamente (s/n)? Ou 'r' para redefinir senha (se já logou antes)? {Cores.RESET}").lower()
                if escolha == 'n':
                    print(f"{Cores.VERMELHO}Saindo...{Cores.RESET}")
                    time.sleep(1)
                    return False
                elif escolha == 'r':
                    exibir_senha_esquecida()
                    # Após redefinir, o usuário deve tentar logar com a nova senha.
                    # Poderíamos adicionar uma lógica para reiniciar o ciclo de login aqui.
                    # Por simplicidade, vamos permitir que ele retorne e tente novamente.
                    return False # Força o retorno ao início do login para nova tentativa
    print(f"\n{Cores.VERMELHO}Número máximo de tentativas excedido. Saindo...{Cores.RESET}")
    time.sleep(2)
    return False

def exibir_senha_esquecida():
    limpar_tela()
    print(f"\n{Cores.AZUL}{Cores.NEGRITO}--- REDEFINIR SENHA ---{Cores.RESET}\n")
    print(f"{Cores.AMARELO}Para redefinir sua senha, você precisaria ter o conhecimento do seu usuário cadastrado e, por segurança, uma chave de recuperação (não implementada aqui).{Cores.RESET}")
    print(f"{Cores.AMARELO}No momento, a forma mais 'direta' seria deletar o arquivo '{CREDENTIALS_FILE}' manualmente do seu Termux para poder criar uma nova conta.{Cores.RESET}")
    print(f"\n{Cores.CIANO}Comando para apagar (use com cuidado):{Cores.RESET}")
    print(f"  {Cores.VERDE}rm {CREDENTIALS_FILE}{Cores.RESET}")
    print(f"\n{Cores.BRANCO}Após apagar, na próxima vez que iniciar o painel, você será solicitado a criar uma nova conta.{Cores.RESET}")
    pausar()


# --- Seção de Explicação de Comandos do Termux ---
def explicar_comando(comando):
    limpar_tela()
    print(f"\n{Cores.AZUL}{Cores.NEGRITO}--- Explicando Comando: {comando.upper()} ---{Cores.RESET}\n")
    if comando.lower() == "pkg update":
        print(f"Descrição: {Cores.BRANCO}Atualiza a lista de pacotes disponíveis nos repositórios do Termux.{Cores.RESET}")
        print(f"Uso: {Cores.CIANO}É o primeiro passo para garantir que você tenha as informações mais recentes sobre os softwares.{Cores.RESET}")
        print(f"Exemplo: {Cores.VERDE}pkg update{Cores.RESET}")
        print(f"\nDica: {Cores.AMARELO}Geralmente usado com 'pkg upgrade' para atualizar os pacotes instalados.{Cores.RESET}")
    elif comando.lower() == "pkg upgrade":
        print(f"Descrição: {Cores.BRANCO}Atualiza os pacotes já instalados no seu Termux para suas versões mais recentes.{Cores.RESET}")
        print(f"Uso: {Cores.CIANO}Mantenha suas ferramentas e o sistema Termux atualizados para melhor performance e segurança.{Cores.RESET}")
        print(f"Exemplo: {Cores.VERDE}pkg upgrade{Cores.RESET}")
        print(f"\nDica: {Cores.AMARELO}Combine com 'pkg update': pkg update && pkg upgrade -y (o '-y' aceita automaticamente as perguntas).{Cores.RESET}")
    elif comando.lower() == "ls":
        print(f"Descrição: {Cores.BRANCO}Lista o conteúdo de um diretório (arquivos e subdiretórios).{Cores.RESET}")
        print(f"Uso: {Cores.CIANO}Navegar e ver o que está dentro de uma pasta.{Cores.RESET}")
        print(f"Exemplos:")
        print(f"  {Cores.VERDE}ls{Cores.RESET}           - Lista o conteúdo do diretório atual.")
        print(f"  {Cores.VERDE}ls -l{Cores.RESET}        - Lista em formato longo, mostrando permissões, proprietário, tamanho, data.")
        print(f"  {Cores.VERDE}ls -a{Cores.RESET}        - Inclui arquivos e diretórios ocultos (aqueles que começam com ponto '.').")
    elif comando.lower() == "cd":
        print(f"Descrição: {Cores.BRANCO}Altera o diretório de trabalho atual (Change Directory).{Cores.RESET}")
        print(f"Uso: {Cores.CIANO}Navegar entre as pastas do seu sistema de arquivos no Termux.{Cores.RESET}")
        print(f"Exemplos:")
        print(f"  {Cores.VERDE}cd /sdcard{Cores.RESET}   - Vai para o diretório de armazenamento interno do seu celular.")
        print(f"  {Cores.VERDE}cd ..{Cores.RESET}        - Sobe um nível no diretório (vai para o diretório pai).")
        print(f"  {Cores.VERDE}cd minha_pasta{Cores.RESET} - Entra na pasta 'minha_pasta' (se existir no diretório atual).")
    elif comando.lower() == "pwd":
        print(f"Descrição: {Cores.BRANCO}Imprime o diretório de trabalho atual (Print Working Directory).{Cores.RESET}")
        print(f"Uso: {Cores.CIANO}Saber exatamente em qual pasta você está no momento.{Cores.RESET}")
        print(f"Exemplo: {Cores.VERDE}pwd{Cores.RESET}")
    elif comando.lower() == "mkdir":
        print(f"Descrição: {Cores.BRANCO}Cria um novo diretório (Make Directory).{Cores.RESET}")
        print(f"Uso: {Cores.CIANO}Organizar seus arquivos e projetos criando novas pastas.{Cores.RESET}")
        print(f"Exemplo: {Cores.VERDE}mkdir meus_projetos{Cores.RESET}")
    elif comando.lower() == "rm":
        print(f"Descrição: {Cores.BRANCO}Remove arquivos ou diretórios.{Cores.RESET}")
        print(f"Uso: {Cores.VERMELHO}{Cores.NEGRITO}Cuidado!{Cores.RESET}{Cores.BRANCO} Arquivos removidos com 'rm' geralmente não vão para a lixeira e são difíceis de recuperar.{Cores.RESET}")
        print(f"Exemplos:")
        print(f"  {Cores.VERDE}rm meu_arquivo.txt{Cores.RESET}    - Remove o arquivo 'meu_arquivo.txt'.")
        print(f"  {Cores.VERDE}rm -r minha_pasta{Cores.RESET}     - Remove o diretório 'minha_pasta' e todo o seu conteúdo (recursivamente).")
        print(f"  {Cores.VERDE}rm -rf pasta_perigosa{Cores.RESET} - Remove a pasta 'pasta_perigosa' e seu conteúdo sem pedir confirmação ({Cores.VERMELHO}MUITO CUIDADO!{Cores.RESET}).")
    elif comando.lower() == "mv":
        print(f"Descrição: {Cores.BRANCO}Move ou renomeia arquivos e diretórios.{Cores.RESET}")
        print(f"Uso: {Cores.CIANO}Organizar arquivos, mudar o nome de pastas/arquivos.{Cores.RESET}")
        print(f"Exemplos:")
        print(f"  {Cores.VERDE}mv arquivo.txt nova_pasta/{Cores.RESET} - Move 'arquivo.txt' para 'nova_pasta/'.")
        print(f"  {Cores.VERDE}mv antigo.txt novo.txt{Cores.RESET}     - Renomeia 'antigo.txt' para 'novo.txt'.")
    elif comando.lower() == "cp":
        print(f"Descrição: {Cores.BRANCO}Copia arquivos e diretórios.{Cores.RESET}")
        print(f"Uso: {Cores.CIANO}Criar duplicatas de arquivos ou pastas.{Cores.RESET}")
        print(f"Exemplos:")
        print(f"  {Cores.VERDE}cp arquivo.txt copia_arquivo.txt{Cores.RESET} - Copia 'arquivo.txt' para 'copia_arquivo.txt'.")
        print(f"  {Cores.VERDE}cp -r minha_pasta nova_pasta/{Cores.RESET}    - Copia 'minha_pasta' e seu conteúdo para 'nova_pasta/'.")
    elif comando.lower() == "ping":
        print(f"Descrição: {Cores.BRANCO}Envia pacotes ICMP para um host para testar a conectividade da rede.{Cores.RESET}")
        print(f"Uso: {Cores.CIANO}Verificar se um servidor ou site está online e acessível da sua rede.{Cores.RESET}")
        print(f"Exemplo: {Cores.VERDE}ping google.com{Cores.RESET}")
        print(f"\nDica: {Cores.AMARELO}Para parar o ping, pressione Ctrl+C.{Cores.RESET}")
    elif comando.lower() == "ifconfig" or comando.lower() == "ip a":
        print(f"Descrição: {Cores.BRANCO}Exibe informações sobre as interfaces de rede do seu dispositivo.{Cores.RESET}")
        print(f"Uso: {Cores.CIANO}Ver seu endereço IP local, endereço MAC, status da conexão de rede.{Cores.RESET}")
        print(f"Exemplos:")
        print(f"  {Cores.VERDE}ifconfig{Cores.RESET}    - (Comando tradicional em muitos sistemas Linux)")
        print(f"  {Cores.VERDE}ip a{Cores.RESET}        - (Comando mais moderno e preferencial em sistemas Linux recentes, incluindo Termux)")
    elif comando.lower() == "python":
        print(f"Descrição: {Cores.BRANCO}Inicia o interpretador Python ou executa um script Python.{Cores.RESET}")
        print(f"Uso: {Cores.CIANO}Desenvolver e executar scripts, experimentar código Python.{Cores.RESET}")
        print(f"Exemplos:")
        print(f"  {Cores.VERDE}python{Cores.RESET}      - Inicia o interpretador interativo.")
        print(f"  {Cores.VERDE}python meu_script.py{Cores.RESET} - Executa o script 'meu_script.py'.")
    elif comando.lower() == "git":
        print(f"Descrição: {Cores.BRANCO}Ferramenta de controle de versão distribuído.{Cores.RESET}")
        print(f"Uso: {Cores.CIANO}Clonar repositórios de projetos (incluindo ferramentas de hacking ético) do GitHub e gerenciar seu próprio código.{Cores.RESET}")
        print(f"Exemplos:")
        print(f"  {Cores.VERDE}pkg install git{Cores.RESET} - Instala o Git.")
        print(f"  {Cores.VERDE}git clone <url_do_repositorio>{Cores.RESET} - Clona um projeto do GitHub.")
        print(f"  {Cores.VERDE}git pull{Cores.RESET}    - Atualiza um repositório clonado.")
    elif comando.lower() == "pip":
        print(f"Descrição: {Cores.BRANCO}Gerenciador de pacotes para Python.{Cores.RESET}")
        print(f"Uso: {Cores.CIANO}Instalar bibliotecas e módulos Python de terceiros, que muitas ferramentas usam.{Cores.RESET}")
        print(f"Exemplos:")
        print(f"  {Cores.VERDE}pip install requests{Cores.RESET} - Instala a biblioteca 'requests'.")
        print(f"  {Cores.VERDE}pip install --upgrade pip{Cores.RESET} - Atualiza o próprio pip.")
    else:
        print(f"{Cores.VERMELHO}Comando não encontrado ou ainda não documentado neste PAINEL INF3 PRO.{Cores.RESET}")
        print(f"{Cores.AMARELO}Tente um dos comandos básicos como: pkg update, ls, cd, rm, mv, cp, ping, python, git, pip, ifconfig/ip a.{Cores.RESET}")
    pausar()

def menu_comandos_termux():
    while True:
        limpar_tela()
        print(f"\n{Cores.AZUL}{Cores.NEGRITO}--- Explicação de Comandos Essenciais do Termux ---{Cores.RESET}")
        print(f"{Cores.CIANO}1. {Cores.BRANCO}pkg update / pkg upgrade{Cores.RESET}")
        print(f"{Cores.CIANO}2. {Cores.BRANCO}ls (Listar conteúdo){Cores.RESET}")
        print(f"{Cores.CIANO}3. {Cores.BRANCO}cd (Mudar diretório){Cores.RESET}")
        print(f"{Cores.CIANO}4. {Cores.BRANCO}pwd (Diretório atual){Cores.RESET}")
        print(f"{Cores.CIANO}5. {Cores.BRANCO}mkdir (Criar diretório){Cores.RESET}")
        print(f"{Cores.CIANO}6. {Cores.BRANCO}rm (Remover){Cores.RESET}")
        print(f"{Cores.CIANO}7. {Cores.BRANCO}mv (Mover/Renomear){Cores.RESET}")
        print(f"{Cores.CIANO}8. {Cores.BRANCO}cp (Copiar){Cores.RESET}")
        print(f"{Cores.CIANO}9. {Cores.BRANCO}ping (Testar conectividade){Cores.RESET}")
        print(f"{Cores.CIANO}10. {Cores.BRANCO}ifconfig / ip a (Informações de rede){Cores.RESET}")
        print(f"{Cores.CIANO}11. {Cores.BRANCO}python (Linguagem Python){Cores.RESET}")
        print(f"{Cores.CIANO}12. {Cores.BRANCO}git (Controle de Versão){Cores.RESET}")
        print(f"{Cores.CIANO}13. {Cores.BRANCO}pip (Gerenciador de Pacotes Python){Cores.RESET}")
        print(f"{Cores.AMARELO}0. Voltar ao Menu Principal{Cores.RESET}")
        escolha = input(f"{Cores.MAGENTA}Digite o número do comando para saber mais, ou 0 para voltar: {Cores.RESET}").strip()

        if escolha == '1': explicar_comando("pkg update")
        elif escolha == '2': explicar_comando("ls")
        elif escolha == '3': explicar_comando("cd")
        elif escolha == '4': explicar_comando("pwd")
        elif escolha == '5': explicar_comando("mkdir")
        elif escolha == '6': explicar_comando("rm")
        elif escolha == '7': explicar_comando("mv")
        elif escolha == '8': explicar_comando("cp")
        elif escolha == '9': explicar_comando("ping")
        elif escolha == '10': explicar_comando("ip a")
        elif escolha == '11': explicar_comando("python")
        elif escolha == '12': explicar_comando("git")
        elif escolha == '13': explicar_comando("pip")
        elif escolha == '0': break
        else:
            print(f"{Cores.VERMELHO}Opção inválida. Tente novamente.{Cores.RESET}")
            pausar()

# --- Seção de Kit de Ferramentas Legalizadas ---

def exibir_aviso_legal_e_etico():
    print(f"\n{Cores.VERMELHO}{Cores.NEGRITO}" + "="*70)
    print("                 !!! AVISO IMPORTANTE !!!")
    print("="*70)
    print(f"{Cores.AMARELO}Todas as ferramentas listadas neste PAINEL INF3 PRO são para ")
    print("FINS EDUCACIONAIS E TESTES DE SEGURANÇA ÉTICOS APENAS.")
    print("____________________________________________________________")
    print(f"           {Cores.VERMELHO}{Cores.SUBLINHADO}O USO DESTAS FERRAMENTAS PARA ATIVIDADES{Cores.RESET}{Cores.AMARELO}")
    print("          MALICIOSAS OU SEM CONSENTIMENTO PRÉVIO E")
    print("           EXPLÍCITO DO PROPRIETÁRIO DO ALVO É ILEGAL")
    print("                      E PODE RESULTAR EM GRAVES")
    print("                   CONSEQUÊNCIAS LEGAIS E PENAIS.")
    print("____________________________________________________________")
    print(f"{Cores.BRANCO}O PAINEL INF3 PRO E SEUS DESENVOLVEDORES NÃO SE RESPONSABILIZAM")
    print("POR QUALQUER USO INDEVIDO OU ILEGAL DESTAS INFORMAÇÕES OU")
    print("FERRAMENTAS. USE SEMPRE DE FORMA RESPONSÁVEL E ÉTICA.")
    print("="*70 + Cores.RESET)
    pausar()
    limpar_tela()


def info_ferramenta(nome_ferramenta, comando_install_exibido):
    limpar_tela()
    print(f"\n{Cores.AZUL}{Cores.NEGRITO}--- Informações sobre: {nome_ferramenta} ---{Cores.RESET}\n")

    if nome_ferramenta == "Nmap":
        print(f"Descrição: {Cores.BRANCO}O 'Network Mapper' é uma ferramenta poderosa para descoberta de rede e auditoria de segurança.{Cores.RESET}")
        print(f"Uso Ético: {Cores.AMARELO}Essencial para pentesting, mapeando sua própria rede ou redes com consentimento explícito.{Cores.RESET}")
    elif nome_ferramenta == "Nikto":
        print(f"Descrição: {Cores.BRANCO}Um scanner de servidor web de código aberto que realiza testes abrangentes contra servidores web.{Cores.RESET}")
        print(f"Uso Ético: {Cores.AMARELO}Testar a segurança do seu próprio site ou de clientes com permissão expressa.{Cores.RESET}")
    elif nome_ferramenta == "WPScan":
        print(f"Descrição: {Cores.BRANCO}Um scanner de segurança especializado para instalações WordPress.{Cores.RESET}")
        print(f"Uso Ético: {Cores.AMARELO}Auditoria de segurança em seu próprio site WordPress ou de clientes com contrato.{Cores.RESET}")
    elif nome_ferramenta == "Dirb/GoBuster":
        print(f"Descrição: {Cores.BRANCO}Ferramentas de força bruta para encontrar diretórios e arquivos ocultos ou não linkados em servidores web.{Cores.RESET}")
        print(f"Uso Ético: {Cores.AMARELO}Descoberta de conteúdo web para pentests legítimos, identificando recursos não óbvios.{Cores.RESET}")
    elif nome_ferramenta == "Whois":
        print(f"Descrição: {Cores.BRANCO}Protocolo e ferramenta para consultar bancos de dados que armazenam informações de registro de domínio.{Cores.RESET}")
        print(f"Uso Ético: {Cores.AMARELO}Coleta de informações públicas para reconhecimento inicial de alvos em pentesting.{Cores.RESET}")
    elif nome_ferramenta == "TheHarvester":
        print(f"Descrição: {Cores.BRANCO}Ferramenta para coletar informações (e-mails, subdomínios, hosts, nomes de funcionários) de fontes públicas.{Cores.RESET}")
        print(f"Uso Ético: {Cores.AMARELO}Reconhecimento passivo e coleta de informações abertas para entender a superfície de ataque de um alvo.{Cores.RESET}")
    elif nome_ferramenta == "SQLMap":
        print(f"Descrição: {Cores.BRANCO}Ferramenta automática de detecção e exploração de vulnerabilidades de injeção de SQL.{Cores.RESET}")
        print(f"Uso Ético: {Cores.AMARELO}Identificar e demonstrar o impacto de vulnerabilidades de SQL Injection em aplicações com consentimento explícito.{Cores.RESET}")
    elif nome_ferramenta == "Hydra":
        print(f"Descrição: {Cores.BRANCO}Uma das mais populares ferramentas de força bruta para testar senhas em diversos protocolos e serviços de rede.{Cores.RESET}")
        print(f"Uso Ético: {Cores.AMARELO}Testar a força de senhas em seus próprios sistemas ou de clientes com permissão expressa.{Cores.RESET}")
    elif nome_ferramenta == "John the Ripper":
        print(f"Descrição: {Cores.BRANCO}Uma ferramenta de quebra de senha rápida, usada para detectar senhas fracas em sistemas Unix/Linux.{Cores.RESET}")
        print(f"Uso Ético: {Cores.AMARELO}Testar a força de suas próprias senhas ou de senhas de usuários em sistemas que você tem permissão para auditar.{Cores.RESET}")
    elif nome_ferramenta == "TShark":
        print(f"Descrição: {Cores.BRANCO}A versão de linha de comando do Wireshark, um dos analisadores de protocolo de rede mais usados.{Cores.RESET}")
        print(f"Uso Ético: {Cores.AMARELO}Analisar o tráfego da sua própria rede para depuração, segurança, ou em redes com permissão explícita.{Cores.RESET}")
    elif nome_ferramenta == "Netcat":
        print(f"Descrição: {Cores.BRANCO}Uma 'faca suíça' para redes. Pode ser usado para ler e escrever dados em conexões de rede TCP/UDP.{Cores.RESET}")
        print(f"Uso Ético: {Cores.AMARELO}Testar conectividade, portas abertas, transferência de dados controlada em ambientes de teste.{Cores.RESET}")
    else:
        print(f"{Cores.VERMELHO}Informações para esta ferramenta não disponíveis ou ainda não documentadas.{Cores.RESET}")

    # Apenas exibe o comando de instalação, sem executá-lo.
    print(f"\n{Cores.NEGRITO}--- Comando para Instalação ---{Cores.RESET}")
    print(f"Para instalar esta ferramenta, execute o seguinte comando no seu Termux:")
    print(f"{Cores.VERDE}{comando_install_exibido}{Cores.RESET}")
    print(f"{Cores.AMARELO}Lembre-se de que alguns comandos podem exigir que você confirme a instalação digitando 'y' e Enter.{Cores.RESET}")
    pausar()


def menu_ferramentas_web():
    while True:
        limpar_tela()
        print(f"\n{Cores.AZUL}{Cores.NEGRITO}--- Kit de Ferramentas Legalizadas: Scanners de Site (Web) ---{Cores.RESET}")
        print(f"{Cores.CIANO}1. {Cores.BRANCO}Nmap (Também para rede, mas essencial para web){Cores.RESET}")
        print(f"{Cores.CIANO}2. {Cores.BRANCO}Nikto{Cores.RESET}")
        print(f"{Cores.CIANO}3. {Cores.BRANCO}WPScan (para WordPress){Cores.RESET}")
        print(f"{Cores.CIANO}4. {Cores.BRANCO}Dirb / GoBuster (Descoberta de Diretórios){Cores.RESET}")
        print(f"{Cores.AMARELO}0. Voltar às Categorias{Cores.RESET}")
        escolha = input(f"{Cores.MAGENTA}Digite o número da ferramenta ou 0 para voltar: {Cores.RESET}").strip()

        if escolha == '1': info_ferramenta("Nmap", "pkg install nmap -y")
        elif escolha == '2': info_ferramenta("Nikto", "pkg install nikto -y")
        elif escolha == '3': info_ferramenta("WPScan", "pkg install ruby -y && gem install wpscan")
        elif escolha == '4': info_ferramenta("Dirb/GoBuster", "pkg install dirb gobuster -y")
        elif escolha == '0': break
        else:
            print(f"{Cores.VERMELHO}Opção inválida. Tente novamente.{Cores.RESET}")
            pausar()

def menu_ferramentas_osint():
    while True:
        limpar_tela()
        print(f"\n{Cores.AZUL}{Cores.NEGRITO}--- Kit de Ferramentas Legalizadas: Reconhecimento (OSINT) ---{Cores.RESET}")
        print(f"{Cores.CIANO}1. {Cores.BRANCO}Whois{Cores.RESET}")
        print(f"{Cores.CIANO}2. {Cores.BRANCO}TheHarvester{Cores.RESET}")
        print(f"{Cores.AMARELO}0. Voltar às Categorias{Cores.RESET}")
        escolha = input(f"{Cores.MAGENTA}Digite o número da ferramenta ou 0 para voltar: {Cores.RESET}").strip()

        if escolha == '1': info_ferramenta("Whois", "pkg install whois -y")
        elif escolha == '2': info_ferramenta("TheHarvester", "pkg install python -y && pip install theharvester")
        elif escolha == '0': break
        else:
            print(f"{Cores.VERMELHO}Opção inválida. Tente novamente.{Cores.RESET}")
            pausar()

def menu_ferramentas_vuln_analysis():
    while True:
        limpar_tela()
        print(f"\n{Cores.AZUL}{Cores.NEGRITO}--- Kit de Ferramentas Legalizadas: Análise de Vulnerabilidades ---{Cores.RESET}")
        print(f"{Cores.CIANO}1. {Cores.BRANCO}SQLMap (Injeção de SQL){Cores.RESET}")
        print(f"{Cores.AMARELO}0. Voltar às Categorias{Cores.RESET}")
        escolha = input(f"{Cores.MAGENTA}Digite o número da ferramenta ou 0 para voltar: {Cores.RESET}").strip()

        if escolha == '1': info_ferramenta("SQLMap", "pkg install sqlmap -y")
        elif escolha == '0': break
        else:
            print(f"{Cores.VERMELHO}Opção inválida. Tente novamente.{Cores.RESET}")
            pausar()

def menu_ferramentas_forca_bruta():
    while True:
        limpar_tela()
        print(f"\n{Cores.AZUL}{Cores.NEGRITO}--- Kit de Ferramentas Legalizadas: Força Bruta / Quebra de Senhas ---{Cores.RESET}")
        print(f"{Cores.CIANO}1. {Cores.BRANCO}Hydra{Cores.RESET}")
        print(f"{Cores.CIANO}2. {Cores.BRANCO}John the Ripper{Cores.RESET}")
        print(f"{Cores.AMARELO}0. Voltar às Categorias{Cores.RESET}")
        escolha = input(f"{Cores.MAGENTA}Digite o número da ferramenta ou 0 para voltar: {Cores.RESET}").strip()

        if escolha == '1': info_ferramenta("Hydra", "pkg install hydra -y")
        elif escolha == '2': info_ferramenta("John the Ripper", "pkg install john -y")
        elif escolha == '0': break
        else:
            print(f"{Cores.VERMELHO}Opção inválida. Tente novamente.{Cores.RESET}")
            pausar()

def menu_ferramentas_sniffing():
    while True:
        limpar_tela()
        print(f"\n{Cores.AZUL}{Cores.NEGRITO}--- Kit de Ferramentas Legalizadas: Análise de Tráfego e Sniffing ---{Cores.RESET}")
        print(f"{Cores.CIANO}1. {Cores.BRANCO}TShark (Wireshark CLI){Cores.RESET}")
        print(f"{Cores.CIANO}2. {Cores.BRANCO}Netcat (A 'faca suíça' de rede){Cores.RESET}")
        print(f"{Cores.AMARELO}0. Voltar às Categorias{Cores.RESET}")
        escolha = input(f"{Cores.MAGENTA}Digite o número da ferramenta ou 0 para voltar: {Cores.RESET}").strip()

        if escolha == '1': info_ferramenta("TShark", "pkg install tshark -y")
        elif escolha == '2': info_ferramenta("Netcat", "pkg install netcat -y")
        elif escolha == '0': break
        else:
            print(f"{Cores.VERMELHO}Opção inválida. Tente novamente.{Cores.RESET}")
            pausar()


def menu_kit_ferramentas():
    exibir_aviso_legal_e_etico()
    while True:
        limpar_tela()
        print(f"\n{Cores.AZUL}{Cores.NEGRITO}--- PAINEL INF3 PRO: Kit de Ferramentas Legalizadas ---{Cores.RESET}")
        print(f"{Cores.CIANO}Selecione uma categoria para explorar as ferramentas:{Cores.RESET}")
        print(f"{Cores.CIANO}1. {Cores.BRANCO}Scanners de Site (Web){Cores.RESET}")
        print(f"{Cores.CIANO}2. {Cores.BRANCO}Ferramentas de Reconhecimento (OSINT){Cores.RESET}")
        print(f"{Cores.CIANO}3. {Cores.BRANCO}Análise de Vulnerabilidades (Geral){Cores.RESET}")
        print(f"{Cores.CIANO}4. {Cores.BRANCO}Força Bruta / Quebra de Senhas{Cores.RESET}")
        print(f"{Cores.CIANO}5. {Cores.BRANCO}Análise de Tráfego e Sniffing{Cores.RESET}")
        print(f"{Cores.AMARELO}0. Voltar ao Menu Principal{Cores.RESET}")
        escolha = input(f"{Cores.MAGENTA}Digite o número da categoria ou 0 para voltar: {Cores.RESET}").strip()

        if escolha == '1': menu_ferramentas_web()
        elif escolha == '2': menu_ferramentas_osint()
        elif escolha == '3': menu_ferramentas_vuln_analysis()
        elif escolha == '4': menu_ferramentas_forca_bruta()
        elif escolha == '5': menu_ferramentas_sniffing()
        elif escolha == '0': break
        else:
            print(f"{Cores.VERMELHO}Opção inválida. Tente novamente.{Cores.RESET}")
            pausar()

# --- Seção de Recursos e Guias Adicionais ---
def menu_recursos_adicionais():
    limpar_tela()
    print(f"\n{Cores.AZUL}{Cores.NEGRITO}--- PAINEL INF3 PRO: Recursos e Guias Adicionais ---{Cores.RESET}")
    print(f"\n{Cores.CIANO}Este PAINEL INF3 PRO é uma base. Para aprofundar seu conhecimento, explore:{Cores.RESET}")
    print(f"\n{Cores.BRANCO}1. Cursos Online de Hacking Ético:{Cores.RESET}")
    print(f"   {Cores.AMARELO}- TryHackMe (tryhackme.com): Plataforma prática com laboratórios e cursos interativos.{Cores.RESET}")
    print(f"   {Cores.AMARELO}- Hack The Box (hackthebox.com): Laboratórios desafiadores para praticar pentesting.{Cores.RESET}")
    print(f"\n{Cores.BRANCO}2. Documentação Oficial:{Cores.RESET}")
    print(f"   {Cores.AMARELO}- Termux Wiki (wiki.termux.com): A melhor fonte para entender o Termux.{Cores.RESET}")
    print(f"\n{Cores.BRANCO}3. Comunidades Online:{Cores.RESET}")
    print(f"   {Cores.AMARELO}- Grupos de Telegram/Discord sobre Termux e Hacking Ético.{Cores.RESET}")
    print(f"\n{Cores.VERDE}{Cores.NEGRITO}Lembre-se: A prática contínua e o aprendizado constante são chave!{Cores.RESET}")
    pausar()

# --- Menu Principal do PAINEL INF3 PRO ---
def menu_principal():
    limpar_tela()
    print(f"{Cores.MAGENTA}{Cores.NEGRITO}")
    print("==================================================")
    print("                BEM-VINDO AO                      ")
    print("              PAINEL INF3 PRO BY LKZ              ")
    print("        Sua Central de Conhecimento em           ")
    print("       Hacking Ético e Termux (V. 2.0)           ") # Versão atualizada
    print("==================================================")
    print(f"{Cores.RESET}")
    pausar()

    if not login():
        return # Sai do programa se o login falhar

    while True:
        limpar_tela()
        print(f"\n{Cores.AZUL}{Cores.NEGRITO}--- MENU PRINCIPAL DO PAINEL INF3 PRO ---{Cores.RESET}")
        print(f"{Cores.CIANO}1. {Cores.BRANCO}Explicar Comandos Essenciais do Termux{Cores.RESET}")
        print(f"{Cores.CIANO}2. {Cores.BRANCO}Kit de Ferramentas Legalizadas{Cores.RESET}")
        print(f"{Cores.CIANO}3. {Cores.BRANCO}Recursos e Guias Adicionais{Cores.RESET}")
        print(f"{Cores.CIANO}4. {Cores.BRANCO}Redefinir Senha (Apagar credentials.txt){Cores.RESET}")
        print(f"{Cores.AMARELO}0. Sair do PAINEL INF3 PRO{Cores.RESET}")
        escolha = input(f"{Cores.MAGENTA}Escolha uma opção: {Cores.RESET}").strip()

        if escolha == '1':
            menu_comandos_termux()
        elif escolha == '2':
            menu_kit_ferramentas()
        elif escolha == '3':
            menu_recursos_adicionais()
        elif escolha == '4':
            exibir_senha_esquecida()
        elif escolha == '0':
            limpar_tela()
            print(f"{Cores.VERDE}Saindo do PAINEL INF3 PRO. Mantenha-se seguro e ético!{Cores.RESET}")
            time.sleep(2)
            break
        else:
            print(f"{Cores.VERMELHO}Opção inválida. Por favor, digite um número válido.{Cores.RESET}")
            pausar()

# --- Execução Principal ---
if __name__ == "__main__":
    menu_principal()
