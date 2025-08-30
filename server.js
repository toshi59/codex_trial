import http from 'http';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

const evalItems = [
  'GDPR適合性',
  'DPIA/PIAの実施',
  'EU AI Act影響',
  'モデル/重みのライセンス',
  'PII/機微情報制御',
  '暗号化',
  'レッドチーム/安全性評価',
  'バイアス/公平性',
  '業務適合性',
  '活動状況',
  '再現可能なビルド',
  'モデルカード/システムカード'
];

const server = http.createServer(async (req, res) => {
  const url = new URL(req.url, `http://${req.headers.host}`);

  if (url.pathname === '/research') {
    const modelName = url.searchParams.get('model');
    if (!modelName) {
      res.writeHead(400, { 'Content-Type': 'application/json' });
      return res.end(JSON.stringify({ error: 'model query required' }));
    }
    const apiKey = process.env.OPENAI_API_KEY;
    if (!apiKey) {
      res.writeHead(500, { 'Content-Type': 'application/json' });
      return res.end(JSON.stringify({ error: 'OPENAI_API_KEY not set' }));
    }

    const checklist = evalItems.map(i => `- ${i}`).join('\n');
    const prompt = `あなたは調査アシスタントです。モデル「${modelName}」について公開情報を調べ、次の各チェック項目が満たされているか評価してください。\n結果はJSONで返してください。形式:\n{\n"metadata": {"model_name": "", "version": "", "provider": "", "license": ""},\n"evaluations": [{"item": "", "status": "達成/未達/不明", "note": ""}]\n}\nチェック項目:\n${checklist}`;

    try {
      const apiRes = await fetch('https://api.openai.com/v1/responses', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${apiKey}`
        },
        body: JSON.stringify({
          model: 'gpt-4.1-mini',
          input: prompt
        })
      });
      const data = await apiRes.json();
      const text = data.output?.[0]?.content?.[0]?.text || data.choices?.[0]?.message?.content || '';
      let result;
      try {
        result = JSON.parse(text);
      } catch (e) {
        result = { metadata: { model_name: modelName }, evaluations: [] };
      }
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify(result));
    } catch (err) {
      res.writeHead(500, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ error: err.message }));
    }
    return;
  }

  // static file
  let filePath = path.join(__dirname, url.pathname === '/' ? 'index.html' : url.pathname);
  fs.readFile(filePath, (err, data) => {
    if (err) {
      res.writeHead(404);
      return res.end('Not found');
    }
    const ext = path.extname(filePath).toLowerCase();
    const type = {
      '.html': 'text/html',
      '.css': 'text/css',
      '.js': 'text/javascript'
    }[ext] || 'application/octet-stream';
    res.writeHead(200, { 'Content-Type': type });
    res.end(data);
  });
});

const port = process.env.PORT || 8000;
server.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});

