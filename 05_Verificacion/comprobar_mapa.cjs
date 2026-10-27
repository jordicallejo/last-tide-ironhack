const assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm');
const html=fs.readFileSync(process.argv[2]||require('node:path').join(__dirname,'../03_Videojuego/LAST_TIDE_Juego.html'),'utf8');const scripts=[...html.matchAll(/<script[^>]*>([\s\S]*?)<\/script>/g)].map(m=>m[1]);
for(const s of scripts)new vm.Script(s);
const env={};vm.createContext(env);vm.runInContext(scripts[0]+scripts[1]+';globalThis.api={LEVELS,Campaign}',env);const {LEVELS,Campaign}=env.api;
let s=Campaign.sanitize(null);assert.equal(s.completed.length,0);assert.equal(Campaign.unlocked(s,0),true);assert.equal(Campaign.unlocked(s,1),false);assert.equal(Campaign.unlocked(s,-1),false);assert.equal(Campaign.unlocked(s,4),false);
s=Campaign.complete(s,3);assert.equal(s.completed.length,0);
for(let i=0;i<4;i++){assert.equal(Campaign.unlocked(s,i),true);s=Campaign.complete(s,i);assert.equal(s.completed.length,i+1);s=Campaign.complete(s,i);assert.equal(s.completed.length,i+1);}
assert.equal(Campaign.sanitize({completed:['australia']}).completed.length,0);
assert.equal(Campaign.sanitize({completed:['florida','florida','fake']}).completed.length,1);
assert.equal(Campaign.sanitize(JSON.parse(JSON.stringify(s))).completed.length,4);
assert.equal(new Set(LEVELS.map(l=>l.id)).size,4);for(const l of LEVELS){assert.equal(l.points.length,3);assert.equal(l.modes.length,3);assert.ok(l.lat>=-90&&l.lat<=90&&l.lon>=-180&&l.lon<=180);assert.ok(l.evidence&&!/mÃ¡s peligroso/.test(l.evidence));}
assert.equal(Campaign.project(0,0).x,540);assert.equal(Campaign.project(0,0).y,270);
assert.equal(/https?:\/\//.test(html.replaceAll('http://www.w3.org/2000/svg','')),false);
console.log('OK: JavaScript vÃ¡lido; 4 niveles; bloqueos; progreso secuencial; repeticiÃ³n idempotente; guardado; entradas alteradas; proyecciÃ³n; sin dependencias de red.');
