import json,base64,urllib.request,os,sys,concurrent.futures as cf
H=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,H); from spec import C
K=os.environ.get('OPENROUTER_API_KEY') or sys.exit('Set OPENROUTER_API_KEY (OpenRouter key) to regenerate images.')
D=H; os.makedirs(D+"/pictograms",exist_ok=True); os.makedirs(D+"/storyboards",exist_ok=True)
V6=os.path.join(H,'style')
P=("Square 1:1 image. A single solid deep indigo-blue CIRCLE centered on a plain pure white background; everything drawn in pure white INSIDE the circle. "
 "Exact style of the Tokyo 2020 Olympic sport pictograms: simple and bold, strictly two colors (white and indigo), no gradients, no shading, no outlines, no text or letters, no halo. "
 "Minimalist geometric figures with round heads slightly separated from bodies, thick limbs, blank faces (except where the scene names a face mask/blindfold/sunglasses detail), max three human figures, side by side on one ground level, similar size. "
 "COSTUMES: Jesus ALWAYS wears a diagonal sash across his chest (a thin indigo band across his white body). "
 "STRICTLY two colors: white on deep indigo ONLY. No orange, no purple, no red, no other color anywhere, even if a reference photo has color. "
 "IDEALIZE: draw what each prop SYMBOLIZES, not the physical prop. A paper of sun rays = real rays of light bursting outward across the whole circle; a wave strip = real water/sea; a face mask = the person's actual face expression (skull face / smiling face); eye cover = the eyes themselves (X-ed out / bright open); a door board = a real door; grape cut-outs = a real vine with grapes; paper fish/loaves = real fish and bread; a ghost cut-out = a sickness cloud/ghost hovering. "
 "NEVER draw any stagehand, helper or support person: only the actors (max three). Anything a stagehand would hold or do happens by itself (a ghost floats on its own, a cloth unwinds on its own, light shines on its own). Exactly ONE scene, no collage. Scene: ")
S=("16:9 landscape stage BLOCKING storyboard sketch for a church youth skit. Loose black pencil line drawing on plain white paper, simple anatomically realistic human figures (mannequin-like, no detailed faces), a single horizontal stage floor line, actors side by side at the same depth with Jesus in the center. "
 "Jesus ALWAYS wears a diagonal cloth sash across his chest, colored RED (the only color besides the props). Draw handmade props so they clearly look like the reference prop photos, lightly colored like the real props. "
 "Draw ONLY the actors unless a stagehand is described below; then draw the stagehand as an extra figure in light GRAY with dashed outline. Use a few simple bold black arrows to show movement into the pose. "
 "No captions, no labels, no panel borders (text painted on props, if any, is fine). Exactly one frame. Scene: ")
def img(p):
    b=base64.b64encode(open(p,'rb').read()).decode(); ext='png' if p.endswith('png') else 'jpeg'
    return {"type":"image_url","image_url":{"url":f"data:image/{ext};base64,{b}"}}
def call(text,refs):
    content=[{"type":"text","text":text}]
    for label,p in refs: content+= [{"type":"text","text":label}, img(p)]
    err=''
    for m in ["google/gemini-3.1-flash-image","google/gemini-2.5-flash-image"]:
        for _ in range(2):
            try:
                r=urllib.request.Request("https://openrouter.ai/api/v1/chat/completions",json.dumps({"model":m,"modalities":["image","text"],"messages":[{"role":"user","content":content}]}).encode(),{"Authorization":"Bearer "+K,"Content-Type":"application/json"})
                d=json.load(urllib.request.urlopen(r,timeout=300)); return base64.b64decode(d['choices'][0]['message']['images'][0]['image_url']['url'].split(',',1)[1])
            except Exception as e: err=f"{m}: {e}"
    raise Exception(err)
STAFF={"03a":"stands behind the sick man holding the ghost cut-out up high above his head.","04b":"crouches behind the disciple slipping loaves and fish into the basket.","05a":"crouches below holding the wave strip up under Jesus' feet.","06b":"stands behind the healed man, swapping his blindfold.","09":"stands hidden right behind Jesus holding the big yellow sun-ray poster up high.","12b":"holds the loose white cloth, having pulled it off Jesus.","14":"kneels behind supporting the leaning figures' backs."}
def refs_for(c,kind):
    R=[]
    for f in c[5]:
        p=os.path.join(H,'ref',f)
        if f.startswith('fb_'): R.append(("REFERENCE (feedback page): the director's hand-drawn notes and sketch for this scene (Korean handwriting, red stroke = Jesus' sash). Follow her sketched idea for the staging; do NOT copy the page layout or text.",p))
        else: R.append(("REFERENCE (photo of the actual handmade prop): match its shape and look.",p))
    sty=os.path.join(V6,'pictograms','15.png') if kind=='p' else os.path.join(V6,'storyboards','15.png')
    if os.path.exists(sty): R.append(("STYLE REFERENCE ONLY (match drawing style, NOT the pose or content):",sty))
    return R
def job(kind,c):
    i=c[0]
    if kind=='p': b=call(P+c[1]+' (PICTOGRAM: ignore any stagehand mentioned above; do not draw them.)',refs_for(c,'p')); open(f"{D}/pictograms/{i}.png","wb").write(b)
    else:
        extra=(" Stagehand (gray, dashed): "+STAFF[i]) if i in STAFF else ""
        b=call(S+c[1]+extra,refs_for(c,'s')); open(f"{D}/storyboards/{i}.png","wb").write(b)
    return kind,i
only=sys.argv[1:]
jobs=[(k,c) for c in C for k in 'ps' if not only or f"{k}{c[0]}" in only or c[0] in only]
with cf.ThreadPoolExecutor(10) as ex:
    fs={ex.submit(job,*j):j for j in jobs}
    for f in cf.as_completed(fs):
        try: print("ok",f.result(),flush=True)
        except Exception as e: print("FAIL",fs[f][0],fs[f][1][0],str(e)[:200],flush=True)
