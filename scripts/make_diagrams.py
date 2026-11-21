"""Creates ER diagram, pipeline diagram and 7 dashboard wireframes (PNG). Proposed designs, not existing systems."""
import subprocess, matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
OUT='/home/claude/repo/docs/diagrams/'
ent={
'USERS':['PK user_id','registered_at','acquisition_source','account_status','consent_status'],
'SESSIONS':['PK session_id','FK user_id','session_start','session_end','session_status'],
'FEATURE_EVENTS':['PK event_id','FK user_id','FK session_id','event_name','feature_name','event_timestamp'],
'TASKS':['PK task_id','task_category','provider'],
'TASK_ACTIVITY':['PK activity_id','FK user_id','FK task_id','FK session_id','task_status','failure_reason'],
'REWARDS':['PK reward_id','FK user_id','FK activity_id','reward_amount','reward_unit','reward_status','original_reward_id'],
'WALLET_TRANSACTIONS':['PK transaction_id','FK user_id','transaction_type','amount, unit','reference_id','FK related_transaction_id'],
'WITHDRAWALS':['PK withdrawal_id','FK user_id','requested_amount','method','requested_at','final_at','withdrawal_status'],
'REFERRALS':['PK referral_id','FK referrer_user_id','FK referred_user_id','created_at','referral_status'],
'SUPPORT_TICKETS':['PK ticket_id','FK user_id','issue_category','ticket_status'],
}
rel=[('USERS','SESSIONS','1 : N'),('USERS','FEATURE_EVENTS','1 : N'),('SESSIONS','FEATURE_EVENTS','1 : N'),('USERS','TASK_ACTIVITY','1 : N'),('TASKS','TASK_ACTIVITY','1 : N'),
('TASK_ACTIVITY','REWARDS','1 : 0..1'),('USERS','REWARDS','1 : N'),('REWARDS','WALLET_TRANSACTIONS','1 : N (credit/reversal/adjustment)'),('USERS','WALLET_TRANSACTIONS','1 : N'),
('USERS','WITHDRAWALS','1 : N'),('USERS','REFERRALS','1 : N (referrer)'),('USERS','SUPPORT_TICKETS','1 : N')]
g='digraph ER{rankdir=LR;nodesep=.5;ranksep=1.1;node[shape=plaintext,fontname="Arial"];edge[fontname="Arial",fontsize=10,color="#1F3864"];\n'
for n,f in ent.items():
    rows=''.join(f'<TR><TD ALIGN="LEFT" PORT="{i}">{x}</TD></TR>' for i,x in enumerate(f))
    g+=f'{n}[label=<<TABLE BORDER="1" CELLBORDER="0" CELLSPACING="0" CELLPADDING="4"><TR><TD BGCOLOR="#1F3864"><FONT COLOR="white"><B>{n}</B></FONT></TD></TR>{rows}</TABLE>>];\n'
for a,b,l in rel: g+=f'{a}->{b}[label="{l}",arrowhead=crow];\n'
g+='WALLET_TRANSACTIONS->WALLET_TRANSACTIONS[label="reverses / corrects",style=dashed];\nWALLET_TRANSACTIONS->WITHDRAWALS[label="funds (via reference_id)",style=dashed];\n}'
open(OUT+'er.dot','w').write(g); subprocess.run(['dot','-Tpng','-Gdpi=130',OUT+'er.dot','-o',OUT+'er_diagram.png'],check=True)
p='''digraph P{rankdir=LR;node[shape=box,style="rounded,filled",fillcolor="#DCE6F2",fontname="Arial"];edge[fontname="Arial",fontsize=10];
A[label="VELOOP app & backend\\n(event producers)"];B[label="Application events\\n(event_id, schema_version)"];C[label="Raw storage\\n(immutable)"];
D[label="Validation\\n(required, types, vocab, dedup)"];Q[label="Quarantine table\\n(rejects + reason)",fillcolor="#F8D7DA"];E[label="Transformation\\n(trim, standardise, state checks)"];
F[label="Analytics layer\\n(entities + KPI views)"];G[label="BI dashboards"];H[label="Business reporting"];M[label="Monitoring: freshness, row counts, reject rate",fillcolor="#FFF3CD"];
A->B->C->D->E->F->G->H;D->Q[label="fail"];M->D[style=dashed];M->F[style=dashed];}'''
open(OUT+'pipeline.dot','w').write(p); subprocess.run(['dot','-Tpng','-Gdpi=130',OUT+'pipeline.dot','-o',OUT+'pipeline.png'],check=True)
# wireframes
WF={
'1_Executive_Overview':(['Active users (KPI-U02)','Task completion rate (E06)','Reward credits (R01)','Pending withdrawals (D03)'],[('Line: DAU trend',0),('Stacked bar: credit volume by unit (never summed)',1),('Funnel: referral created → converted',2),('Bar: withdrawal status mix',3)],'Date range | Platform | Feature'),
'2_User_Analytics':(['Registrations (U01)','Returning users (U03)','Inactive users (U06)','Verification rate (U08)'],[('Line: registrations by day',0),('Bar: acquisition source',1),('Bar: device / platform',2),('Table: lifecycle status',3)],'Date range | Source | Device'),
'3_Engagement':(['Feature adoption (E02)','Task starts (E04)','Completion rate (E06)','Abandonment (E07)'],[('Bar: feature usage',0),('Funnel: viewed → started → completed',1),('Bar: completion by task category',2),('Line: activity trend',3)],'Date range | Feature | Task category'),
'4_Rewards':(['Reward credits (R01)','Pending rewards (R03)','Reversal rate (R04)','Activity-to-credit (R07)'],[('Line: credits per day',0),('Bar: credits by feature',1),('Pie: status share',2),('Table: reversals by reason',3)],'Date range | Unit | Task category'),
'5_Wallet':(['Transactions (W01)','Credit volume (W02)','Redemptions (W03)','Reversal rate (W04)'],[('Line: transactions per day',0),('Bar: credits vs redemptions by unit',1),('Table: failed/reversed',2),('Reconciliation: rewards vs wallet',3)],'Date range | Unit | Type'),
'6_Withdrawals':(['Requests (D01)','Completed (D02)','Pending queue (D03)','Median processing h (D06)'],[('Line: requests vs completions',0),('Bar: status mix',1),('Histogram: processing time',2),('Bar: method distribution',3)],'Date range | Method | Status'),
'7_Referrals':(['Created (F01)','Registrations (F02)','Activations (F03)','Conversion rate (F04)'],[('Funnel: created → registered → activated → converted',0),('Line: referrals per week',1),('Bar: channel',2),('Table: expired / invalid referrals',3)],'Date range | Channel'),
}
for name,(tiles,charts,filt) in WF.items():
    fig,ax=plt.subplots(figsize=(11,7)); ax.set_xlim(0,11); ax.set_ylim(0,7); ax.axis('off')
    ax.add_patch(Rectangle((.1,6.3),10.8,.6,fc='#1F3864')); ax.text(.3,6.6,'Dashboard '+name.replace('_',' ',1).replace('_',' ')+'   (WIREFRAME — proposed)',color='w',va='center',fontsize=13,weight='bold')
    ax.add_patch(Rectangle((.1,5.65),10.8,.5,fc='#EEEEEE',ec='#999')); ax.text(.3,5.9,'Filters: '+filt,va='center',fontsize=10)
    for i,t in enumerate(tiles):
        x=.1+i*2.73; ax.add_patch(Rectangle((x,4.35),2.6,1.1,fc='#DCE6F2',ec='#1F3864')); ax.text(x+1.3,4.9,t,ha='center',va='center',fontsize=9,wrap=True); ax.text(x+1.3,4.55,'[value]',ha='center',fontsize=8,color='#555')
    for t,i in charts:
        x=.1+(i%2)*5.45; y=2.25-(i//2)*2.15
        ax.add_patch(Rectangle((x,y),5.35,1.95,fc='white',ec='#1F3864',ls='--')); ax.text(x+2.67,y+1.0,t,ha='center',va='center',fontsize=10)
    ax.text(.1,.05,'SIMULATED DATA — layout only; every visual uses the KPI definition in the KPI Catalogue.',fontsize=8,color='#C00000')
    fig.savefig(OUT+f'wireframe_{name}.png',dpi=110,bbox_inches='tight'); plt.close(fig)
print('done')
