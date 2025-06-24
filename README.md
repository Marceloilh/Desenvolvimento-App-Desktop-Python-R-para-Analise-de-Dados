Relatório Final do Projeto: Sistema de Análise Preditiva de Diabetes

Resumo do Projeto ("O que foi feito")
O objetivo deste projeto foi desenvolver uma aplicação de ponta a ponta para análises preditivas sobre o risco de diabetes. O projeto evoluiu de um pipeline de scripts simples para um aplicativo de desktop completo com interface gráfica.

O sistema final é um aplicativo robusto que permite a um usuário:

Treinar um modelo de Machine Learning a partir de um conjunto de dados de referência. O modelo treinado é salvo para uso futuro. Realizar dispersão em tempo real de duas formas distintas: Previsão Manual: Inserindo os dados de um único paciente através de campos na interface. Previsão em Lote: Selecionando um arquivo CSV contendo dados de múltiplos pacientes. Visualize os resultados diretamente na interface, incluindo um relatório textual formatado e um gráfico de perfil para análises individuais. Gere relatórios profissionais em PDF, com uma página detalhada para cada paciente analisado em lote, ou um relatório exclusivo para o manual de análise. Ao longo do desenvolvimento, superamos diversos desafios técnicos, incluindo a integração entre linguagens (Python e R), permissões de sistema no Windows, tratamento de dependências de pacotes, codificação de caracteres (UTF-8) e depuração lógica de dados.

Linguagens Utilizadas
Python: Usado como linguagem principal para orquestrar todo o processo, construir uma interface gráfica e gerar os relatórios finais. R: Usada especificamente para a sua especialidade: a análise estatística e o treinamento dos modelos de Machine Learning.

Tecnologias, Bibliotecas e Ferramentas Utilizadas
Em Python:

Interface Gráfica (GUI): CustomTkinter: A biblioteca principal para criar todos os componentes visuais da aplicação (janelas, botões, abas, etc.), conferindo um visual moderno. Tkinter (messagebox, filedialog): Usado para exibir caixas de diálogo de pop-up e para selecionar arquivos. Pillow (PIL): Para manipular e exibir imagens dos gráficos na interface. Processamento de Dados e Banco de Dados: pandas: Para ler e manipular os arquivos CSV de forma eficiente. sqlite3: Para criar e interagir com o banco de dados local onde os dados de treino foram armazenados. Geração de Relatórios: fpdf2: Para criar os relatórios finais em formato PDF, com suporte a fontes customizadas para acentuação. matplotlib: Para gerar os gráficos de perfil dos pacientes na análise por tabela, diretamente do Python. Sistema e Orquestração: subprocesso: Para executar o script R a partir do Python. threading: Para garantir que a interface gráfica não congele durante a execução da análise. pathlib: Para manipulação moderna e segura dos caminhos de arquivos. logging: Para exibir o progresso e os erros em tempo real na interface.

Em R:

Machine Learning e Modelagem: caret: A principal ferramenta para simplificar o processo de treinamento e avaliação dos modelos. randomForest: Para o treinamento do modelo de Random Forest. e1071 / kernlab: Dependências para o treinamento do modelo SVM. caTools: Utilizado para a divisão dos dados em conjuntos de treino e teste. Manipulação de Dados: dplyr: Para operações de seleção e manipulação de dados. Visualização: ggplot2: Para a criação do gráfico de barras do perfil do paciente na análise manual. Ambiente e Outros:

Anaconda / Conda: Utilizado para criar e gerenciar o ambiente virtual (teste), isolando as dependências do projeto. Batch Script (.bat): Criado como uma solução robusta para contornar os problemas de permissão do Windows ao executar o R ​​a partir de um processo Python.

Modelo de Linguagem Utilizado
Gemini, um modelo de linguagem grande desenvolvido pelo Google. O modelo de linguagem participou do projeto como um assistente de programação e destruição ativa, realizando as seguintes tarefas:

Escrita de Código: Geração de scripts completos e trechos de código em Python e R. Depuração (Debugging): Análise de uma vasta gama de erros, desde SyntaxError simples até problemas complexos como ModuleNotFoundError, AttributeError, erros de permissão (Acesso Negado), erros de lógica em R (tipos diferentes de ajuste) e falhas de renderização da GUI. Refatoração e Arquitetura: Sugestão e implementação de melhorias arquitetônicas, como a mudança de CSV para SQLite, a criação de um fluxo de treino/previsão, o uso de threading na GUI e a implementação do workaround com o script .bat. Explicação de Conceitos: Esclarecimento de detalhes sobre ambientes virtuais, dependências, correção de caracteres e lógica por trás dos erros encontrados.
