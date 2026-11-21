"""Aggregates for the dashboard prototype and insight tables. SIMULATED DATA. Tasks/events/users are SUPPLIED data; rewards are ANALYST-GENERATED stand-ins."""
import pandas as pd, numpy as np, json
import profile_data as P, generate_supplementary as G
T=P.sets['T02.Task_Activity'].copy(); EV=pd.read_csv('/home/claude/repo/data/cleaned/events_cleaned.csv',parse_dates=['event_datetime'])
U=P.sets['T02.Users'].copy(); S=P.sets['T02.Sessions'].copy(); R=G.SIM['Rewards'].copy()
d=lambda s:pd.to_datetime(s).dt.strftime('%Y-%m-%d')
T['day']=d(T.task_started_at.fillna(T.task_viewed_at)); EV['day']=d(EV.event_datetime); S['day']=d(S.session_start); R['day']=d(R.reward_created_at)
U['day']=d(U.registration_datetime)
days=sorted(set(T.day)|set(EV.day)|set(S.day)|set(R.day)|set(U.day)); di={x:i for i,x in enumerate(days)}
cats=sorted(T.task_category.unique()); ci={x:i for i,x in enumerate(cats)}
stat=['Completed','Abandoned','Failed','Pending']; si={x:i for i,x in enumerate(stat)}
units=['VE','XP','Gems','Tokens']; ui={x:i for i,x in enumerate(units)}
rst=['Credited','Pending','Reversed','Corrected']; ri={x:i for i,x in enumerate(rst)}
feats=sorted(EV.feature_name.unique()); fi={x:i for i,x in enumerate(feats)}
dau=EV.groupby('day').user_id.nunique().reindex(days,fill_value=0).tolist()
sess=S.groupby('day').size().reindex(days,fill_value=0).tolist()
newu=U.groupby('day').size().reindex(days,fill_value=0).tolist()
tk=T.groupby(['day','task_category','task_status']).size().reset_index(name='n'); tk=[[di[r.day],ci[r.task_category],si[r.task_status],int(r.n)] for r in tk.itertuples()]
fr=T[T.task_status.isin(['Failed','Abandoned'])].copy(); fr['failure_reason']=fr.failure_reason.fillna('Not recorded')
reasons=sorted(fr.failure_reason.unique()); rsi={x:i for i,x in enumerate(reasons)}
fg=fr.groupby(['day','task_category','failure_reason']).size().reset_index(name='n'); fg=[[di[r.day],ci[r.task_category],rsi[r.failure_reason],int(r.n)] for r in fg.itertuples()]
rw=R.groupby(['day','reward_unit','reward_status']).agg(n=('reward_id','size'),amt=('reward_amount','sum')).reset_index(); rw=[[di[r.day],ui[r.reward_unit],ri[r.reward_status],int(r.n),int(r.amt)] for r in rw.itertuples()]
fe=EV.groupby(['day','feature_name']).size().reset_index(name='n'); fe=[[di[r.day],fi[r.feature_name],int(r.n)] for r in fe.itertuples()]
DASH=dict(days=days,cats=cats,stat=stat,units=units,rst=rst,feats=feats,reasons=reasons,dau=dau,sess=sess,newu=newu,tk=tk,fg=fg,rw=rw,fe=fe)
json.dump(DASH,open('/home/claude/repo/scripts/dash.json','w'),separators=(',',':'))
if __name__=='__main__':
    print(len(days),days[0],days[-1],len(json.dumps(DASH,separators=(',',':')))//1024,'KB')
    c=T.groupby('task_category').task_status.value_counts().unstack(fill_value=0); c['n']=c.sum(axis=1); c['compl%']=(100*c.Completed/c.n).round(1); c['aband%']=(100*c.Abandoned/c.n).round(1); c['fail%']=(100*c.Failed/c.n).round(1)
    print(c.sort_values('compl%').to_string())
    print(T.task_status.value_counts(normalize=True).round(3).to_dict())
    print(fr.failure_reason.value_counts().to_dict())
    print(EV.groupby('feature_name').user_id.nunique().sort_values().to_dict())
    print('active users total',EV.user_id.nunique(),'of',len(U),'reward status',R.reward_status.value_counts().to_dict())
    print(R[R.reward_status=='Credited'].groupby('reward_unit').reward_amount.agg(['count','sum']).to_dict())
    print('pending rewards among Completed activities', R[(R.reward_status=='Pending')].activity_id.isin(T[T.task_status=='Completed'].activity_id).sum())
