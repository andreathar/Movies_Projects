// Synthetic execution of two pure validators from the installed official bundle.
// This never runs CLI entrypoints, provider calls, uploads, authentication or generation.
import {readFileSync} from 'node:fs';
import vm from 'node:vm';
import assert from 'node:assert/strict';
const source=readFileSync(process.argv[2],'utf8');
const section=(start,end)=>source.slice(source.indexOf('function '+start+'('),source.indexOf('function '+end+'('));
const validators=section('parseCombinedItemCap','normalizeModel')+section('assertCombinedItemCap','tailSlotName');
const ctx={ValidationError:Error,msg:(_cn,en)=>en,camelOf:n=>n.replace(/_([a-z])/g,(_m,c)=>c.toUpperCase())};
vm.createContext(ctx);vm.runInContext(validators,ctx,{timeout:1000});
const cap={maxItems:15,arguments:['elements'],inputPrefixes:['image_','video_','audio_']};
ctx.assertCombinedItemCap({model:'fixture',combinedItemCap:cap},['image_1','audio_1'],{elements:'[{"id":"123"}]'});
assert.throws(()=>ctx.assertCombinedItemCap({model:'fixture',combinedItemCap:{...cap,maxItems:2}},['image_1','audio_1'],{elements:'[{"id":"123"}]'}),/combined reference limit/);
const conditional={maxItems:1,arguments:[],inputPrefixes:['image_'],whenAnyInputPrefixes:['video_']};
ctx.assertCombinedItemCap({model:'fixture',combinedItemCaps:[conditional]},['image_1','image_2']);
assert.throws(()=>ctx.assertCombinedItemCap({model:'fixture',combinedItemCaps:[conditional]},['image_1','image_2','video_1']),/combinedItemCaps/);
ctx.assertCombinedItemCap({model:'fixture',combinedItemCaps:[{...conditional,whenNoneInputPrefixes:['audio_']}]},['image_1','image_2','video_1','audio_1']);
assert.throws(()=>ctx.parseCombinedItemCap({...cap,whenAnyInputPrefixes:12}),/invalid/);
assert.throws(()=>ctx.parseCombinedItemCaps('bad'),/must be an array/);
console.log(JSON.stringify({type:'synthetic_vendor_validators',checks:7,passed:7,paidCalls:0,uploads:0,networkCalls:0}));
