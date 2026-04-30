const express = require('express');
const { exec } = require('child_process');
const cors = require('cors');
const fs = require('fs');
const path = require('path');

const app = express();
app.use(cors());
app.use(express.json());

// CONFIGURAÇÃO: Aponte para a raiz do seu repositório Builders Hub
const REPO_PATH = 'c:\\Users\\marco\\Desktop\\builders-tests';

// Endpoint para ler as skills locais dinamicamente
app.get('/api/skills', (req, res) => {
    const skillsPath = path.join(REPO_PATH, '.agents', 'skills');
    try {
        const folders = fs.readdirSync(skillsPath);
        const skills = folders.map(folder => {
            const skillMdPath = path.join(skillsPath, folder, 'SKILL.md');
            if (fs.existsSync(skillMdPath)) {
                const content = fs.readFileSync(skillMdPath, 'utf-8');
                return { id: folder, content };
            }
            return null;
        }).filter(s => s !== null);
        res.json(skills);
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

// Endpoint para ler os clientes reais
app.get('/api/clients', (req, res) => {
    const clientsPath = path.join(REPO_PATH, 'bases', 'peretto-co', 'clientes');
    try {
        if (!fs.existsSync(clientsPath)) {
            return res.json([]);
        }
        const folders = fs.readdirSync(clientsPath, { withFileTypes: true });
        const clients = folders.filter(dirent => dirent.isDirectory() && dirent.name !== '_template-peretto')
                               .map(dirent => ({ id: dirent.name, name: dirent.name.replace(/-/g, ' ') }));
        res.json(clients);
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

// Endpoint para Onboarding (Cria pasta e .env)
app.post('/api/onboarding', (req, res) => {
    const { name, notebookUrl, googleAdsId, v4mosKey } = req.body;
    const clientSlug = name.toLowerCase().replace(/\s+/g, '-');
    const clientPath = path.join(REPO_PATH, 'bases', 'peretto-co', 'clientes', clientSlug);

    try {
        if (!fs.existsSync(clientPath)) {
            fs.mkdirSync(clientPath, { recursive: true });
        }

        const envContent = `CLIENT_NAME=${name}\nNOTEBOOK_LM_URL=${notebookUrl}\nGOOGLE_ADS_ID=${googleAdsId}\nV4MOS_API_KEY=${v4mosKey}\n`;
        fs.writeFileSync(path.join(clientPath, '.env'), envContent);
        
        // Cria um CLAUDE.md inicial básico
        const claudeMd = `# Contexto: ${name}\n\nEste cliente utiliza o NotebookLM: ${notebookUrl}\nGoogle Ads ID: ${googleAdsId}\n`;
        fs.writeFileSync(path.join(clientPath, 'CLAUDE.md'), claudeMd);

        res.json({ success: true, slug: clientSlug });
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

// Endpoint para executar comandos (CUIDADO: Apenas para uso local seguro)
app.post('/api/execute', (req, res) => {
    const { command } = req.body;
    console.log(`Executando: ${command}`);
    
    // Executa o comando na pasta do repositório
    exec(command, { cwd: REPO_PATH }, (error, stdout, stderr) => {
        if (error) {
            return res.status(500).json({ error: error.message, stderr });
        }
        res.json({ stdout, stderr });
    });
});

const PORT = 3001;
app.listen(PORT, () => {
    console.log(`🚀 Bridge Peretto ativa em http://localhost:${PORT}`);
    console.log(`Conectada ao repositório: ${REPO_PATH}`);
});
