const express = require('express');
const session = require('express-session');
const { createProxyMiddleware } = require('http-proxy-middleware');
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const app = express();
const PORT = process.env.PORT || 3000;
const SESSION_SECRET = process.env.SESSION_SECRET || crypto.randomBytes(32).toString('hex');
const USERS_PATH = process.env.USERS_PATH || '/app/users.json';

let usersCache = [];
let usersCacheTime = 0;

function loadUsers() {
  const stat = fs.statSync(USERS_PATH, { throwIfNoEntry: false });
  if (!stat) return [];
  if (stat.mtimeMs === usersCacheTime && usersCache.length) return usersCache;
  try {
    const raw = fs.readFileSync(USERS_PATH, 'utf-8');
    usersCache = JSON.parse(raw).users || [];
    usersCacheTime = stat.mtimeMs;
    return usersCache;
  } catch {
    return [];
  }
}

function findUser(usernameOrEmail) {
  return loadUsers().find(u => u.username === usernameOrEmail || u.email === usernameOrEmail);
}

function getUser(req) {
  const remoteUser = req.headers['remote-user'] || req.headers['x-forwarded-user'];
  if (remoteUser) {
    const user = findUser(remoteUser);
    if (user) return user;
  }
  if (req.session?.user) {
    const user = findUser(req.session.user.username);
    if (user) return user;
  }
  return null;
}

app.use(express.json());
app.use(session({
  secret: SESSION_SECRET,
  resave: false,
  saveUninitialized: false,
  cookie: {
    secure: process.env.NODE_ENV === 'production',
    httpOnly: true,
    maxAge: 24 * 60 * 60 * 1000
  }
}));

app.get('/api/health', (_req, res) => res.json({ status: 'ok', uptime: process.uptime() }));
app.get('/api/session', (req, res) => {
  const user = getUser(req);
  if (user) return res.json({ authenticated: true, user });
  res.json({ authenticated: false });
});

app.get('/login', (req, res) => {
  if (getUser(req)) return res.redirect('/');
  res.sendFile(path.join(__dirname, 'public', 'login.html'));
});

app.post('/api/login', (req, res) => {
  const { username, password } = req.body;
  if (!username || !password) return res.status(400).json({ error: 'Usuário e senha obrigatórios' });
  const user = findUser(username);
  if (!user) return res.status(401).json({ error: 'Usuário ou senha inválidos' });
  const hash = crypto.createHash('sha256').update(password).digest('hex');
  const storedHash = user.passwordHash;
  if (!storedHash || hash !== storedHash) return res.status(401).json({ error: 'Usuário ou senha inválidos' });
  req.session.user = user;
  res.json({ success: true, user: { name: user.name, username: user.username, squad: user.squad } });
});

app.post('/api/logout', (req, res) => {
  req.session.destroy(() => {
    res.clearCookie('connect.sid');
    res.json({ success: true });
  });
});

app.use('/static', express.static(path.join(__dirname, 'public')));

const opencodeProxy = createProxyMiddleware({
  target: (req) => {
    const user = getUser(req);
    const safeName = user ? user.username.replace(/\./g, '-') : '';
    return user ? `http://opencode-web-${safeName}:4096` : 'http://opencode-web:4096';
  },
  changeOrigin: true,
  ws: true
});

app.use('/', (req, res, next) => {
  if (req.path === '/api/health' || req.path.startsWith('/login') || req.path.startsWith('/static')) return next();
  if (getUser(req)) return opencodeProxy(req, res, next);
  res.redirect('/login');
});

app.listen(PORT, '0.0.0.0', () => {
  console.log(`OpenCode Login rodando na porta ${PORT}`);
});
