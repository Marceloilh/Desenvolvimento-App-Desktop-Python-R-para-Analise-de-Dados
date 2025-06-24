Relatório Final do Projeto: Sistema de Análise Preditiva de Diabetes

1. Resumo do Projeto ("O que foi feito")

O objetivo deste projeto foi desenvolver uma aplicação de ponta a ponta para realizar análises preditivas sobre o risco de diabetes. O projeto evoluiu de um simples pipeline de scripts para um aplicativo de desktop completo com interface gráfica.

O sistema final é um aplicativo robusto que permite a um usuário:

Treinar um modelo de Machine Learning a partir de um conjunto de dados de referência. O modelo treinado é salvo para uso futuro.
Realizar previsões em tempo real de duas formas distintas:
Previsão Manual: Inserindo os dados de um único paciente através de campos na interface.
Previsão em Lote: Selecionando um arquivo CSV contendo dados de múltiplos pacientes.
Visualizar os resultados diretamente na interface, incluindo um relatório textual formatado e um gráfico de perfil para análises individuais.
Gerar relatórios profissionais em PDF, com uma página detalhada para cada paciente analisado em lote, ou um relatório único para a análise manual.
Ao longo do desenvolvimento, superamos diversos desafios técnicos, incluindo a integração entre linguagens (Python e R), permissões de sistema no Windows, tratamento de dependências de pacotes, codificação de caracteres (UTF-8) e depuração de lógica de dados.

2. Linguagens Utilizadas

Python: Usada como a linguagem principal para orquestrar todo o processo, construir a interface gráfica e gerar os relatórios finais.
R: Usada especificamente para a sua especialidade: a análise estatística e o treinamento dos modelos de Machine Learning.

3. Tecnologias, Bibliotecas e Ferramentas Utilizadas

Em Python:

Interface Gráfica (GUI):
CustomTkinter: A biblioteca principal para criar todos os componentes visuais da aplicação (janelas, botões, abas, etc.), conferindo um visual moderno.
Tkinter (messagebox, filedialog): Usada para exibir caixas de diálogo de pop-up e para selecionar arquivos.
Pillow (PIL): Para manipular e exibir as imagens dos gráficos na interface.
Processamento de Dados e Banco de Dados:
pandas: Para ler e manipular os arquivos CSV de forma eficiente.
sqlite3: Para criar e interagir com o banco de dados local onde os dados de treino foram armazenados.
Geração de Relatórios:
fpdf2: Para criar os relatórios finais em formato PDF, com suporte a fontes customizadas para acentuação.
matplotlib: Para gerar os gráficos de perfil dos pacientes na análise por tabela, diretamente do Python.
Sistema e Orquestração:
subprocess: Para executar o script R a partir do Python.
threading: Para garantir que a interface gráfica não congele durante a execução da análise.
pathlib: Para manipulação moderna e segura dos caminhos de arquivos.
logging: Para exibir o progresso e os erros em tempo real na interface.

Em R:

Machine Learning e Modelagem:
caret: A principal ferramenta para simplificar o processo de treinamento e avaliação dos modelos.
randomForest: Para o treinamento do modelo de Random Forest.
e1071 / kernlab: Dependências para o treinamento do modelo SVM.
caTools: Utilizado para a divisão dos dados em conjuntos de treino e teste.
Manipulação de Dados:
dplyr: Para operações de seleção e manipulação de dados.
Visualização:
ggplot2: Para a criação do gráfico de barras do perfil do paciente na análise manual.
Ambiente e Outros:

Anaconda / Conda: Utilizado para criar e gerenciar o ambiente virtual (teste), isolando as dependências do projeto.
Batch Script (.bat): Criado como uma solução robusta para contornar os problemas de permissão do Windows ao executar o R a partir de um processo Python.

4. Modelo de Linguagem Utilizado

 Gemini, um modelo de linguagem grande desenvolvido pelo Google. O modelo de linguagem participou do projeto como um assistente de programação e depuração ativo, realizando as seguintes tarefas:

Escrita de Código: Geração de scripts completos e trechos de código em Python e R.
Depuração (Debugging): Análise de uma vasta gama de erros, desde SyntaxError simples até problemas complexos como ModuleNotFoundError, AttributeError, erros de permissão (Acesso Negado), erros de lógica em R (tipos diferentes do ajuste) e falhas de renderização da GUI.
Refatoração e Arquitetura: Sugestão e implementação de melhorias arquitetônicas, como a mudança de CSV para SQLite, a criação de um fluxo de treino/previsão, o uso de threading na GUI e a implementação do workaround com o script .bat.
Explicação de Conceitos: Clarificação de tópicos como ambientes virtuais, dependências, codificação de caracteres e a lógica por trás dos erros encontrados.
