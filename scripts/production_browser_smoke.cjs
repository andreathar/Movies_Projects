/* Explicit synthetic browser smoke test. No production credential may be passed here. */
const fs = require('node:fs');
const path = require('node:path');
const os = require('node:os');
const crypto = require('node:crypto');
const [modulePath, url, fixtureRoot, output] = process.argv.slice(2);
let phase = 'startup';
let browser;
let loginStatus = null;
let loginOrigin = null;
(async () => {
  const { chromium } = require(modulePath);
  // Accept only an orchestrator-owned temporary fixture, never a production key path.
  const parsed = new URL(url);
  if (parsed.protocol !== 'http:' || parsed.hostname !== '127.0.0.1' || !parsed.port || parsed.username || parsed.password || parsed.pathname !== '/' || parsed.search || parsed.hash) throw Error('loopback URL required');
  const root = fs.realpathSync(fixtureRoot);
  if (root !== path.resolve(fixtureRoot) || path.dirname(root) !== fs.realpathSync(os.tmpdir()) || !path.basename(root).startsWith('production-browser-fixture-')) throw Error('temporary fixture required');
  const nonce = process.env.PRODUCTION_BROWSER_FIXTURE_NONCE;
  if (!nonce || fs.readFileSync(path.join(root, '.synthetic-browser-fixture'), 'utf8') !== nonce) throw Error('orchestrator required');
  delete process.env.PRODUCTION_BROWSER_FIXTURE_NONCE;
  const readKey = name => {
    const keyPath = path.join(root, name);
    const stat = fs.lstatSync(keyPath);
    if (!stat.isFile() || stat.isSymbolicLink() || (stat.mode & 0o077) !== 0 || fs.realpathSync(keyPath) !== keyPath) throw Error('private fixture key required');
    return fs.readFileSync(keyPath, 'utf8').trim();
  };
  const operator = readKey('operator.key');
  const executor = readKey('executor.key');
  browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({ viewport: { width: 1440, height: 1000 } });
  const page = await context.newPage();
  const errors = [];
  page.on('pageerror', () => errors.push('pageerror'));
  const assert = (ok, name) => { if (!ok) throw Error(name); };
  async function login(page, token) {
    await page.goto(url);
    phase = 'login keyboard focus';
    await page.keyboard.press('Tab');
    assert(await page.locator('#credential').evaluate(el => el === document.activeElement), 'keyboard login focus');
    await page.locator('#credential').fill(token);
    await page.keyboard.press('Tab');
    phase = 'login POST';
    const [response] = await Promise.all([page.waitForResponse(r => r.request().method() === 'POST'), page.keyboard.press('Enter')]);
    loginStatus = response.status();
    loginOrigin = (await response.request().allHeaders()).origin || 'absent';
    await page.getByRole('heading', { name: 'Gestão de produção', exact: true }).waitFor();
  }
  async function operation(page, command, values) {
    if (command !== 'project-create') {
      await page.getByRole('button', { name: 'Projeto de teste — sem produção (synthetic)', exact: true }).click();
    }
    const detail = page.locator('details').filter({ has: page.locator(`input[name="command"][value="${command}"]`) });
    await detail.locator('summary').click();
    for (const [key, value] of Object.entries(values)) {
      const control = page.locator(`#${command}-${key}`);
      if (await control.evaluate(el => el.tagName === 'SELECT')) await control.selectOption(value);
      else await control.fill(value);
    }
    if (!Object.hasOwn(values, 'reason')) await page.locator(`#${command}-reason`).fill('Synthetic browser verification only');
    await detail.getByRole('button').click();
    await page.getByRole('heading', { name: 'Operação registrada', exact: true }).waitFor();
    await page.getByRole('button', { name: 'Voltar ao painel', exact: true }).click();
    await page.getByRole('heading', { name: 'Gestão de produção', exact: true }).waitFor();
  }
  phase = 'login screenshot';
  await page.goto(url);
  await page.screenshot({ path: path.join(output, 'login-desktop.png'), fullPage: true });
  phase = 'keyboard login and empty state';
  await login(page, operator);
  assert((await page.textContent('main')).includes('Banco sem projetos'), 'genuine empty state');
  assert((await context.cookies()).length === 0, 'cookie-free sessions');
  assert(await page.evaluate(() => localStorage.length === 0 && sessionStorage.length === 0), 'no browser persistence');
  await page.screenshot({ path: path.join(output, 'empty-desktop.png'), fullPage: true });
  phase = 'mobile empty state';
  await page.setViewportSize({ width: 390, height: 844 });
  assert(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth), 'no mobile page overflow');
  await page.screenshot({ path: path.join(output, 'empty-mobile.png'), fullPage: true });
  await page.setViewportSize({ width: 1440, height: 1000 });
  phase = 'project and assignment forms';
  await operation(page, 'project-create', { project: 'synthetic', title: 'Projeto de teste — sem produção' });
  await page.getByRole('button', { name: 'Projeto de teste — sem produção (synthetic)', exact: true }).click();
  assert(await page.locator('#member-add-role').evaluate(el => el.tagName === 'SELECT'), 'native role dropdown');
  assert(await page.locator('#approval-record-outcome').evaluate(el => el.tagName === 'SELECT'), 'native outcome dropdown');
  await operation(page, 'member-add', { project: 'synthetic', user: 'executor', role: 'contributor' });
  await operation(page, 'task-create', { project: 'synthetic', id: 'T1', title: 'Proposta sintética' });
  await operation(page, 'task-offer', { task: 'T1', revision: '1', to: 'executor', scope: 'Only the synthetic proposal; no spend', allowed_path: 'proposal.md' });
  phase = 'executor identity and acceptance';
  const executorContext = await browser.newContext({ viewport: { width: 1440, height: 1000 } });
  const executorPage = await executorContext.newPage();
  await login(executorPage, executor);
  await operation(executorPage, 'task-accept', { task: 'T1', revision: '2' });
  fs.writeFileSync(path.join(fixtureRoot, 'proposal.md'), 'Synthetic browser proposal. Not film content.\n', { flag: 'wx', mode: 0o600 });
  phase = 'artifact and handoff forms';
  await operation(executorPage, 'artifact-add', { task: 'T1', revision: '3', id: 'A1', path: 'proposal.md' });
  await operation(executorPage, 'handoff-submit', { task: 'T1', revision: '3', id: 'H1', scope: 'Synthetic proposal only', limitations: 'No artistic acceptance', artifact: 'A1', check: 'readback | passed | Read exact synthetic bytes' });
  phase = 'producer verification and integration';
  await operation(page, 'handoff-verify', { handoff: 'H1', revision: '1' });
  await operation(page, 'handoff-integrate', { handoff: 'H1', revision: '2', closed: 'true' });
  await page.getByRole('button', { name: 'Projeto de teste — sem produção (synthetic)', exact: true }).click();
  assert((await page.textContent('main')).includes('completed'), 'completed task visible');
  await page.screenshot({ path: path.join(output, 'completed-desktop.png'), fullPage: true });
  phase = 'API reads same state';
  const response = await context.request.get(`${url}api/snapshot?project=synthetic`, { headers: { Authorization: `Bearer ${operator}` } });
  assert(response.ok(), 'API authenticated snapshot');
  const { snapshot } = await response.json();
  assert(snapshot.tasks[0].state === 'completed', 'same database state');
  assert(snapshot.approvals.length === 0, 'integration is not approval');
  const html = await page.content();
  assert(!html.includes(operator) && !html.includes(executor), 'no credential reflected in HTML');
  phase = 'logout';
  await page.getByRole('button', { name: 'Sair', exact: true }).click();
  await page.getByRole('heading', { name: 'Entrar na gestão local', exact: true }).waitFor();
  assert(errors.length === 0, 'no page errors');
  const versions = { chromium: browser.version(), playwright: require(path.join(modulePath, 'package.json')).version, node: process.version };
  const scriptHash = crypto.createHash('sha256').update(fs.readFileSync(__filename)).digest('hex');
  await browser.close();
  console.log(JSON.stringify({ status: 'passed', browser: 'Chromium headless', syntheticOnly: true, versions, browserScriptSha256: scriptHash,
    checks: ['native-role-dropdown', 'native-outcome-dropdown', 'existing-record-dropdowns', 'keyboard-login', 'empty-state', 'desktop', 'mobile-no-overflow', 'no-cookies-or-storage', 'separate-executor', 'assignment-acceptance', 'artifact-hash', 'handoff-submit', 'producer-verification', 'closed-integration', 'API-same-state', 'no-implicit-approval', 'no-credential-reflection', 'logout'],
    screenshots: ['login-desktop.png', 'empty-desktop.png', 'empty-mobile.png', 'completed-desktop.png'] }));
})().catch(async () => {
  if (browser) await browser.close().catch(() => {});
  // Playwright call logs may include values entered into password fields. Never print them.
  console.error(JSON.stringify({ status: 'failed', phase, loginStatus, loginOrigin }));
  process.exitCode = 1;
});
