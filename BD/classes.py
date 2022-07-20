from BD.schema import Conexao
from sqlite3 import Error

class Login:

	def valida_login(login, senha):
		conecta = Conexao()
		conecta.connect()   
		conecta.execute("""SELECT l.idLogin, l.login, l.senha, p.permissao, pe.nomePessoa
			FROM LOGIN l INNER JOIN PESSOA pe 
			ON l.idPessoa = pe.idPessoa
			INNER JOIN PERFIL p ON p.permissao = pe.permissao;""")   
		linhas = conecta.fetchall()
		for x in linhas:
			if x[1] == login and x[2] == senha:
				valid =  True
				id = x[0]
				permissao = x[3]
				nome_usario = x[4]
				break
			else:
				valid = False
				id = None
				permissao = ""
				nome_usario = ""
		
		if permissao == 2:
			conecta.execute(f"""SELECT e.siglaEmpresa
				FROM LOGIN l INNER JOIN PESSOA s ON s.idPessoa = l.idPessoa
				INNER JOIN EMPRESA e ON s.siglaEmpresa = e.siglaEmpresa
				WHERE l.idLogin = {id};""")
			linhas = conecta.fetchall()
			for x in linhas:
				sigla_empresa = x[0]
		else:
			sigla_empresa = ""
		
		return (valid, id, sigla_empresa, nome_usario)
	
	def valida_permissao(id):
		conecta = Conexao()
		conecta.connect()   
		conecta.execute(f"""SELECT p.permissao
			FROM LOGIN l INNER JOIN PESSOA pe ON l.idPessoa = pe.idPessoa 
			INNER JOIN PERFIL p ON p.permissao = pe.permissao
			WHERE idLogin = {id};""")
		linhas = conecta.fetchall()

		return linhas[0]

	def insert_login(login, senha, id_pessoa):
		conecta = Conexao()
		conecta.connect()   
		conecta.execute("INSERT INTO LOGIN (login, senha, idPessoa) VALUES (?,?,?)", (login, senha, id_pessoa))
		conecta.commit()

	def excluir_login(id_pessoa):
		conecta = Conexao()
		conecta.connect()   
		conecta.execute(f"DELETE FROM LOGIN WHERE idPessoa = {id_pessoa};")
		conecta.commit()


class Token:

	def insert_token(token):
		conecta = Conexao()
		conecta.connect()   
		conecta.execute("INSERT INTO TOKEN (token) VALUES (?)", (token,))
		conecta.commit()   

	def valida_token(token):
		conecta = Conexao()
		conecta.connect()   
		conecta.execute("SELECT token FROM TOKEN;")  
		linhas = conecta.fetchall()
		for x in linhas:
			if x[0] == token:
				valid = True
				break
			else: 
				valid = False

		return valid	

	def id_token_colaborador():	
		conecta = Conexao()
		conecta.connect()
		conecta.execute("SELECT idToken FROM TOKEN;")
		linhas_token = conecta.fetchall()
		for x in linhas_token:
			id_token = x[0]
		
		return id_token

	def incrementa_token():
		conecta = Conexao()
		conecta.connect()
		conecta.execute("SELECT token FROM TOKEN;")
		linhas_token = conecta.fetchall()
		for x in linhas_token:
			token = x[0]
		
		token = int(token) + 41	
		Token.insert_token(token)

	def gera_token_colaborador(sigla_empresa):
		num_colab = Pessoa.numero_colab_token(sigla_empresa)
		id_colab = Pessoa.id_num_colab(sigla_empresa)
		for x in range(0, int(num_colab[0])):
			Token.incrementa_token()
			id_token = Token.id_token_colaborador()
			Pessoa.update_token(id_token, id_colab[x][0])
		
	def token_email():
		conecta = Conexao()
		conecta.connect()   
		conecta.execute("SELECT token FROM TOKEN;")  
		linhas = conecta.fetchall()
		for x in linhas:
			token = x[0]

		return token


class Endereco:

	def insert_endereco(estado, cidade, bairro, rua, numero, complemento, cep):
		conecta = Conexao()
		conecta.connect()  
		conecta.execute("""INSERT INTO ENDERECO (estado, cidade, bairro, rua, numero, complemento, cep)
			VALUES (?,?,?,?,?,?,?)""", (estado, cidade, bairro, rua, numero, complemento, cep))
		conecta.commit()

	def id_endereco_empresa():
		conecta = Conexao()
		conecta.connect()  
		conecta.execute("SELECT idEndereco FROM ENDERECO")
		linhas = conecta.fetchall()
		for x in linhas:
			id = x[0]

		return id
	
	def excluir_endereco(id):
		conecta = Conexao()
		conecta.connect()  
		conecta.execute(f"DELETE FROM ENDERECO WHERE idEndereco = {id[0]};")
		conecta.commit()	


class Empresa:

	def insert_empresa(sigla, nome, cnpj, id_endereco):
		conecta = Conexao()
		conecta.connect()
		conecta.execute("""INSERT INTO EMPRESA (siglaEmpresa, nomeEmpresa, cnpj, idEndereco) 
			VALUES (?,?,?,?)""", (sigla, nome, cnpj, id_endereco))
		conecta.commit()
	
	def view_empresa():
		conecta = Conexao()
		conecta.connect()   
		conecta.execute("""SELECT e.siglaEmpresa, e.nomeEmpresa, e.cnpj, ed.estado, ed.cidade, ed.bairro, ed.rua, ed.numero, ed.cep, ed.complemento 
			FROM EMPRESA e inner join ENDERECO ed on e.idEndereco = ed.idEndereco;""")   
		linhas = conecta.fetchall()

		return linhas
	
	def view_empresa_pesquisa(nome_empresa):
		conecta = Conexao()
		conecta.connect()   
		conecta.execute(f"""SELECT e.siglaEmpresa, e.nomeEmpresa, e.cnpj, ed.estado, ed.cidade, ed.bairro, ed.rua, ed.numero, ed.cep, ed.complemento 
			FROM EMPRESA e inner join ENDERECO ed on e.idEndereco = ed.idEndereco WHERE e.nomeEmpresa LIKE '%{nome_empresa}%';""")   
		linhas = conecta.fetchall()

		return linhas
	
	def view_sigla_Empresa():
		conecta = Conexao()
		conecta.connect()   
		conecta.execute("SELECT siglaEmpresa FROM EMPRESA;")
		linhas = conecta.fetchall()

		return linhas
	
	def campos_atualizar(sigla_empresa):
		conecta = Conexao()
		conecta.connect()   
		conecta.execute(f"""SELECT e.siglaEmpresa, e.nomeEmpresa, e.cnpj, ed.estado, ed.cidade, ed.bairro, 
			ed.rua, ed.numero, ed.cep, ed.complemento 
			FROM EMPRESA e inner join ENDERECO ed on e.idEndereco = ed.idEndereco 
			WHERE e.siglaEmpresa = '{sigla_empresa}';""")
		linhas = conecta.fetchall()

		return linhas[0]
	
	def quantidade_de_empresas():
		conecta = Conexao()
		conecta.connect()   
		conecta.execute("SELECT count(siglaEmpresa) FROM EMPRESA;")
		linhas = conecta.fetchall()

		return linhas[0]

	def id_endereco(sigla_empresa):
		conecta = Conexao()
		conecta.connect()   
		conecta.execute(f"SELECT idEndereco FROM EMPRESA WHERE siglaEmpresa = '{sigla_empresa}';")
		linhas = conecta.fetchall()

		return linhas[0]
	
	def excluir_empresas(sigla_empresa):
		id_enderco = Empresa.id_endereco(sigla_empresa)
		conecta = Conexao()
		conecta.connect()   
		conecta.execute(f"DELETE FROM EMPRESA WHERE siglaEmpresa = '{sigla_empresa}';")
		conecta.commit()
		Endereco.excluir_endereco(id_enderco)
		Setor.excluir_setor_empresa(sigla_empresa)
		Pessoa.excluir_pessoa_empresa(sigla_empresa)


class Setor:

	def view_setor(sigla_empresa):
		conecta = Conexao()
		conecta.connect()   
		conecta.execute(f"""SELECT se.siglaSetor, se.nomeSetor, se.localizacao, se.ramal, se.setorPai, se.descricaoSetor 
			FROM SETOR se WHERE se.siglaEmpresa = '{sigla_empresa}';""")
		linhas = conecta.fetchall()

		return linhas
	
	def view_sigla_setor(sigla_empresa):
		conecta = Conexao()
		conecta.connect()   
		conecta.execute(f"SELECT se.siglaSetor FROM SETOR se WHERE se.siglaEmpresa = '{sigla_empresa}';")
		linhas = conecta.fetchall()

		return linhas

	def view_setor_pesquisa(nome_pesquisa, sigla_empresa):
		conecta = Conexao()
		conecta.connect()   
		conecta.execute(f"""SELECT se.siglaSetor, se.nomeSetor, se.localizacao, se.ramal, se.setorPai, se.descricaoSetor
			FROM SETOR se WHERE se.nomeSetor LIKE '%{nome_pesquisa}%' and se.siglaEmpresa = '{sigla_empresa}';""")
		linhas = conecta.fetchall()

		return linhas
	
	def insert_setor(sigla_setor, nome_setor, loc_setor, ramal_setor, setor_pai, desc_setor, sigla_empresa):
		conecta = Conexao()
		conecta.connect()   
		conecta.execute("""INSERT INTO SETOR 
			(siglaSetor, nomeSetor, localizacao, ramal, setorPai, descricaoSetor, siglaEmpresa)
			VALUES (?,?,?,?,?,?,?);""", 
			(sigla_setor, nome_setor, loc_setor, ramal_setor, setor_pai, desc_setor, sigla_empresa))
		conecta.commit()
	
	def campos_atualizar(sigla_setor, sigla_empresa):
		conecta = Conexao()
		conecta.connect()   
		conecta.execute(f"""SELECT nomeSetor, siglaSetor, localizacao, setorPai, ramal, descricaoSetor 
			FROM SETOR WHERE siglaSetor = '{sigla_setor}' and siglaEmpresa = '{sigla_empresa}';""")
		linhas = conecta.fetchall()

		return linhas[0]

	def excluir_setor(sigla_setor):
		conecta = Conexao()
		conecta.connect()   
		conecta.execute(f"DELETE FROM SETOR WHERE siglaSetor = '{sigla_setor}';")
		conecta.commit()

	def excluir_setor_empresa(sigla_empresa):
		conecta = Conexao()
		conecta.connect()   
		conecta.execute(f"DELETE FROM SETOR WHERE siglaEmpresa = '{sigla_empresa}';")
		conecta.commit()
	
	def quantidade_setor_cadastrados(sigla_empresa):
		conecta = Conexao()
		conecta.connect()   
		conecta.execute(f"SELECT count(siglaSetor) FROM SETOR WHERE siglaEmpresa = '{sigla_empresa}';")
		linhas = conecta.fetchall()

		return linhas[0]


class Pessoa():
	
	def insert_pessoa(nome, email, tel, cargo, cpf, validPermisao, siglaStor, siglaEmpresa):
		try:
			conecta = Conexao()
			conecta.connect()
			Token.incrementa_token()
			id_token = Token.id_token_colaborador()
			conecta.execute("""INSERT INTO PESSOA (nomePessoa, email, telefone, cargo, cpf, idToken, permissao, siglaSetor, siglaEmpresa) 
				VALUES (?,?,?,?,?,?,?,?,?);""",(nome, email, tel, cargo, cpf, id_token, validPermisao, siglaStor, siglaEmpresa))
			conecta.commit()
		except:
			return False
		else: 
			return True
	
	def insert_gestor(nome, email, tel, cargo, cpf, validPermisao, siglaStor, siglaEmpresa):
		try:
			conecta = Conexao()
			conecta.connect()
			id_token = ""
			conecta.execute("""INSERT INTO PESSOA (nomePessoa, email, telefone, cargo, cpf, idToken, permissao, siglaSetor, siglaEmpresa) 
				VALUES (?,?,?,?,?,?,?,?,?);""",(nome, email, tel, cargo, cpf, id_token, validPermisao, siglaStor, siglaEmpresa))
			conecta.commit()
		except:
			return False
		else: 
			return True

	def view_pessoa(sigla_empresa):
		conecta = Conexao()
		conecta.connect()
		conecta.execute(f"""SELECT pe.idPessoa, pe.nomePessoa, pe.email, pe.telefone, pe.cargo
			FROM PESSOA pe
			WHERE pe.siglaEmpresa = '{sigla_empresa}' AND pe.permissao != 2;""")    
		linhas = conecta.fetchall()

		return linhas
	
	def id_login():
		conecta = Conexao()
		conecta.connect()
		conecta.execute("SELECT idPessoa FROM PESSOA;")
		linhas = conecta.fetchall()
		for x in linhas:
			id_pessoa = x[0]
		
		return id_pessoa
	
	def view_pessoa_pesquisa(nome_pesquisa, sigla_empresa):
		conecta = Conexao()
		conecta.connect()   
		conecta.execute(f"SELECT idPessoa, nomePessoa, email, telefone, cargo FROM PESSOA WHERE nomePessoa LIKE '%{nome_pesquisa}%' and siglaEmpresa = '{sigla_empresa}';")   
		linhas = conecta.fetchall()

		return linhas
	
	def campos_atulizar(id):
		conecta = Conexao()
		conecta.connect()   
		conecta.execute(f"SELECT nomePessoa, cpf, email, telefone, cargo, siglaSetor FROM PESSOA WHERE idPessoa = {id};")   
		linhas = conecta.fetchall()

		return linhas[0]
	
	def numero_colab_token(sigla_empresa):
		conecta = Conexao()
		conecta.connect()   
		conecta.execute(f"""SELECT count(p.idPessoa) 
			FROM PESSOA p WHERE p.permissao = 3 AND p.siglaEmpresa = '{sigla_empresa}';""")
		linhas = conecta.fetchall()

		return linhas[0]
	
	def id_num_colab(sigla_empresa):
		conecta = Conexao()
		conecta.connect()   
		conecta.execute(f"""SELECT p.idPessoa 
			FROM PESSOA p WHERE p.permissao = 3 AND p.siglaEmpresa = '{sigla_empresa}';""")
		linhas = conecta.fetchall()

		return linhas

	def update_token(id_token, id_pessoa):
		conecta = Conexao()
		conecta.connect()   
		conecta.execute(f"""UPDATE PESSOA SET idToken = {id_token} WHERE idPessoa = {id_pessoa};""")
		conecta.commit()
	
	def veiw_pessoa_gerar_token(sigla_empresa):
		conecta = Conexao()
		conecta.connect()   
		conecta.execute(f"""SELECT pe.nomePessoa, se.nomeSetor,
			tk.token
			FROM PESSOA pe INNER JOIN SETOR se 
			ON pe.siglaSetor = se.siglaSetor
			INNER JOIN TOKEN tk 
			ON pe.idToken = tk.idToken
			WHERE pe.siglaEmpresa = '{sigla_empresa}'
			ORDER BY pe.nomePessoa;""")
		linhas = conecta.fetchall()

		return linhas
	
	def excluir_pessoa(id):
		conecta = Conexao()
		conecta.connect()   
		conecta.execute(f"DELETE FROM PESSOA WHERE idPessoa = {id};")
		conecta.commit()

	def excluir_pessoa_empresa(sigla_empresa):
		id_pessoa = Pessoa.id_gestor(sigla_empresa)
		conecta = Conexao()
		conecta.connect()   
		conecta.execute(f"DELETE FROM PESSOA WHERE siglaEmpresa = '{sigla_empresa}';")
		conecta.commit()
		Login.excluir_login(id_pessoa[0])
	
	def id_gestor(sigla_empresa):
		conecta = Conexao()
		conecta.connect()   
		conecta.execute(f"SELECT idPessoa FROM PESSOA WHERE siglaEmpresa = '{sigla_empresa}' AND permissao = 2;")
		linhas = conecta.fetchall()

		return linhas[0]
	
	def quantidade_pessoas_cadastradas(sigla_empresa):
		conecta = Conexao()
		conecta.connect()   
		conecta.execute(f"SELECT count(idPessoa) FROM PESSOA WHERE siglaEmpresa = '{sigla_empresa}' AND permissao != 2;")
		linhas = conecta.fetchall()

		return linhas[0]


class Resposta:
	def insert_resposta(resposta, id_questao):
		conecta = Conexao()
		conecta.connect()   
		conecta.execute("INSERT INTO RESPOSTA (descricaoResposta, idQuestao) VALUES (?,?);", (resposta, id_questao))
		conecta.commit()
	
	########################################################################################
	#Questão 1 Fase 1
	def view_grafico_quest1_A_fase1():
		conecta = Conexao()
		conecta.connect()   
		conecta.execute("""SELECT count(descricaoResposta) FROM RESPOSTA
			WHERE descricaoResposta = 'Feminino' AND idQuestao = 1;""")
		linhas = conecta.fetchall()

		return linhas[0]

	def view_grafico_quest1_B_fase1():
		conecta = Conexao()
		conecta.connect()   
		conecta.execute("""SELECT count(descricaoResposta) FROM RESPOSTA
			WHERE descricaoResposta = 'Masculino' AND idQuestao = 1;""")
		linhas = conecta.fetchall()

		return linhas[0]
	
	def view_grafico_quest1_C_fase1():
		conecta = Conexao()
		conecta.connect()   
		conecta.execute("""SELECT count(descricaoResposta) FROM RESPOSTA
			WHERE descricaoResposta = 'Outro' AND idQuestao = 1;""")
		linhas = conecta.fetchall()

		return linhas[0]
	########################################################################################

	########################################################################################
	#Questão 2 Fase 1
	def view_grafico_quest2_A_fase1():
		conecta = Conexao()
		conecta.connect()   
		conecta.execute("""SELECT count(descricaoResposta) FROM RESPOSTA
			WHERE descricaoResposta = 'Entre 18 e 24 anos' AND idQuestao = 2;""")
		linhas = conecta.fetchall()

		return linhas[0]

	def view_grafico_quest2_B_fase1():
		conecta = Conexao()
		conecta.connect()   
		conecta.execute("""SELECT count(descricaoResposta) FROM RESPOSTA
			WHERE descricaoResposta = 'Entre 25 e 34 anos' AND idQuestao = 2;""")
		linhas = conecta.fetchall()

		return linhas[0]
	
	def view_grafico_quest2_C_fase1():
		conecta = Conexao()
		conecta.connect()   
		conecta.execute("""SELECT count(descricaoResposta) FROM RESPOSTA
			WHERE descricaoResposta = 'Entre 35 e 44 anos' AND idQuestao = 2;""")
		linhas = conecta.fetchall()

		return linhas[0]
	
	def view_grafico_quest2_D_fase1():
		conecta = Conexao()
		conecta.connect()   
		conecta.execute("""SELECT count(descricaoResposta) FROM RESPOSTA
			WHERE descricaoResposta = '45 anos ou mais' AND idQuestao = 2;""")
		linhas = conecta.fetchall()

		return linhas[0]
	########################################################################################

	########################################################################################
	#Questão 3 Fase 1
	def view_grafico_quest3_A_fase1():
		conecta = Conexao()
		conecta.connect()   
		conecta.execute("""SELECT count(descricaoResposta) FROM RESPOSTA
			WHERE descricaoResposta = 'Solteiro(a)' AND idQuestao = 3;""")
		linhas = conecta.fetchall()

		return linhas[0]

	def view_grafico_quest3_B_fase1():
		conecta = Conexao()
		conecta.connect()   
		conecta.execute("""SELECT count(descricaoResposta) FROM RESPOSTA
			WHERE descricaoResposta = 'Casado(a)' AND idQuestao = 3;""")
		linhas = conecta.fetchall()

		return linhas[0]
	
	def view_grafico_quest3_C_fase1():
		conecta = Conexao()
		conecta.connect()   
		conecta.execute("""SELECT count(descricaoResposta) FROM RESPOSTA
			WHERE descricaoResposta = 'Viúvo(a)' AND idQuestao = 3;""")
		linhas = conecta.fetchall()

		return linhas[0]
	
	def view_grafico_quest3_D_fase1():
		conecta = Conexao()
		conecta.connect()   
		conecta.execute("""SELECT count(descricaoResposta) FROM RESPOSTA
			WHERE descricaoResposta = 'Outro' AND idQuestao = 3;""")
		linhas = conecta.fetchall()

		return linhas[0]
	########################################################################################

	########################################################################################
	#Questão 4 Fase 1
	def view_grafico_quest4_A_fase1():
		conecta = Conexao()
		conecta.connect()   
		conecta.execute("""SELECT count(descricaoResposta) FROM RESPOSTA
			WHERE descricaoResposta = 'Setor A' AND idQuestao = 4;""")
		linhas = conecta.fetchall()

		return linhas[0]

	def view_grafico_quest4_B_fase1():
		conecta = Conexao()
		conecta.connect()   
		conecta.execute("""SELECT count(descricaoResposta) FROM RESPOSTA
			WHERE descricaoResposta = 'Setor B' AND idQuestao = 4;""")
		linhas = conecta.fetchall()

		return linhas[0]
	
	def view_grafico_quest4_C_fase1():
		conecta = Conexao()
		conecta.connect()   
		conecta.execute("""SELECT count(descricaoResposta) FROM RESPOSTA
			WHERE descricaoResposta = 'Setor C' AND idQuestao = 4;""")
		linhas = conecta.fetchall()

		return linhas[0]
	
	def view_grafico_quest4_D_fase1():
		conecta = Conexao()
		conecta.connect()   
		conecta.execute("""SELECT count(descricaoResposta) FROM RESPOSTA
			WHERE descricaoResposta = 'Outro setor' AND idQuestao = 4;""")
		linhas = conecta.fetchall()

		return linhas[0]
	########################################################################################

	########################################################################################
	#Questão 1
	def view_grafico_quest1_A():
		conecta = Conexao()
		conecta.connect()   
		conecta.execute("""SELECT count(descricaoResposta) FROM RESPOSTA
			WHERE descricaoResposta = 'Nunca' AND idQuestao = 5;""")
		linhas = conecta.fetchall()

		return linhas[0]

	def view_grafico_quest1_B():
		conecta = Conexao()
		conecta.connect()   
		conecta.execute("""SELECT count(descricaoResposta) FROM RESPOSTA
			WHERE descricaoResposta = 'Às vezes' AND idQuestao = 5;""")
		linhas = conecta.fetchall()

		return linhas[0]
	
	def view_grafico_quest1_C():
		conecta = Conexao()
		conecta.connect()   
		conecta.execute("""SELECT count(descricaoResposta) FROM RESPOSTA
			WHERE descricaoResposta = 'Diariamente' AND idQuestao = 5;""")
		linhas = conecta.fetchall()

		return linhas[0]
	
	def view_grafico_quest1_D():
		conecta = Conexao()
		conecta.connect()   
		conecta.execute("""SELECT count(descricaoResposta) FROM RESPOSTA
			WHERE descricaoResposta = 'Semanalmente' AND idQuestao = 5;""")
		linhas = conecta.fetchall()

		return linhas[0]
	########################################################################################

	########################################################################################
	#Questão 2
	def view_grafico_quest2_A():
		conecta = Conexao()
		conecta.connect()   
		conecta.execute("""SELECT count(descricaoResposta) FROM RESPOSTA
			WHERE descricaoResposta = 'Nunca' AND idQuestao = 6;""")
		linhas = conecta.fetchall()

		return linhas[0]
	
	def view_grafico_quest2_B():
		conecta = Conexao()
		conecta.connect()   
		conecta.execute("""SELECT count(descricaoResposta) FROM RESPOSTA
			WHERE descricaoResposta = 'Às vezes' AND idQuestao = 6;""")
		linhas = conecta.fetchall()

		return linhas[0]

	def view_grafico_quest2_C():
		conecta = Conexao()
		conecta.connect()   
		conecta.execute("""SELECT count(descricaoResposta) FROM RESPOSTA
			WHERE descricaoResposta = 'Diariamente' AND idQuestao = 6;""")
		linhas = conecta.fetchall()

		return linhas[0]

	def view_grafico_quest2_D():
		conecta = Conexao()
		conecta.connect()   
		conecta.execute("""SELECT count(descricaoResposta) FROM RESPOSTA
			WHERE descricaoResposta = 'Semanalmente' AND idQuestao = 6;""")
		linhas = conecta.fetchall()

		return linhas[0]
	
	########################################################################################
	#Questão 3
	def view_grafico_quest3_A():
		conecta = Conexao()
		conecta.connect()   
		conecta.execute("""SELECT count(descricaoResposta) FROM RESPOSTA
			WHERE descricaoResposta = 'Nunca' AND idQuestao = 7;""")
		linhas = conecta.fetchall()

		return linhas[0]
	
	def view_grafico_quest3_B():
		conecta = Conexao()
		conecta.connect()   
		conecta.execute("""SELECT count(descricaoResposta) FROM RESPOSTA
			WHERE descricaoResposta = 'Às vezes' AND idQuestao = 7;""")
		linhas = conecta.fetchall()

		return linhas[0]

	def view_grafico_quest3_C():
		conecta = Conexao()
		conecta.connect()   
		conecta.execute("""SELECT count(descricaoResposta) FROM RESPOSTA
			WHERE descricaoResposta = 'Diariamente' AND idQuestao = 7;""")
		linhas = conecta.fetchall()

		return linhas[0]

	def view_grafico_quest3_D():
		conecta = Conexao()
		conecta.connect()   
		conecta.execute("""SELECT count(descricaoResposta) FROM RESPOSTA
			WHERE descricaoResposta = 'Semanalmente' AND idQuestao = 7;""")
		linhas = conecta.fetchall()

		return linhas[0]
	
	########################################################################################
	#Questão 4
	def view_grafico_quest4_A():
		conecta = Conexao()
		conecta.connect()   
		conecta.execute("""SELECT count(descricaoResposta) FROM RESPOSTA
			WHERE descricaoResposta = 'Nunca' AND idQuestao = 8;""")
		linhas = conecta.fetchall()

		return linhas[0]
	
	def view_grafico_quest4_B():
		conecta = Conexao()
		conecta.connect()   
		conecta.execute("""SELECT count(descricaoResposta) FROM RESPOSTA
			WHERE descricaoResposta = 'Às vezes' AND idQuestao = 8;""")
		linhas = conecta.fetchall()

		return linhas[0]

	def view_grafico_quest4_C():
		conecta = Conexao()
		conecta.connect()   
		conecta.execute("""SELECT count(descricaoResposta) FROM RESPOSTA
			WHERE descricaoResposta = 'Diariamente' AND idQuestao = 8;""")
		linhas = conecta.fetchall()

		return linhas[0]

	def view_grafico_quest4_D():
		conecta = Conexao()
		conecta.connect()   
		conecta.execute("""SELECT count(descricaoResposta) FROM RESPOSTA
			WHERE descricaoResposta = 'Semanalmente' AND idQuestao = 8;""")
		linhas = conecta.fetchall()

		return linhas[0]

	########################################################################################
	#Questão 5
	def view_grafico_quest5_A():
		conecta = Conexao()
		conecta.connect()   
		conecta.execute("""SELECT count(descricaoResposta) FROM RESPOSTA
			WHERE descricaoResposta = 'Nunca' AND idQuestao = 9;""")
		linhas = conecta.fetchall()

		return linhas[0]
	
	def view_grafico_quest5_B():
		conecta = Conexao()
		conecta.connect()   
		conecta.execute("""SELECT count(descricaoResposta) FROM RESPOSTA
			WHERE descricaoResposta = 'Às vezes' AND idQuestao = 9;""")
		linhas = conecta.fetchall()

		return linhas[0]

	def view_grafico_quest5_C():
		conecta = Conexao()
		conecta.connect()   
		conecta.execute("""SELECT count(descricaoResposta) FROM RESPOSTA
			WHERE descricaoResposta = 'Diariamente' AND idQuestao = 9;""")
		linhas = conecta.fetchall()

		return linhas[0]

	def view_grafico_quest5_D():
		conecta = Conexao()
		conecta.connect()   
		conecta.execute("""SELECT count(descricaoResposta) FROM RESPOSTA
			WHERE descricaoResposta = 'Semanalmente' AND idQuestao = 9;""")
		linhas = conecta.fetchall()

		return linhas[0]

	########################################################################################
	#Questão 6
	def view_grafico_quest6_A():
		conecta = Conexao()
		conecta.connect()   
		conecta.execute("""SELECT count(descricaoResposta) FROM RESPOSTA
			WHERE descricaoResposta = 'Alguns dias' AND idQuestao = 10;""")
		linhas = conecta.fetchall()

		return linhas[0]
	
	def view_grafico_quest6_B():
		conecta = Conexao()
		conecta.connect()   
		conecta.execute("""SELECT count(descricaoResposta) FROM RESPOSTA
			WHERE descricaoResposta = 'Algumas semanas' AND idQuestao = 10;""")
		linhas = conecta.fetchall()

		return linhas[0]

	def view_grafico_quest6_C():
		conecta = Conexao()
		conecta.connect()   
		conecta.execute("""SELECT count(descricaoResposta) FROM RESPOSTA
			WHERE descricaoResposta = 'Alguns meses' AND idQuestao = 10;""")
		linhas = conecta.fetchall()

		return linhas[0]

	def view_grafico_quest6_D():
		conecta = Conexao()
		conecta.connect()   
		conecta.execute("""SELECT count(descricaoResposta) FROM RESPOSTA
			WHERE descricaoResposta = 'Um ano' AND idQuestao = 10;""")
		linhas = conecta.fetchall()

		return linhas[0]

	########################################################################################
	#Questão 8
	def view_grafico_quest8_A():
		conecta = Conexao()
		conecta.connect()   
		conecta.execute("""SELECT count(descricaoResposta) FROM RESPOSTA
			WHERE descricaoResposta = 'Ignoraram o fato' AND idQuestao = 11;""")
		linhas = conecta.fetchall()

		return linhas[0]
	
	def view_grafico_quest8_B():
		conecta = Conexao()
		conecta.connect()   
		conecta.execute("""SELECT count(descricaoResposta) FROM RESPOSTA
			WHERE descricaoResposta = 'Procuraram medir a situação' AND idQuestao = 11;""")
		linhas = conecta.fetchall()

		return linhas[0]

	def view_grafico_quest8_C():
		conecta = Conexao()
		conecta.connect()   
		conecta.execute("""SELECT count(descricaoResposta) FROM RESPOSTA
			WHERE descricaoResposta = 'Puniram o(s) agressor(es)' AND idQuestao = 11;""")
		linhas = conecta.fetchall()

		return linhas[0]

	def view_grafico_quest8_D():
		conecta = Conexao()
		conecta.connect()   
		conecta.execute("""SELECT count(descricaoResposta) FROM RESPOSTA
			WHERE descricaoResposta = 'Puniram você' AND idQuestao = 11;""")
		linhas = conecta.fetchall()

		return linhas[0]
	
	########################################################################################
	#Questão 9
	def view_grafico_quest9_A():
		conecta = Conexao()
		conecta.connect()   
		conecta.execute("""SELECT count(descricaoResposta) FROM RESPOSTA
			WHERE descricaoResposta = 'Sim' AND idQuestao = 12;""")
		linhas = conecta.fetchall()

		return linhas[0]
	
	def view_grafico_quest9_B():
		conecta = Conexao()
		conecta.connect()   
		conecta.execute("""SELECT count(descricaoResposta) FROM RESPOSTA
			WHERE descricaoResposta = 'Não' AND idQuestao = 12;""")
		linhas = conecta.fetchall()

		return linhas[0]
	
	########################################################################################
	#Questão 10
	def view_grafico_quest10_A():
		conecta = Conexao()
		conecta.connect()   
		conecta.execute("""SELECT count(descricaoResposta) FROM RESPOSTA
			WHERE descricaoResposta = 'Desejar melhorias de salário' AND idQuestao = 13;""")
		linhas = conecta.fetchall()

		return linhas[0]
	
	def view_grafico_quest10_B():
		conecta = Conexao()
		conecta.connect()   
		conecta.execute("""SELECT count(descricaoResposta) FROM RESPOSTA
			WHERE descricaoResposta = 'Receio de serem eles também vitimas de perseguição' AND idQuestao = 13;""")
		linhas = conecta.fetchall()

		return linhas[0]

	def view_grafico_quest10_C():
		conecta = Conexao()
		conecta.connect()   
		conecta.execute("""SELECT count(descricaoResposta) FROM RESPOSTA
			WHERE descricaoResposta = 'Estarem do lado do(s) agressor(es)' AND idQuestao = 13;""")
		linhas = conecta.fetchall()

		return linhas[0]

	def view_grafico_quest10_D():
		conecta = Conexao()
		conecta.connect()   
		conecta.execute("""SELECT count(descricaoResposta) FROM RESPOSTA
			WHERE descricaoResposta = 'Outros' AND idQuestao = 13;""")
		linhas = conecta.fetchall()

		return linhas[0]