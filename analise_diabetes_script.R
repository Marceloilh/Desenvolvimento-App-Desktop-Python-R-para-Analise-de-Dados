# analise_diabetes_script.R




args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 4) { stop("Uso incorreto.") }

modo <- args[1]
path_saida_texto <- args[length(args) - 1]
path_saida_grafico <- args[length(args)]
path_modelo_rf <- "modelo_rf.rds"

# ===================================================================
# MODO TREINAR
# ===================================================================
if (modo == "treinar") {
  path_dados_entrada <- args[2]
  cat("R_LOG: Iniciando MODO TREINAR.\n")
  col_names <- c('Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age', 'Outcome')
  dados_treino_brutos <- read.csv(file = path_dados_entrada, header = FALSE, col.names = col_names)
  colunas_para_limpar <- c("Glucose", "BloodPressure", "SkinThickness", "Insulin", "BMI")
  dados_com_na <- dados_treino_brutos
  dados_com_na[colunas_para_limpar] <- lapply(dados_com_na[colunas_para_limpar], function(x) ifelse(x == 0, NA, x))
  dados_treino_limpos <- na.omit(dados_com_na)
  dados_treino_limpos$Outcome <- factor(dados_treino_limpos$Outcome, levels = c(0, 1), labels = c("Negativo", "Positivo"))
  predictor_names <- setdiff(names(dados_treino_limpos), "Outcome")
  dados_treino_limpos[predictor_names] <- lapply(dados_treino_limpos[predictor_names], as.numeric)

 
  fitControl <- trainControl(method = "cv", number = 5) # 5-fold Cross-Validation

  tuneGrid_rf <- expand.grid(.mtry = c(2))
  modelo_rf <- train(Outcome ~ ., data = dados_treino_limpos, method = "rf", trControl = fitControl, tuneGrid = tuneGrid_rf, na.action = na.omit)
  saveRDS(modelo_rf, file = path_modelo_rf)
  texto_saida <- c("=== Relatório de Treinamento ===","","Modelo treinado com sucesso.","","Pronto para previsões.")
  
  png(filename = path_saida_grafico, width = 800, height = 600, bg = "white") 
  plot(varImp(modelo_rf), main="Importância das Variáveis no Modelo")
  dev.off()
  
  acuracia <- max(modelo_rf$results$Accuracy) # Agora 'max' é usado para pegar o melhor resultado da CV
  cat(paste0("PYTHON_METRIC:Precisão do Modelo (Acurácia): ", round(acuracia * 100, 2), "%\n"))
  
  cat("R_LOG: MODO TREINAR concluído.\n")
}

# ===================================================================
# MODO PREVER (TABELA)
# ===================================================================
if (modo == "prever_tabela") {
    path_dados_entrada <- args[2]
    cat("R_LOG: Iniciando MODO PREVER (TABELA).\n")
    if (!file.exists(path_modelo_rf)) { stop("ERRO: Modelo não encontrado. Treine primeiro.") }
    modelo_rf <- readRDS(path_modelo_rf)
    dados_analise_brutos <- read.csv(file = path_dados_entrada, header = TRUE, stringsAsFactors = FALSE)
    
    nomes_pacientes <- dados_analise_brutos[[1]]
    colunas_do_modelo <- all.vars(formula(modelo_rf)[-2])
    dados_para_prever <- dados_analise_brutos %>% select(all_of(colunas_do_modelo))
    dados_para_prever[] <- lapply(dados_para_prever, as.numeric)
    predicoes <- predict(modelo_rf, newdata = dados_para_prever)
    resultado_final_df <- data.frame(Nome_do_Paciente = nomes_pacientes, Diagnostico_Predito = predicoes)
    write.csv(resultado_final_df, "resultado_previsao.csv", row.names = FALSE, quote = TRUE)

    texto_saida <- c("=== Resultado da Análise (Tabela) ===", "", paste("Arquivo de análise:", basename(path_dados_entrada)), "", "Gere o PDF para um relatório detalhado por paciente.")
    resultados_texto <- capture.output(print(resultado_final_df, row.names=FALSE))
    texto_saida <- c(texto_saida, resultados_texto)
    cat("R_LOG: MODO PREVER (TABELA) concluído.\n")
}

# ===================================================================
# MODO PREVER (MANUAL)
# ===================================================================
if (modo == "prever_manual") {
  cat("R_LOG: Iniciando MODO PREVER (MANUAL).\n")
  if (!file.exists(path_modelo_rf)) { stop("ERRO: Modelo não encontrado. Treine primeiro.") }
  modelo_rf <- readRDS(path_modelo_rf)
  nome_paciente <- args[2]
  valores_preditores <- as.numeric(args[3:10])
  colunas_do_modelo <- all.vars(formula(modelo_rf)[-2])
  dados_para_prever <- as.data.frame(matrix(valores_preditores, nrow = 1))
  names(dados_para_prever) <- colunas_do_modelo
  predicao <- predict(modelo_rf, newdata = dados_para_prever)
  texto_saida <- c(
    "Avaliação dos Exames", "",
    paste("Paciente: ", nome_paciente, "     Data: ", format(Sys.Date(), "%d/%m/%Y")),
    "---------------------------------", "Dados:", ""
  )
  for(i in 1:length(colunas_do_modelo)){
      texto_saida <- c(texto_saida, paste(format(colunas_do_modelo[i], width=25), "=", dados_para_prever[[i]]))
  }
  texto_saida <- c(texto_saida, "", "---------------------------------", paste("Resultado: ", as.character(predicao)))
  dados_grafico <- data.frame(
      Caracteristica = factor(names(dados_para_prever), levels = names(dados_para_prever)),
      Valor = valores_preditores
  )
  grafico <- ggplot(dados_grafico, aes(x = Caracteristica, y = Valor)) +
    geom_bar(stat = "identity", fill = "#0072B2", width=0.6) +
    theme_minimal(base_size = 14) +
    theme(axis.text.x = element_text(angle = 45, hjust = 1)) +
    labs(title = paste("Perfil do Paciente:", nome_paciente), x = "Característica", y = "Valor Registrado")
  ggsave(path_saida_grafico, plot = grafico, width = 10, height = 6, dpi = 100)
  cat("R_LOG: MODO PREVER (MANUAL) concluído.\n")
}

# --- Escrever o resultado no arquivo de texto de saída ---
con_out <- file(path_saida_texto, open = "w", encoding = "UTF-8")
......continue(- -)