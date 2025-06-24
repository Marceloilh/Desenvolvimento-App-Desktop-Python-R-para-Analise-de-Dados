

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

class TextboxHandler(logging.Handler):
    def __init__(self, textbox):
        super().__init__()
        self.textbox = textbox

    def emit(self, record):
        msg = self.format(record)
        if self.textbox:
            self.textbox.master.after(0, self.update_textbox, msg)

    def update_textbox(self, msg):
        self.textbox.configure(state="normal")
        if "---" in msg:
             self.textbox.insert("end", msg + "\n", "highlight")
        else:
             self.textbox.insert("end", msg + "\n")
        self.textbox.configure(state="disabled")
        self.textbox.see("end")

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.treino_file_path = None
        self.analise_file_path = None
        self.output_txt_path = Path.cwd() / "resultado_r.txt"
        self.output_png_path = Path.cwd() / "grafico_r.png"
        self.last_run_mode = ""
        
        self.title("Sistema de Análise Preditiva (Versão DEMO)")
        self.geometry("950x800")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1) 

        # UI Frame de Treinamento
        self.treino_frame = customtkinter.CTkFrame(self)
        self.treino_frame.grid(row=0, column=0, padx=20, pady=(20,10), sticky="ew")
        self.treino_frame.grid_columnconfigure(1, weight=1)
        self.lbl_treino = customtkinter.CTkLabel(self.treino_frame, text="TREINAMENTO DO MODELO", font=customtkinter.CTkFont(weight="bold"))
        self.lbl_treino.grid(row=0, column=0, pady=(5,10), padx=10, sticky="w")
        self.credit_label = customtkinter.CTkLabel(self.treino_frame, text="Created by Smd Health serv .LTDA", font=customtkinter.CTkFont(size=9, slant="italic"), text_color="gray")
        self.credit_label.grid(row=0, column=2, padx=10, pady=5, sticky="e")
        self.btn_select_treino = customtkinter.CTkButton(self.treino_frame, text="Selecionar Tabela de Treino", command=self.selecionar_arquivo_treino)
        self.btn_select_treino.grid(row=1, column=0, padx=10, pady=5)
        self.lbl_treino_file = customtkinter.CTkLabel(self.treino_frame, text="Nenhum arquivo", anchor="w")
        self.lbl_treino_file.grid(row=1, column=1, padx=10, sticky="ew")
        self.btn_run_treino = customtkinter.CTkButton(self.treino_frame, text="1. Treinar Modelo", state="disabled", command=lambda: self.iniciar_processo_thread(modo="treinar"))
        self.btn_run_treino.grid(row=1, column=2, padx=10, pady=5)

        # UI Abas
        self.tab_view = customtkinter.CTkTabview(self, anchor="w")
        self.tab_view.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        self.tab_view.add("Previsão Manual de Paciente")
        self.tab_view.add("Previsão de Tabela de Pacientes")
        
        manual_frame = self.tab_view.tab("Previsão Manual de Paciente")
        manual_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        self.entry_widgets = {}
        labels = ['Paciente', 'Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age']
        placeholders = ['Nome Sobrenome', '6', '148', '72', '35', '0', '33.6', '0.627', '50'] 
        for i, label in enumerate(labels):
            row, col = divmod(i, 4)
            lbl = customtkinter.CTkLabel(manual_frame, text=label); lbl.grid(row=row*2, column=col, padx=10, pady=(10, 0), sticky="w")
            entry = customtkinter.CTkEntry(manual_frame, placeholder_text=placeholders[i]); entry.grid(row=row*2+1, column=col, padx=10, pady=(0, 10), sticky="ew")
            self.entry_widgets[label] = entry
        self.btn_run_manual = customtkinter.CTkButton(manual_frame, text="2. Fazer Previsão Manual", state="disabled", command=lambda: self.iniciar_processo_thread(modo="prever_manual"))
        self.btn_run_manual.grid(row=6, column=0, columnspan=4, padx=10, pady=20, sticky="ew")

        tabela_frame = self.tab_view.tab("Previsão de Tabela de Pacientes")
        tabela_frame.grid_columnconfigure(1, weight=1)
        self.btn_select_analise = customtkinter.CTkButton(tabela_frame, text="Selecionar Tabela (Análise)", command=self.selecionar_arquivo_analise, state="disabled")
        self.btn_select_analise.grid(row=0, column=0, padx=20, pady=20)
        self.lbl_analise_file = customtkinter.CTkLabel(tabela_frame, text="Aguardando treinamento...", anchor="w")
        self.lbl_analise_file.grid(row=0, column=1, padx=20, pady=20, sticky="ew")
        self.btn_run_tabela = customtkinter.CTkButton(tabela_frame, text="2. Fazer Previsão da Tabela", state="disabled", command=lambda: self.iniciar_processo_thread(modo="prever_tabela"))
        self.btn_run_tabela.grid(row=0, column=2, padx=20, pady=20)
        
        # UI Widgets Inferiores
        self.progressbar = customtkinter.CTkProgressBar(self)
        self.progressbar.grid(row=2, column=0, padx=20, pady=5, sticky="ew")
        self.progressbar.set(0)
        self.bottom_frame = customtkinter.CTkFrame(self)
        self.bottom_frame.grid(row=3, column=0, padx=20, pady=(0, 20), sticky="nsew")
        self.bottom_frame.grid_columnconfigure(0, weight=1)
        self.bottom_frame.grid_rowconfigure(0, weight=1)
        self.preview_tabs = customtkinter.CTkTabview(self.bottom_frame)
        self.preview_tabs.pack(expand=True, fill="both")
        self.preview_tabs.add("Logs do Processo")
        self.preview_tabs.add("Preview do Relatório")
        self.log_textbox = customtkinter.CTkTextbox(self.preview_tabs.tab("Logs do Processo"))
        self.log_textbox.pack(expand=True, fill="both")
        self.log_textbox.configure(state="disabled")
        self.log_textbox.tag_config("highlight", foreground="#0077B3", underline=True)
        self.preview_scroll_frame = customtkinter.CTkScrollableFrame(self.preview_tabs.tab("Preview do Relatório"), label_text="Visualização Prévia")
        self.preview_scroll_frame.pack(expand=True, fill="both")
        self.preview_label_texto = customtkinter.CTkLabel(self.preview_scroll_frame, text="Aguardando análise...", anchor="w", justify="left")
        self.preview_label_texto.pack(pady=10, expand=True, fill="x")
        self.preview_label_grafico = customtkinter.CTkLabel(self.preview_scroll_frame, text="")
        self.preview_label_grafico.pack(pady=10)
        self.pdf_button = customtkinter.CTkButton(self.bottom_frame, text="Gerar PDF do Relatório Acima", command=self.gerar_pdf, state="disabled")
        self.pdf_button.pack(pady=10)
        
        # Configuração do Logger
        self.log_handler = TextboxHandler(self.log_textbox)
        formatter = logging.Formatter('%(asctime)s - %(message)s', datefmt='%H:%M:%S')
        self.log_handler.setFormatter(formatter)
        logging.getLogger().handlers = []; logging.getLogger().addHandler(self.log_handler); logging.getLogger().setLevel(logging.INFO)
        logging.info("Aplicação iniciada.")

    def selecionar_arquivo_treino(self):
        filepath = customtkinter.filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if filepath:
            self.treino_file_path = Path(filepath)
            self.lbl_treino_file.configure(text=self.treino_file_path.name)
            self.btn_run_treino.configure(state="normal")
    
    def selecionar_arquivo_analise(self):
        filepath = customtkinter.filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if filepath:
            self.analise_file_path = Path(filepath)
            self.lbl_analise_file.configure(text=self.analise_file_path.name)
            self.btn_run_tabela.configure(state="normal")
            
    def iniciar_processo_thread(self, modo):
        self.log_textbox.configure(state="normal"); self.log_textbox.delete("1.0", "end"); self.log_textbox.configure(state="disabled")
        self.btn_run_treino.configure(state="disabled"); self.btn_run_manual.configure(state="disabled"); self.btn_run_tabela.configure(state="disabled"); self.pdf_button.configure(state="disabled")
        self.progressbar.configure(mode="indeterminate"); self.progressbar.start()
        thread = threading.Thread(target=self.executar_processo_r, args=(modo,)); thread.start()

    def executar_processo_r(self, modo):
        self.last_run_mode = modo 
        try:
            base_dir = Path.cwd(); args_para_r = [modo]
            # ... (Lógica de argumentos do R mantida) ...
            if modo == "treinar":
                if not self.treino_file_path: raise ValueError("Arquivo de treino não selecionado.")
                args_para_r.append(str(self.treino_file_path))
            elif modo == "prever_tabela":
                if not self.analise_file_path: raise ValueError("Arquivo de análise não selecionado.")
                args_para_r.append(str(self.analise_file_path))
            elif modo == "prever_manual":
                labels = ['Paciente', 'Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age']
                dados_manuais = [self.entry_widgets[label].get() for label in labels]
                if any(val == "" for val in dados_manuais): raise ValueError("Todos os campos devem ser preenchidos.")
                args_para_r.extend(dados_manuais)
            args_para_r.append(str(self.output_txt_path)); args_para_r.append(str(self.output_png_path))
            
            # Execução do processo R
            caminho_r_executavel = "C:\\Program Files\\R\\R-4.5.0\\bin\\Rscript.exe"
            script_r = base_dir / "analise_diabetes_script.R"
            comando_completo = f'"{caminho_r_executavel}" "{script_r}"' + " " + " ".join([f'"{arg}"' for arg in args_para_r])
            conteudo_bat = f'@echo OFF\nchcp 65001 > NUL\n{comando_completo}'
            with open('executar_r_generico.bat', 'w', encoding='utf-8') as f: f.write(conteudo_bat)
            
            logging.info(f"Executando R no modo '{modo}'...")
            resultado = subprocess.run(['executar_r_generico.bat'], capture_output=True, text=True, encoding='utf-8', check=True, shell=True)
            
            if resultado.stdout:
                for linha in resultado.stdout.splitlines():
                    if "PYTHON_METRIC:" in linha: logging.info(f"--- {linha.split('PYTHON_METRIC:')[1].strip()} ---")
                    elif "R_LOG:" in linha: logging.info(linha.split("R_LOG:")[1].strip())
            
            self.preparar_preview()

        except subprocess.CalledProcessError as e:
            logging.error(f"FALHA NO SCRIPT R: {e.stderr}"); messagebox.showerror("Erro no Script R", f"Ocorreu um erro na execução do R.\n\nVerifique os logs para detalhes.")
        except Exception as e:
            logging.error(f"FALHA NO PYTHON: {traceback.format_exc()}"); messagebox.showerror("Erro no Aplicativo", f"Ocorreu uma falha no aplicativo.\n\nVerifique os logs para detalhes.")
        finally:
            self.after(100, self.atualizar_ui_final)

    def atualizar_ui_final(self):
        """Função dedicada a reabilitar todos os botões e parar a barra de progresso de forma segura."""
        self.progressbar.stop()
        self.progressbar.set(0)
        self.btn_run_treino.configure(state="normal" if self.treino_file_path else "disabled")
        
        if Path("modelo_rf.rds").exists():
             self.btn_run_manual.configure(state="normal")
             self.btn_run_tabela.configure(state="normal" if self.analise_file_path else "disabled")
             self.btn_select_analise.configure(state="normal")
             self.lbl_analise_file.configure(text=self.analise_file_path.name if self.analise_file_path else "Selecione um arquivo...")
        
        # --- AJUSTE FINAL AQUI ---
        # A lógica para habilitar o botão de PDF agora também está nesta função segura.
        self.pdf_button.configure(state="normal" if self.output_txt_path.exists() else "disabled")
        
        logging.info("Interface atualizada e pronta para a próxima ação.")

    def preparar_preview(self):
        """Prepara a área de visualização, mas NÃO mexe mais no estado do botão de PDF."""
        try:
            self.preview_label_texto.configure(text=""); self.preview_label_grafico.configure(image=None, text="")
            if self.output_txt_path.exists():
                with open(self.output_txt_path, 'r', encoding='utf-8') as f: texto_resultado = f.read()
                self.preview_label_texto.configure(text=texto_resultado)
            if self.output_png_path.exists() and (self.last_run_mode in ['prever_manual', 'treinar']):
                imagem_ctk = customtkinter.CTkImage(light_image=Image.open(self.output_png_path), size=(600, 400))
                self.preview_label_grafico.configure(image=imagem_ctk)
            
      
            
            self.preview_tabs.set("Preview do Relatório")
        except Exception as e:
            logging.error(f"Erro ao carregar o preview: {traceback.format_exc()}"); messagebox.showerror("Erro de Preview", f"Não foi possível carregar os resultados.\n\nVerifique os logs.")
            
    def gerar_pdf(self):
        pdf_path = customtkinter.filedialog.asksaveasfilename(title="Salvar Relatório PDF como...", defaultextension=".pdf", filetypes=(("Arquivos PDF", "*.pdf"),))
        if not pdf_path: return
        try:
            if self.last_run_mode == "prever_manual": self.criar_pdf_manual(Path(pdf_path))
            elif self.last_run_mode == "prever_tabela": self.criar_pdf_tabela(Path(pdf_path))
            else: self.criar_pdf_simples(Path(pdf_path))
        except Exception as e:
            logging.error(f"FALHA CRÍTICA AO GERAR PDF: {traceback.format_exc()}"); messagebox.showerror("Erro ao Gerar PDF", f"Não foi possível gerar o PDF.\n\nConsulte os logs para o erro técnico.")

    def criar_pdf_tabela(self, caminho_saida_pdf):
        
        try:
            df_entrada = pd.read_csv(self.analise_file_path, header=0, dtype=str)
            df_resultado = pd.read_csv("resultado_previsao.csv", header=0)
            nome_coluna_paciente_entrada = df_entrada.columns[0]
            df_completo = pd.merge(df_entrada, df_resultado, left_on=nome_coluna_paciente_entrada, right_on='Nome_do_Paciente')
            if df_completo.empty: messagebox.showerror("Erro de Dados", "Nenhum paciente correspondeu. O PDF não será gerado."); return
            pdf = FPDF(); font_path = Path("fonts") / 'DejaVuSans.ttf'; font_path_bold = Path("fonts") / 'DejaVuSans-Bold.ttf'
            try: matplotlib_font_properties = FontProperties(fname=str(font_path)) if font_path.is_file() else FontProperties()
            except Exception: matplotlib_font_properties = FontProperties()
            try:
                pdf.add_font('DejaVu', '', str(font_path), uni=True)
                pdf.add_font('DejaVu', 'B', str(font_path_bold), uni=True)
                set_font = lambda style, size: pdf.set_font('DejaVu', style, size)
            except RuntimeError:
                pdf.set_font('Arial', 'B', 16)
                set_font = lambda style, size: pdf.set_font('Arial', style, size)
            colunas_preditoras_esperadas = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age']
            grafico_temp_path = Path.cwd() / "temp_grafico_paciente.png"
            for index, row in df_completo.iterrows():
                pdf.add_page()
                set_font('B', 16); pdf.cell(0, 10, "Avaliação dos Exames", ln=True, align='C'); pdf.ln(10)
                set_font('', 12); pdf.cell(0, 8, f"Paciente: {row['Nome_do_Paciente']}     Data: {datetime.now().strftime('%d/%m/%Y')}", ln=True); pdf.ln(4)
                set_font('', 11); colunas_existentes_no_arquivo = [col for col in colunas_preditoras_esperadas if col in row.index]
                for col_name in colunas_existentes_no_arquivo: pdf.cell(0, 7, f"  {col_name}: {row.get(col_name, 'N/D')}", ln=True)
                pdf.ln(4); pdf.cell(0, 8, "-"*80, ln=True)
                set_font('B', 14); pdf.cell(0, 8, f"Resultado: {row['Diagnostico_Predito']}", ln=True); pdf.ln(10)
                if colunas_existentes_no_arquivo:
                    valores_numericos = pd.to_numeric(row[colunas_existentes_no_arquivo], errors='coerce').fillna(0)
                    plt.figure(figsize=(10, 6)); ax = valores_numericos.plot(kind='bar', color='#0072B2')
                    ax.set_ylabel('Valor Registrado', fontproperties=matplotlib_font_properties)
                    ax.set_title(f'Perfil do Paciente: {row["Nome_do_Paciente"]}', fontproperties=matplotlib_font_properties)
                    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", fontproperties=matplotlib_font_properties)
                    plt.tight_layout(); plt.savefig(grafico_temp_path); plt.close()
                    pdf.image(str(grafico_temp_path), x=None, y=None, w=190)
                else: set_font('', 10); pdf.cell(0, 10, "Nenhum dado numérico disponível para o gráfico.", ln=True, align='C')
            pdf.output(str(caminho_saida_pdf));
            if grafico_temp_path.exists(): os.remove(grafico_temp_path)
            messagebox.showinfo("Sucesso", f"Relatório com {len(df_completo)} páginas salvo em:\n{caminho_saida_pdf}")
        except Exception as e:
            logging.error(f"FALHA CRÍTICA AO GERAR PDF: {traceback.format_exc()}"); messagebox.showerror("Erro ao Gerar PDF", f"Não foi possível gerar o PDF.\n\nConsulte os logs para o erro técnico.")

    def criar_pdf_manual(self, caminho_saida_pdf): pass
    def criar_pdf_simples(self, caminho_saida_pdf): pass
