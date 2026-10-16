import { execFileSync } from 'node:child_process';
import { realpath } from 'node:fs/promises';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { source, catalog, unique, verifyPath, emit, outputPath } from './export-common.mjs';
const args=process.argv.slice(2);const check=args.includes('--check');
const root=await realpath(resolve(args.find(a=>a!=='--check')||'../..'));
const site=resolve(dirname(fileURLToPath(import.meta.url)),'..');
const files=['workspace.json','skills/registry.json','skills/README.md','agents/registry.json','agents/README.md','tasks/README.md','docs/WORKSPACE.md','docs/FOLDER_STRUCTURE.md','projects/andre-time-travel/tasks/README.md'];
const inputs={},sources=[];
for(const path of files)inputs[path]=await source(root,path,sources);
const workspace=JSON.parse(inputs['workspace.json']);
const activeFilm=workspace.projects.find(p=>p.id===workspace.activeFilm);
if(!activeFilm)throw Error('Filme ativo ausente');
const assetPath=activeFilm.root+'/asset-registry.csv';
await source(root,assetPath,sources);
const assetReport=JSON.parse(execFileSync('python3',[resolve(root,'scripts/manage.py'),'--root',root,'assets','validate','--film',activeFilm.root],{encoding:'utf8',maxBuffer:4*1024*1024}));
if(assetReport.status!=='ok'||assetReport.errors.length||Object.keys(assetReport.duplicate_asset_ids).length)throw Error('Catálogo de mídia inválido');
const assetIds=unique(assetReport.records,'asset_id');
if(assetReport.catalog_sha256!==sources.find(s=>s.path===assetPath).sha256)throw Error('Catálogo mudou durante exportação');
const assetCatalog={path:assetPath,sha256:assetReport.catalog_sha256,recordCount:assetReport.records.length,uniqueIdCount:assetIds.size,localReferenceCount:assetReport.records.filter(r=>r.path_base!=='provider').length,uniqueLocalPathCount:new Set(assetReport.records.filter(r=>r.path_base!=='provider').map(r=>(r.path_base==='film'?activeFilm.root+'/':'')+r.path_or_provider_id)).size,providerReferenceCount:assetReport.records.filter(r=>r.path_base==='provider').length,historicalOriginLiteralsPending:assetReport.records.filter(r=>r.source.includes('legacy_origin_path_literal=')).length,approvalScope:'catalog_flags_only'};
const c=await catalog(root,sources);
const {skills,roles,adapters,automaticSkillDiscovery,coordinateRegistered}=c;
const stageTitles = ['Briefing e decisões','Roteiro e idiomas','Referências visuais','Bíblias e continuidade','Áudio e vozes','Storyboard e animatic','Piloto e testes','Geração de planos','Montagem e revisão','Entrega e qualidade'];
const stageDescriptions = ['Escopo, aprovações, decisões e pesquisa.','Texto em inglês, IDs de falas e traduções.','Originais, seleção, sintéticos, identidade, mesa e figurino.','Regras de personagem, câmera, luz e cenas.','Falas, testes de voz e pistas de som.','Fontes editáveis, keyframes, planos e animatics.','Clipes de teste, variantes e revisões.','Solicitações, respostas do provedor e takes com proveniência.','Timelines, legendas, revisões e candidatos à imagem final.','Masters, legendas, pistas e revisão final.'];
const stages = inputs['docs/WORKSPACE.md'].split('\n').filter(l=>/^- `\d\d_/.test(l)).map((line,i)=>({path:`projects/${workspace.activeFilm}/`+line.match(/`([^`]+)`/)[1],title:stageTitles[i],description:stageDescriptions[i],order:String(i).padStart(2,'0')}));
const moves = inputs['projects/andre-time-travel/tasks/README.md'].split('\n').filter(l=>/^\| `tasks\//.test(l)).map(l=>{const paths=[...l.matchAll(/`([^`]+)`/g)].map(m=>m[1]);return {from:paths[0],to:paths[1]};});
for(const move of moves) await verifyPath(root,`projects/${workspace.activeFilm}/${move.to}`);
const paths = [
 ['Regras do workspace','AGENTS.md','Contrato obrigatório de escopo, autoridade e revisão.'],
 ['Retomada do filme',`projects/${workspace.activeFilm}/memory/STATE.md`,'Ponto único de retomada; conferir com os registros oficiais.'],
 ['Quadro oficial',`projects/${workspace.activeFilm}/tasks/board.json`,'T01–T21: única fonte de situação das tarefas de produção.'],
 ['Especificações',`projects/${workspace.activeFilm}/tasks/specs/`,'O que entregar e como verificar cada tarefa.'],
 ['Planos e workflow',`projects/${workspace.activeFilm}/tasks/plans/`,'Mapas e planos datados; W01–W68 detalham o trabalho.'],
 ['Plano de execução',`projects/${workspace.activeFilm}/tasks/execution-plan-v1/`,'Planejamento detalhado; não constitui execução ou aceite.'],
 ['Aprovações',`projects/${workspace.activeFilm}/00_brief/approvals.json`,'Escopos de aprovação registrados pelo produtor.'],
 ['Decisões',`projects/${workspace.activeFilm}/00_brief/decisions/`,'Registros D: referência para as escolhas do filme.'],
 ['Catálogo de mídia',assetPath,'IDs estáveis, caminhos canônicos, hashes e proveniência; os indicadores do registro não aprovam novos usos.'],
 ['Papéis','agents/registry.json','Responsabilidades e skills; não indica sessões ativas.'],
 ['Skills','skills/registry.json','Procedimento local e vínculos com fontes compartilhadas.'],
 ['Entregas entre agentes','shared/templates/agent-handoff-v2.json','Escopo, hashes, verificações, limites e próximo responsável.'],
 ['Série e continuação','series/andre-time-travel/series.json','Regras reutilizáveis; sem herdar aprovações ou gastos.'],
].map(([title,path,description])=>({title,path,description}));
for(const item of [...paths,...stages]) await verifyPath(root,item.path);

unique(moves,'from'); unique(stages,'path');
const data={schemaVersion:1,projectId:workspace.activeFilm,sources,assetCatalog,stages,paths,moves,skills,roles,adapters,automaticSkillDiscovery,coordinateRegistered};
console.log(JSON.stringify(await emit(data,await outputPath(site,resolve(site,'data/workspace-reference.json')),root,check)));
