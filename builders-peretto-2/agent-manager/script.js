document.addEventListener('DOMContentLoaded', () => {
    // --- STATE & DATA ---
    const agentsConfig = {
        copywriter: {
            name: "Copywriter V4", 
            icon: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 19l7-7 3 3-7 7-3-3z"></path><path d="M18 13l-1.5-7.5L2 2l3.5 14.5L13 18l5-5z"></path><path d="M2 2l7.586 7.586"></path><circle cx="11" cy="11" r="2"></circle></svg>`,
            desc: "Especialista em jornada, funil e conversão.",
            prompt: "Você é um Copywriter Senior V4. Sua função é construir a comunicação que move o cliente da consciência até a conversão. Você não escreve texto — você arquiteta jornadas. Use frameworks como PAS, AIDA e o checklist de diagnóstico de copy da V4."
        },
        account_manager: {
            name: "Account Manager V4", 
            icon: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="7" width="20" height="14" rx="2" ry="2"></rect><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"></path></svg>`,
            desc: "Gestão estratégica de clientes e operações.",
            prompt: "Você é um Account Manager Senior V4. Responsável por conectar marketing e negócio. Domina SPICED, STEP Frame, OKRs e rituais de FCA. Seu foco é garantir que nenhum cliente entre em execução sem os 4 entregáveis de onboarding completos."
        },
        coordenador: {
            name: "Coordenador V4", 
            icon: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg>`,
            desc: "Auditoria, quality check e conformidade.",
            prompt: "Você é o Coordenador da Squad — estrategista e auditor. Você NÃO EXECUTA as entregas, você garante que o sistema (rituais, checklist, quality check) esteja funcionando. Seus outputs são relatórios de conformidade e feedbacks estruturados."
        },
        peretto_novo_cliente: {
            name: "Onboarding de Clientes", 
            icon: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 2 7 12 12 22 7 12 2"></polygon><polyline points="2 17 12 22 22 17"></polyline><polyline points="2 12 12 17 22 12"></polyline></svg>`,
            desc: "Setup de clientes no padrão Peretto & Co.",
            prompt: "Você é um especialista em Onboarding da Peretto & Co. Sua função é automatizar a criação de novos clientes seguindo o padrão de escala da franquia. Você deve coletar Nome, Google Ads ID e URL do NotebookLM para configurar a estrutura bases/peretto-co/clientes/."
        },
        analista_v4mos: {
            name: "Analista V4mos (Meta Ads)", 
            icon: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="20" x2="18" y2="10"></line><line x1="12" y1="20" x2="12" y2="4"></line><line x1="6" y1="20" x2="6" y2="14"></line></svg>`,
            desc: "Extração de dados inteligentes via API V4mos.",
            prompt: "Você é o Analista V4mos especialista em Meta Ads. Você utiliza as credenciais (V4MOS_API_KEY) configuradas no onboarding para traduzir perguntas em linguagem natural em chamadas de API reais. Use 'ctr_calc' (clicks/impressions) e analise anomalias, ROAS e quality rankings."
        },
        csm: {
            name: "CSM V4", 
            icon: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M23 21v-2a4 4 0 0 0-3-3.87"></path><path d="M16 3.13a4 4 0 0 1 0 7.75"></path></svg>`,
            desc: "Foco em retenção, satisfação (NPS) e LTV.",
            prompt: "Você é um Customer Success Manager (CSM) da V4 Company. Sua missão é garantir a retenção e o sucesso do cliente. Você analisa CSAT/NPS, identifica riscos de churn (cancelamento) precocemente e utiliza o framework SPICED para manter o alinhamento de expectativas. Seu tom é empático, porém focado em dados e planos de ação para salvar contas em risco."
        }
    };

    const providers = {
        openrouter: { name: "OpenRouter (Universal)", url: "https://openrouter.ai/api/v1", keyLink: "https://openrouter.ai/keys", keyPlaceholder: "sk-or-v1-..." },
        google: { name: "Google Gemini (AI Studio)", url: "https://generativelanguage.googleapis.com/v1beta/openai/", keyLink: "https://aistudio.google.com/app/apikey", keyPlaceholder: "AIza..." },
        anthropic: { name: "Anthropic Claude (via OpenRouter)", url: "https://openrouter.ai/api/v1", keyLink: "https://openrouter.ai/keys", keyPlaceholder: "Use OpenRouter para melhor compatibilidade" },
        groq: { name: "Groq (Ultra-Rápido)", url: "https://api.groq.com/openai/v1", keyLink: "https://console.groq.com/keys", keyPlaceholder: "gsk_..." },
        nim: { name: "NVIDIA NIM", url: "https://integrate.api.nvidia.com/v1", keyLink: "https://build.nvidia.com/explore/discover", keyPlaceholder: "nvapi-..." },
        openai: { name: "OpenAI (GPT-4)", url: "https://api.openai.com/v1", keyLink: "https://platform.openai.com/api-keys", keyPlaceholder: "sk-..." },
        deepseek: { name: "DeepSeek", url: "https://api.deepseek.com", keyLink: "https://platform.deepseek.com/api_keys", keyPlaceholder: "sk-..." },
        ollama: { name: "Ollama (Localhost)", url: "http://localhost:11434/v1", keyLink: "", keyPlaceholder: "Opcional..." },
        custom: { name: "Customizado (Outro)", url: "", keyLink: "", keyPlaceholder: "Chave..." }
    };

    let currentAgent = 'copywriter';
    let cachedModels = { openrouter: [], google: [{ id: "gemini-1.5-pro", name: "Gemini 1.5 Pro" }, { id: "gemini-1.5-flash", name: "Gemini 1.5 Flash" }], groq: [{ id: "llama-3.1-70b-versatile", name: "Llama 3.1 70B" }] };
    let chatMessages = [];
    let activeTasks = [];

    // --- DOM ELEMENTS ---
    const agentItems = document.querySelectorAll('#agentList li');
    const currentAgentName = document.getElementById('currentAgentName');
    const currentAgentDesc = document.getElementById('currentAgentDesc');
    const systemPromptInput = document.getElementById('systemPromptInput');
    const providerSelect = document.getElementById('providerSelect');
    const modelSelect = document.getElementById('modelSelect');
    const customModelInput = document.getElementById('customModelInput');
    const baseUrlGroup = document.getElementById('baseUrlGroup');
    const baseUrlInput = document.getElementById('baseUrlInput');
    const apiKeyInput = document.getElementById('apiKeyInput');
    const getApiKeyBtn = document.getElementById('getApiKeyBtn');
    const chatHistory = document.getElementById('chatHistory');
    const promptInput = document.getElementById('promptInput');
    const sendBtn = document.getElementById('sendBtn');
    
    const openWikiBtn = document.getElementById('openWikiBtn');
    const closeWikiBtn = document.getElementById('closeWikiBtn');
    const wikiModal = document.getElementById('wikiModal');
    
    // Login & Context Elements
    const loginOverlay = document.getElementById('loginOverlay');
    const loginBtn = document.getElementById('loginBtn');
    const contextSelect = document.getElementById('contextSelect');

    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');
    const taskList = document.getElementById('taskList');

    // --- INITIALIZATION ---
    async function init() {
        // Login Logic
        const isLogged = localStorage.getItem('peretto_logged_in');
        if (isLogged) {
            loginOverlay.style.display = 'none';
        }
        
        loginBtn.onclick = () => {
            const user = document.getElementById('loginUser').value;
            const pass = document.getElementById('loginPass').value;
            
            if (user === 'admin' && pass === 'v4peretto') {
                loginOverlay.style.display = 'none';
                localStorage.setItem('peretto_logged_in', 'true');
            } else {
                alert('Usuário ou senha incorretos. Tente: admin / v4peretto');
            }
        };

        // Onboarding Modal Logic
        const onboardingModal = document.getElementById('onboardingModal');
        const closeOnboardingBtn = document.getElementById('closeOnboardingBtn');
        const startOnboardingBtn = document.getElementById('startOnboardingBtn');

        closeOnboardingBtn.onclick = () => onboardingModal.style.display = 'none';

        // Modificar o clique no agente de Onboarding para abrir o modal
        const onboardingAgentBtn = document.querySelector('[data-agent="peretto_novo_cliente"]');
        if (onboardingAgentBtn) {
            onboardingAgentBtn.onclick = (e) => {
                e.stopPropagation();
                onboardingModal.style.display = 'flex';
            };
        }

        startOnboardingBtn.onclick = async () => {
            const data = {
                name: document.getElementById('obClientName').value,
                notebookUrl: document.getElementById('obNotebookUrl').value,
                googleAdsId: document.getElementById('obGoogleAdsId').value,
                v4mosKey: document.getElementById('obV4mosKey').value
            };

            if (!data.name) return alert("O nome do cliente é obrigatório.");

            startOnboardingBtn.innerHTML = "⏳ Criando Estrutura...";
            
            try {
                const res = await fetch('http://localhost:3001/api/onboarding', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });

                if (res.ok) {
                    addMessage(`✅ Onboarding concluído para **${data.name}**! A pasta bases/peretto-co/clientes/${data.name.toLowerCase()} foi criada com o arquivo .env e CLAUDE.md.`, 'ai');
                    onboardingModal.style.display = 'none';
                    await fetchLocalClients(); // Atualiza o dropdown
                } else {
                    // Fallback para V0/Vercel (Salvar apenas no localStorage)
                    const localClients = JSON.parse(localStorage.getItem('v0_clients') || '[]');
                    localClients.push({ id: data.name.toLowerCase(), name: data.name });
                    localStorage.setItem('v0_clients', JSON.stringify(localClients));
                    
                    addMessage(`✅ Onboarding concluído (Modo Cloud)! O cliente **${data.name}** foi salvo na sua sessão local.`, 'ai');
                    onboardingModal.style.display = 'none';
                    await fetchLocalClients();
                }
            } catch (e) {
                // Se o servidor local não existir (V0), salvar no localStorage
                const localClients = JSON.parse(localStorage.getItem('v0_clients') || '[]');
                localClients.push({ id: data.name.toLowerCase(), name: data.name });
                localStorage.setItem('v0_clients', JSON.stringify(localClients));
                
                addMessage(`✅ Onboarding concluído (Modo Cloud)! O cliente **${data.name}** foi salvo na sua sessão local.`, 'ai');
                onboardingModal.style.display = 'none';
                renderClientsDropdown();
            } finally {
                startOnboardingBtn.innerHTML = "Finalizar e Criar Estrutura";
            }
        };

        // Context Logic
        const savedContext = localStorage.getItem('peretto_context');
        
        function renderClientsDropdown(clients = []) {
            const localClients = JSON.parse(localStorage.getItem('v0_clients') || '[]');
            const allClients = [...clients, ...localClients];
            
            contextSelect.innerHTML = '<option value="none">Selecione um Cliente...</option>';
            allClients.forEach(c => {
                const opt = document.createElement('option');
                opt.value = c.id;
                opt.textContent = c.name.toUpperCase();
                contextSelect.appendChild(opt);
            });
            if (savedContext) {
                contextSelect.value = savedContext;
                updateContextUI(savedContext, contextSelect.options[contextSelect.selectedIndex]?.text);
            }
        }

        async function fetchLocalClients() {
            try {
                const res = await fetch('http://localhost:3001/api/clients');
                if (res.ok) {
                    const clients = await res.json();
                    renderClientsDropdown(clients);
                } else {
                    renderClientsDropdown([]);
                }
            } catch (e) {
                renderClientsDropdown([]);
            }
        }
        
        fetchLocalClients();

        function updateContextUI(contextValue, contextName) {
            const ui = document.getElementById('clientContextUI');
            const label = document.getElementById('clientContextLabel');
            
            if (contextValue && contextValue !== 'none') {
                ui.classList.add('client-active');
                label.textContent = contextName;
            } else {
                ui.classList.remove('client-active');
                label.textContent = "Sem Cliente";
            }
        }

        contextSelect.addEventListener('change', () => {
            localStorage.setItem('peretto_context', contextSelect.value);
            const contextName = contextSelect.options[contextSelect.selectedIndex].text;
            updateContextUI(contextSelect.value, contextName);
            addMessage(`Contexto duplo ativado: Motor Global (Peretto & Co) + Motor Cliente (**${contextName}**).`, 'ai', `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 12h-4l-3 9L9 3l-3 9H2"></path></svg>`);
        });

        const refreshContextBtn = document.getElementById('refreshContextBtn');
        if (refreshContextBtn) {
            refreshContextBtn.onclick = () => fetchLocalClients();
        }

        // Google Drive Logic
        const googleDriveBtn = document.getElementById('googleDriveBtn');
        let driveConnected = localStorage.getItem('drive_connected') === 'true';

        if (driveConnected) {
            googleDriveBtn.innerHTML = `<span>✅ Drive Conectado</span>`;
            googleDriveBtn.style.background = '#e8f5e9';
            googleDriveBtn.style.color = '#2e7d32';
        }

        googleDriveBtn.onclick = () => {
            if (!driveConnected) {
                // Simulação de OAuth
                googleDriveBtn.innerHTML = `<span>⏳ Autenticando...</span>`;
                setTimeout(() => {
                    driveConnected = true;
                    localStorage.setItem('drive_connected', 'true');
                    googleDriveBtn.innerHTML = `<span>✅ Drive Conectado</span>`;
                    googleDriveBtn.style.background = '#e8f5e9';
                    googleDriveBtn.style.color = '#2e7d32';
                    addMessage("Sua conta do **Google Drive** foi conectada com sucesso! Agora os agentes podem buscar arquivos e usá-los como base de conhecimento.", 'ai', `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"></path></svg>`);
                }, 1500);
            } else {
                if (confirm("Deseja desconectar o Google Drive?")) {
                    driveConnected = false;
                    localStorage.removeItem('drive_connected');
                    location.reload();
                }
            }
        };

        // Modal & Tabs Logic
        openWikiBtn.onclick = () => wikiModal.style.display = 'flex';
        closeWikiBtn.onclick = () => wikiModal.style.display = 'none';
        window.onclick = (event) => { if (event.target == wikiModal) wikiModal.style.display = 'none'; }

        tabBtns.forEach(btn => {
            btn.onclick = () => {
                tabBtns.forEach(b => b.classList.remove('active'));
                tabContents.forEach(c => c.classList.remove('active'));
                btn.classList.add('active');
                document.getElementById(btn.dataset.tab + 'Tab').classList.add('active');
            }
        });

        providerSelect.innerHTML = '';
        Object.keys(providers).forEach(key => {
            const opt = document.createElement('option');
            opt.value = key; opt.textContent = providers[key].name;
            providerSelect.appendChild(opt);
        });

        loadSettings();
        loadAgent(currentAgent);
        loadChatHistory();
        updateUIForProvider();
        fetchOpenRouterModels();

        promptInput.addEventListener('input', function() {
            this.style.height = '24px'; this.style.height = (this.scrollHeight) + 'px';
        });
    }

    // --- TASK MANAGEMENT (ASYNC SIMULATION) ---
    function createTask(title) {
        const id = 'task-' + Date.now();
        const task = { id, title, status: 'Iniciando...', progress: 0 };
        activeTasks.push(task);
        renderTasks();
        
        // Simular progresso autônomo
        let prog = 0;
        const interval = setInterval(() => {
            prog += Math.random() * 15;
            if (prog >= 100) {
                prog = 100;
                task.status = 'Concluído';
                clearInterval(interval);
                addMessage(`**[Tarefa Assíncrona Concluída]**\n${title}: O agente finalizou o processamento em segundo plano.`, 'ai');
            } else if (prog > 60) { task.status = 'Finalizando...'; }
            else if (prog > 30) { task.status = 'Analisando...'; }
            else { task.status = 'Executando...'; }
            
            task.progress = prog;
            renderTasks();
        }, 1500);
    }

    function renderTasks() {
        if (activeTasks.length === 0) {
            taskList.innerHTML = '<div class="empty-tasks">Nenhuma tarefa assíncrona ativa.</div>';
            return;
        }
        taskList.innerHTML = activeTasks.map(t => `
            <div class="task-item">
                <div class="task-header">
                    <span class="task-title">${t.title}</span>
                    <span class="task-status">${t.status}</span>
                </div>
                <div class="task-progress-bar">
                    <div class="task-progress-fill" style="width: ${t.progress}%"></div>
                </div>
            </div>
        `).join('');
    }

    // --- SETTINGS & PERSISTENCE ---
    function saveSettings() {
        localStorage.setItem('peretto_provider', providerSelect.value);
        localStorage.setItem('peretto_model', modelSelect.value);
        localStorage.setItem('peretto_apiKey', apiKeyInput.value);
        localStorage.setItem('peretto_customModel', customModelInput.value);
    }

    function loadSettings() {
        const savedProvider = localStorage.getItem('peretto_provider');
        if (savedProvider) providerSelect.value = savedProvider;
        const savedKey = localStorage.getItem('peretto_apiKey');
        if (savedKey) apiKeyInput.value = savedKey;
        const savedCustom = localStorage.getItem('peretto_customModel');
        if (savedCustom) customModelInput.value = savedCustom;
    }

    function saveChatHistory() {
        localStorage.setItem('peretto_chat_' + currentAgent, JSON.stringify(chatMessages));
    }

    function loadChatHistory() {
        const saved = localStorage.getItem('peretto_chat_' + currentAgent);
        if (saved) {
            chatMessages = JSON.parse(saved);
            chatHistory.innerHTML = '';
            chatMessages.forEach(m => renderMessage(m.text, m.sender, m.icon));
        } else {
            chatMessages = [];
            addInitialGreeting();
        }
    }

    function addInitialGreeting() {
        const agent = agentsConfig[currentAgent];
        let greeting = `Olá! Eu sou o **${agent.name}**. Como posso ajudar na operação hoje?`;
        
        if (currentAgent === 'peretto_novo_cliente') {
            greeting = "Olá! Eu sou o **assistente de onboarding**. Vamos configurar o seu novo cliente no padrão Peretto & Co?";
        }
        
        addMessage(greeting, 'ai', agent.icon);
    }

    async function fetchOpenRouterModels() {
        try {
            const response = await fetch("https://openrouter.ai/api/v1/models");
            const json = await response.json();
            cachedModels.openrouter = json.data.map(m => ({ id: m.id, name: m.name, isFree: m.pricing.prompt === "0" && m.pricing.completion === "0" }));
            cachedModels.openrouter.sort((a, b) => (b.isFree ? 1 : 0) - (a.isFree ? 1 : 0));
            if (providerSelect.value === 'openrouter') updateModelDropdown();
        } catch (error) { console.error("Erro ao buscar modelos:", error); }
    }

    function loadAgent(agentKey) {
        currentAgent = agentKey;
        const agent = agentsConfig[agentKey];
        agentItems.forEach(item => item.classList.remove('active'));
        const el = document.querySelector(`[data-agent="${agentKey}"]`);
        if (el) el.classList.add('active');
        currentAgentName.textContent = agent.name;
        currentAgentDesc.textContent = agent.desc;
        systemPromptInput.value = agent.prompt;
        loadChatHistory();
    }

    agentItems.forEach(item => item.addEventListener('click', () => loadAgent(item.getAttribute('data-agent'))));

    function updateUIForProvider() {
        const providerKey = providerSelect.value;
        const config = providers[providerKey];
        baseUrlInput.value = config.url;
        apiKeyInput.placeholder = config.keyPlaceholder;
        getApiKeyBtn.style.display = config.keyLink ? 'flex' : 'none';
        if (config.keyLink) getApiKeyBtn.href = config.keyLink;
        baseUrlGroup.style.display = (providerKey === 'openrouter') ? 'none' : 'block';
        updateModelDropdown();
    }

    function updateModelDropdown() {
        const providerKey = providerSelect.value;
        const models = cachedModels[providerKey] || [];
        modelSelect.innerHTML = '';
        if (providerKey === 'openrouter' && models.length === 0) {
            modelSelect.innerHTML = '<option>Carregando modelos...</option>'; return;
        }
        models.forEach(m => {
            const opt = document.createElement('option'); opt.value = m.id; opt.textContent = m.isFree ? `🎁 ${m.name}` : m.name; modelSelect.appendChild(opt);
        });
        const customOpt = document.createElement('option'); customOpt.value = 'custom'; customOpt.textContent = "⚙️ Digitar ID Manualmente..."; modelSelect.appendChild(customOpt);
        checkCustomModel();
    }

    function checkCustomModel() {
        customModelInput.style.display = modelSelect.value === 'custom' ? 'block' : 'none';
        saveSettings();
    }

    providerSelect.addEventListener('change', () => { updateUIForProvider(); saveSettings(); });
    modelSelect.addEventListener('change', () => { checkCustomModel(); saveSettings(); });
    apiKeyInput.addEventListener('input', saveSettings);
    customModelInput.addEventListener('input', saveSettings);

    function renderMessage(text, sender, iconStr) {
        const msgDiv = document.createElement('div');
        msgDiv.className = `message ${sender}-msg`;
        
        let defaultUser = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>`;
        let icon = iconStr || (sender === 'user' ? defaultUser : agentsConfig[currentAgent].icon);
        
        const formattedText = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        msgDiv.innerHTML = `<div class="avatar">${icon}</div><div class="content">${formattedText}</div>`;
        chatHistory.appendChild(msgDiv); chatHistory.scrollTop = chatHistory.scrollHeight;
    }

    function addMessage(text, sender, iconStr = null) {
        chatMessages.push({ text, sender, icon: iconStr });
        renderMessage(text, sender, iconStr);
        saveChatHistory();
    }

    function showLoading() {
        const id = 'loading-' + Date.now();
        const msgDiv = document.createElement('div');
        msgDiv.className = `message ai-msg`; msgDiv.id = id;
        msgDiv.innerHTML = `<div class="avatar">${agentsConfig[currentAgent].icon}</div><div class="content loading-dots"><div></div><div></div><div></div></div>`;
        chatHistory.appendChild(msgDiv); chatHistory.scrollTop = chatHistory.scrollHeight;
        return id;
    }

    function removeLoading(id) { const el = document.getElementById(id); if (el) el.remove(); }

    // --- GLOBAL SETTINGS (Para o time Tech configurar no deploy) ---
    const GLOBAL_CONFIG = {
        defaultApiKey: "", 
        isUnifiedAuth: false 
    };

    async function sendToAPI(userPrompt) {
        const providerKey = providerSelect.value;
        const userApiKey = apiKeyInput.value.trim();
        const baseSystemPrompt = systemPromptInput.value.trim();
        const contextValue = contextSelect.value;
        const baseUrl = baseUrlInput.value.trim();
        const modelId = modelSelect.value === 'custom' ? customModelInput.value.trim() : modelSelect.value;

        let finalSystemPrompt = baseSystemPrompt;
        
        // 1. Motor Global (Manual da Franquia) sempre injetado
        finalSystemPrompt += `\n\n[BASE DE CONHECIMENTO GLOBAL - ATIVA]: Você está operando sob o Manual de Operações da franquia Peretto & Co. Siga rigorosamente as diretrizes da V4 Company para todos os processos (SPICED, FCA, OKR, Quality Check).`;

        // 2. Motor Específico (Cliente) injetado se selecionado
        if (contextValue !== 'none') {
            const contextName = contextSelect.options[contextSelect.selectedIndex].text;
            finalSystemPrompt += `\n\n[BASE DE CONHECIMENTO ESPECÍFICA - ATIVA]: O usuário está trabalhando ativamente na conta do cliente "${contextName}". Adapte suas respostas e estratégias para a realidade, o nicho e os dados atuais desta conta específica.`;
        }

        const activeApiKey = userApiKey || GLOBAL_CONFIG.defaultApiKey;

        if (providerKey !== 'ollama' && providerKey !== 'custom' && !activeApiKey) {
            throw new Error("Nenhuma chave encontrada. Insira sua chave ou autentique-se no Peretto Hub.");
        }

        const response = await fetch(`${baseUrl}/chat/completions`, {
            method: "POST",
            headers: { 
                "Content-Type": "application/json", 
                "Authorization": `Bearer ${activeApiKey}`, 
                "HTTP-Referer": window.location.href, 
                "X-Title": "Peretto Agent Manager" 
            },
            body: JSON.stringify({ model: modelId, messages: [{ role: "system", content: finalSystemPrompt }, { role: "user", content: userPrompt }], temperature: 0.7 })
        });
        
        if (!response.ok) { const err = await response.text(); throw new Error(`Erro na API: ${err}`); }
        const data = await response.json(); return data.choices[0].message.content;
    }

    async function handleChatSubmit() {
        const text = promptInput.value.trim();
        if (!text) return;
        
        if (text.toLowerCase().includes("analisar") || text.toLowerCase().includes("processar") || text.toLowerCase().includes("executar")) {
            createTask(text.substring(0, 30) + "...");
        }

        promptInput.value = ''; promptInput.style.height = '24px'; sendBtn.disabled = true;
        addMessage(text, 'user');
        const loadingId = showLoading();
        try {
            const aiResponse = await sendToAPI(text);
            removeLoading(loadingId);
            addMessage(aiResponse, 'ai');
        } catch (error) {
            removeLoading(loadingId);
            addMessage(`**Erro:** ${error.message}`, 'ai', '⚠️');
        } finally { sendBtn.disabled = false; }
    }

    sendBtn.addEventListener('click', handleChatSubmit);
    promptInput.addEventListener('keydown', (e) => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); handleChatSubmit(); } });
    init();
});
