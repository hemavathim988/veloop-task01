"""Charts for report and presentation. SIMULATED DATA; reward chart uses analyst-generated stand-in data."""
import json, matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt, numpy as np, pandas as pd
OUT='/home/claude/repo/docs/diagrams/'
D=json.load(open('/home/claude/repo/scripts/dash.json')); F=json.load(open('/home/claude/repo/scripts/facts.json'))
N='#1F3864';B2='#2E75B6';L='#9DC3E6';O='#C55A11';G='#548235';Y='#BF9000';GR='#7F7F7F'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'axes.spines.top':False,'axes.spines.right':False})
def foot(ax,t='SIMULATED DATA — not actual VELOOP data'):
    ax.figure.text(0.01,0.01,t,color='#C00000',fontsize=8)
# 1 DAU
days=pd.to_datetime(D['days']); dau=np.array(D['dau']); r7=pd.Series(dau).rolling(7,min_periods=1).mean()
fig,ax=plt.subplots(figsize=(10,4.2)); ax.plot(days,dau,color=L,lw=1,label='Daily active users'); ax.plot(days,r7,color=N,lw=2.4,label='7-day average'); ax.set_title('Daily active users (supplied simulated events, after cleaning)',loc='left',weight='bold'); ax.legend(frameon=False); ax.set_ylabel('Unique users'); foot(ax); fig.tight_layout(rect=(0,.03,1,1)); fig.savefig(OUT+'chart_dau.png',dpi=130); plt.close(fig)
# 2 task outcomes by category (%)
cats=D['cats']; stat=D['stat']; M=np.zeros((len(cats),4))
for d,c,s,n in D['tk']: M[c,s]+=n
P=100*M/M.sum(axis=1,keepdims=True); o=np.argsort(P[:,0])
fig,ax=plt.subplots(figsize=(10,4.6)); left=np.zeros(len(cats)); cols=[G,Y,O,GR]
for j in range(4):
    ax.barh([cats[i] for i in o],P[o,j],left=left,color=cols[j],label=stat[j]); left+=P[o,j]
for k,i in enumerate(o): ax.text(1.5,k,f'{P[i,0]:.1f}% completed',va='center',color='white',fontsize=9,weight='bold')
ax.set_xlim(0,100); ax.set_xlabel('% of attempts'); ax.set_title('Task outcomes by category: near-uniform in the simulated data',loc='left',weight='bold'); ax.legend(ncol=4,frameon=False,loc='lower center',bbox_to_anchor=(.5,-.28)); foot(ax); fig.tight_layout(rect=(0,.03,1,1)); fig.savefig(OUT+'chart_tasks.png',dpi=130); plt.close(fig)
# 3 rewards by unit/status (stand-in)
U=D['units']; R=D['rst']; A=np.zeros((4,4))
for d,u,s,n,m in D['rw']: A[u,s]+=m
fig,ax=plt.subplots(figsize=(10,4.2)); bot=np.zeros(4); cols=[N,L,O,Y]
for j in range(4): ax.bar(U,A[:,j],bottom=bot,color=cols[j],label=R[j]); bot+=A[:,j]
ax.set_ylabel('Amount (units are never summed together)'); ax.set_title('Reward amount by unit and status — ANALYST-GENERATED STAND-IN DATA',loc='left',weight='bold',fontsize=11); ax.legend(frameon=False); foot(ax,'ANALYST-GENERATED STAND-IN DATA — testing only'); fig.tight_layout(rect=(0,.03,1,1)); fig.savefig(OUT+'chart_rewards.png',dpi=130); plt.close(fig)
# 4 before/after cleaning
ba=pd.read_csv if False else None
labs=['Users rows','Duplicate user IDs','Events rows (÷1000)','Duplicate event IDs','Non-canonical text cells','Distinct feature names']
bef=[F['users_raw'],8,F['events_raw']/1000,10,9,20]; aft=[F['users_clean'],0,F['events_clean']/1000,0,0,15]
x=np.arange(len(labs)); fig,ax=plt.subplots(figsize=(10,4.4)); ax.bar(x-.2,bef,.4,color=O,label='Before cleaning'); ax.bar(x+.2,aft,.4,color=N,label='After cleaning')
for i in range(len(labs)):
    ax.text(x[i]-.2,bef[i],f'{bef[i]:g}',ha='center',va='bottom',fontsize=9); ax.text(x[i]+.2,aft[i],f'{aft[i]:g}',ha='center',va='bottom',fontsize=9)
ax.set_xticks(x); ax.set_xticklabels(labs,rotation=18,ha='right'); ax.set_yscale('symlog',linthresh=10); ax.set_title('Data cleaning: before and after (supplied simulated sheets)',loc='left',weight='bold'); ax.legend(frameon=False); foot(ax); fig.tight_layout(rect=(0,.03,1,1)); fig.savefig(OUT+'chart_cleaning.png',dpi=130); plt.close(fig)
# 5 KPI testability
t=F['test']; labs=['Supplied data','Partly supplied','Stand-in data only','No data']; vals=[t[k] for k in labs]
fig,ax=plt.subplots(figsize=(10,3.6)); ax.barh(labs[::-1],vals[::-1],color=[G,Y,O,GR][::-1]);
for i,v in enumerate(vals[::-1]): ax.text(v+.3,i,str(v),va='center',weight='bold')
ax.set_xlabel('Number of KPIs (46 in catalogue)'); ax.set_title('How many KPIs can be tested with the data provided',loc='left',weight='bold'); foot(ax); fig.tight_layout(rect=(0,.03,1,1)); fig.savefig(OUT+'chart_kpi_testability.png',dpi=130); plt.close(fig)
# 6 event coverage
seen=F['n_proposed_seen']; tot=F['n_events']
fig,ax=plt.subplots(figsize=(10,2.8)); ax.barh(['Proposed events'],[seen],color=G,label=f'Present in supplied data ({seen})'); ax.barh(['Proposed events'],[tot-seen],left=[seen],color=O,label=f'Not present ({tot-seen})')
ax.set_xlim(0,tot); ax.legend(frameon=False,ncol=2,loc='upper center',bbox_to_anchor=(.5,-.25)); ax.set_title(f'Event coverage: {seen} of {tot} proposed events appear in the supplied event list',loc='left',weight='bold'); foot(ax); fig.tight_layout(rect=(0,.03,1,1)); fig.savefig(OUT+'chart_event_coverage.png',dpi=130); plt.close(fig)
print('charts ok')
