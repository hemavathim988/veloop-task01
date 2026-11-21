"""Builds the revised report (page and Word versions) from report_template.md using facts.json (single source of truth)."""
import json,re,subprocess,os
F=json.load(open('/home/claude/repo/scripts/facts.json')); T=open('/home/claude/repo/scripts/report_template.md').read()
k={'n_areas','n_features','n_events','n_fields','n_entities','n_kpis','n_assume','n_backlog','n_gaps','n_proposed_seen','n_dq_checks','n_dq_found','n_dq_passed','n_sq_checks','n_sq_planted'}
rep={x:str(F[x]) for x in k}
rep.update(t_sup=F['test']['Supplied data'],t_par=F['test']['Partly supplied'],t_sub=F['test']['Stand-in data only'],t_nod=F['test']['No data'],
 s_rew=f"{F['sizes']['rewards']:,}",s_wal=f"{F['sizes']['wallet']:,}",s_wd=f"{F['sizes']['withdrawals']:,}",s_ref=f"{F['sizes']['referrals']:,}",
 g_user=F['kpi_groups']['User'],g_eng=F['kpi_groups']['Engagement'],g_rew=F['kpi_groups']['Reward'],g_wal=F['kpi_groups']['Wallet'],g_wd=F['kpi_groups']['Withdrawal'],g_ref=F['kpi_groups']['Referral'],g_sup=F['kpi_groups']['Support'])
def fill(t,er,pipe,wire):
    for a,b in rep.items(): t=t.replace('@@'+a+'@@',str(b))
    return t.replace('@@ER@@',er).replace('@@PIPE@@',pipe).replace('@@WIRE@@',wire)
wires=''.join(f"![Wireframe {n.replace('_',' ')}](diagrams/wireframe_{n}.png){{width=62%}}\n\n" for n in ['1_Executive_Overview','2_User_Analytics','3_Engagement','4_Rewards','5_Wallet','6_Withdrawals','7_Referrals'])
T=re.sub(r'(!\[[^\]]*\]\(diagrams/chart_[a-z_]+\.png\))',r'\1{width=85%}',T)
doc=fill(T,'![Logical ER diagram (proposed)](diagrams/er_diagram.png)','![Proposed data pipeline](diagrams/pipeline.png)',wires)
assert '@@' not in doc
D='/home/claude/repo/docs/'
open(D+'VELOOP_Task01_Final_Report.md','w').write(doc)
subprocess.run(['pandoc',D+'VELOOP_Task01_Final_Report.md','-f','markdown','-o',D+'VELOOP_Task01_Final_Report.docx','--resource-path='+D],check=True)
css="""<style>:root{--bg:#fff;--tx:#1c2430;--mu:#5b6676;--ac:#1f3864;--bd:#d9dfe8;--bq:#fdecec;color-scheme:light;box-sizing:border-box;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#10151d;--tx:#e6ebf2;--mu:#9aa6b6;--ac:#8fb0ee;--bd:#2a3442;--bq:#3a1d1d;color-scheme:dark}}
:root[data-theme="dark"]{--bg:#10151d;--tx:#e6ebf2;--mu:#9aa6b6;--ac:#8fb0ee;--bd:#2a3442;--bq:#3a1d1d;color-scheme:dark}
html{scroll-padding-top:env(safe-area-inset-top,0px)}body{background:var(--bg);color:var(--tx);font:16px/1.55 system-ui,-apple-system,"Segoe UI",Arial,sans-serif;max-width:960px;margin:0 auto;padding:16px}
h1,h2,h3{color:var(--ac);line-height:1.25}h2{border-bottom:2px solid var(--bd);padding-bottom:4px;margin-top:34px}
blockquote{background:var(--bq);border-left:4px solid #c00000;margin:12px 0;padding:6px 14px;border-radius:4px}
.tw{overflow-x:auto}table{border-collapse:collapse;font-size:14px;width:100%}th,td{border:1px solid var(--bd);padding:6px 8px;vertical-align:top;text-align:left}th{background:var(--ac);color:#fff}
img{max-width:100%;height:auto;background:#fff;border-radius:6px}code{font-size:13px}</style>"""
open('/tmp/hdr.html','w').write('<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">'+css)
subprocess.run(['pandoc',D+'VELOOP_Task01_Final_Report.md','-f','markdown','-s','--embed-resources','--resource-path='+D,'--metadata','title=VELOOP Task 01 — Revised Report','-H','/tmp/hdr.html','-o','/mnt/user-data/outputs/VELOOP_Task01_Report_v2.html'],check=True)
h=open('/mnt/user-data/outputs/VELOOP_Task01_Report_v2.html').read()
h=h.replace('<table>','<div class="tw"><table>').replace('</table>','</table></div>')
h=re.sub(r'<header id="title-block-header">.*?</header>','',h,flags=re.S)
open('/mnt/user-data/outputs/VELOOP_Task01_Report_v2.html','w').write(h)
print(len(doc.split()),'words;',os.path.getsize('/mnt/user-data/outputs/VELOOP_Task01_Report_v2.html')//1024,'KB html')
