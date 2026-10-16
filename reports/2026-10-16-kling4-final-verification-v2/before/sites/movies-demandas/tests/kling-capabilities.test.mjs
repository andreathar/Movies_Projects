import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
const read=p=>readFileSync(new URL(p,import.meta.url),'utf8');
test('Kling capability export separates current interface, announced features and approval scopes',()=>{
 const data=JSON.parse(read('../data/workspace-reference.json')).klingCapabilities;
 assert.equal(data.provider,'kling-global');assert.equal(data.cli.version,'0.2.1');
 assert.equal(data.generationTested,false);assert.equal(data.price.status,'unknown');assert.equal(data.automaticFallback,false);
 assert.deepEqual(data.routes.map(r=>r.tool).sort(),['image_to_video','omni_ref_video','text_to_video']);
 for(const route of data.routes){assert.equal(route.model,'kling-video-v4_0');assert.deepEqual(route.parameters.find(p=>p.name==='resolution').allowedValues,['720p','1080p']);}
 const omni=data.routes.find(r=>r.tool==='omni_ref_video');assert.deepEqual(omni.parameters.find(p=>p.name==='prefer_multi_shots').allowedValues,['true']);
 const keyframes=data.routes.find(r=>r.tool==='image_to_video');assert.equal(keyframes.parameters.some(p=>p.name==='elements'),false);
 assert.ok(data.notes.some(n=>n.includes('composition only')));
 assert.ok(data.unavailable.includes('10_bit_hdr_coming_soon'));
 const component=read('../app/kling-capabilities.tsx');assert.ok(component.includes('reference.klingCapabilities'));assert.ok(component.includes('aprovação de composição'));
});
