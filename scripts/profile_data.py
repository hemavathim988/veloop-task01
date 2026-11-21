"""VELOOP Task 01 - simulated data profiling & data quality audit.
SIMULATED DATA - CREATED FOR ANALYTICAL TESTING. Not actual VELOOP data."""
import pandas as pd, numpy as np, re, sys
UP='/mnt/user-data/uploads/'
F1=UP+'VELoop_Rewards_Data_01.xlsx'; F2=UP+'VELOOP_Simulated_User_Behavior_1000.xlsx'
x1=pd.ExcelFile(F1); x2=pd.ExcelFile(F2)
sets={
 'T01.Users_Clean':x1.parse('Users_1000_Clean'),
 'T01.Users_Messy':x1.parse('Users_Messy_Audit'),
 'T02.Users':x2.parse('01_Users_1000'),
 'T02.Sessions':x2.parse('02_Sessions'),
 'T02.Feature_Events':x2.parse('03_Feature_Events'),
 'T02.Daily_Activity':x2.parse('04_Daily_Activity'),
 'T02.Task_Activity':x2.parse('05_Task_Activity'),
 'T02.Milestones':x2.parse('06_Milestones'),
 'T02.Event_Audit':x2.parse('10_Event_Data_Quality_Audit'),
}
idcols={'user_id','session_id','event_id','activity_id','task_id'}
prof=[];cols=[]
for n,d in sets.items():
    dt=[c for c in d.columns if 'date' in c.lower() or c.endswith('_at') or c.endswith('_start') or c.endswith('_end')]
    rng=''
    parsed=[pd.to_datetime(d[c],errors='coerce') for c in dt]
    if parsed:
        mn=min(p.min() for p in parsed); mx=max(p.max() for p in parsed); rng=f'{mn} to {mx}'
    prof.append(dict(dataset=n,records=len(d),columns=d.shape[1],date_range=rng,
        full_row_duplicates=int(d.duplicated().sum()),total_missing_cells=int(d.isna().sum().sum())))
    for c in d.columns:
        s=d[c]; r=dict(dataset=n,field=c,dtype=str(s.dtype),non_null=int(s.notna().sum()),missing=int(s.isna().sum()),
            missing_pct=round(100*s.isna().mean(),2),unique=int(s.nunique()),
            duplicate_values=int(s.dropna().duplicated().sum()) if c in idcols else '')
        if pd.api.types.is_numeric_dtype(s): r.update(min=s.min(),max=s.max(),mean=round(float(s.mean()),2))
        elif s.nunique()<=20: r['categories']='; '.join(f'{k}={v}' for k,v in s.value_counts(dropna=False).items())
        cols.append(r)
P=pd.DataFrame(prof); C=pd.DataFrame(cols)
# ---- relationship tests (J2)
rel=[]
def rt(child,ckey,parent,pkey):
    c=sets[child][ckey].dropna(); p=set(sets[parent][pkey].dropna())
    orphan=int((~c.isin(p)).sum())
    rel.append(dict(child=child,child_key=ckey,parent=parent,parent_key=pkey,child_rows=len(c),orphan_rows=orphan,
        result='PASS' if orphan==0 else 'FAIL'))
for ch in ['T02.Sessions','T02.Feature_Events','T02.Daily_Activity','T02.Task_Activity','T02.Milestones']:
    rt(ch,'user_id','T02.Users','user_id')
rt('T02.Feature_Events','session_id','T02.Sessions','session_id')
rt('T02.Task_Activity','session_id','T02.Sessions','session_id')
rt('T02.Milestones','session_id','T02.Sessions','session_id')
rt('T01.Users_Messy','user_id','T01.Users_Clean','user_id')
for e in ['Rewards','Wallet','Withdrawals','Referrals']:
    rel.append(dict(child=e,child_key='user_id',parent='Users',parent_key='user_id',child_rows='n/a',orphan_rows='n/a',result='NOT SUPPLIED - tested on analyst-generated stand-in (see SIM_Relationships)'))
R=pd.DataFrame(rel)
# ---- data quality issues (K)
iss=[];n=[0]
def add(ds,field,typ,cnt,sev,logic,cause,fix,prev,owner):
    n[0]+=1; iss.append(dict(issue_id=f'DQ{n[0]:03d}',dataset=ds,field=field,issue_type=typ,records_affected=int(cnt),severity=sev,
      detection_logic=logic,likely_cause=cause,correction=fix,prevention=prev,owner=owner,status='Open'))
m=sets['T01.Users_Messy']
add('T01.Users_Messy','user_id','Duplicate ID (8 duplicated IDs, 16 rows involved; 8 excess rows)',m.user_id.duplicated().sum(),'Critical','user_id appears >1 time (rows involved)','Double ingestion / re-import','Keep latest valid record per user_id; log rejects','Unique constraint at ingestion','Data/Engineering')
for col in ['age','gender','city','registration_datetime','acquisition_source','primary_device','email_verification_status','onboarding_status']:
    add('T01.Users_Messy',col,'Unexpected null (isolated)',m[col].isna().sum(),'High' if col in('registration_datetime','acquisition_source') else 'Medium','null in a field that is non-null in Users_1000_Clean','Partial write / dropped property','Quarantine or backfill from source of record; never impute silently','Required-field validation at collection','Engineering')
rd=m.registration_datetime
nn=rd.notna()
parsed=pd.to_datetime(rd,errors='coerce')
mal=int((parsed.isna()&nn).sum())
add('T01.Users_Messy','registration_datetime','Malformed date (text, month=14: 2026-14-02 12:00)',mal,'High','non-null value that fails datetime parsing; column also mixes datetime/text types','DD-MM / MM-DD swap at source','Reject; request corrected value; parse to UTC','ISO-8601 + timezone validation at ingestion','Engineering')
add('T01.Users_Messy','last_login_datetime','Missing value',m.last_login_datetime.isna().sum(),'Medium','last_login null','Never logged in OR not tracked','Distinguish never-logged-in from untracked','Emit user_logged_in; default null semantics documented','Engineering')
add('T01.Users_Messy','referral_source_detail','Conditional null',m.referral_source_detail.isna().sum(),'Low','Null count vs acquisition_source=Referral','Expected for non-referral users','Validate: required only when source=Referral','Conditional validation rule','Data')
refmis=int(((m.acquisition_source=='Referral')&m.referral_source_detail.isna()).sum())
add('T01.Users_Messy','referral_source_detail','Conditional rule violation',refmis,'Medium','acquisition_source=Referral AND referral_source_detail null','Detail not captured','Make detail required for Referral','Conditional validation','Engineering')
for col in ['full_name','email','age','gender','city','state']:
    pass
# PII
add('T01.Users_Clean / T02.Users','full_name, email, gender, age, city','Unnecessary personal data',len(sets['T01.Users_Clean']),'High','Direct identifiers present in analytical dataset','Dataset designed with personal-looking attributes','Remove/pseudonymise in analytics layer; keep user_id only','Data minimisation; restricted raw zone','Data Governance')
e=sets['T02.Event_Audit']; ev=sets['T02.Feature_Events']
add('T02.Event_Audit','event_id','Duplicate event',e.event_id.duplicated().sum(),'Critical','Duplicate event_id','Retry/double fire','Deduplicate on event_id','Idempotent event_id','Engineering')
add('T02.Event_Audit','row_count','Row count differs from Feature_Events',len(e)-len(ev),'Medium','len(audit)-len(events)','Injected audit rows','Reconcile','Pipeline row-count checks','Data')
cap=int((~e.feature_name.isin(set(ev.feature_name))).sum())
add('T02.Event_Audit','feature_name','Inconsistent capitalisation/naming',cap,'Medium','feature_name not in canonical Feature_Events vocabulary (e.g. missions, wallet, daily reward)','Different producers','Standardise to controlled vocabulary','Allowed-values list','Engineering')
ws=int((e.event_status!=e.event_status.str.strip()).sum())
add('T02.Event_Audit','event_status','Trailing space / inconsistent value ("success " vs "Success")',ws,'Low','regex ^\\s|\\s$','Manual entry','TRIM at transform','Trim at ingestion','Data')
for c in e.columns:
    if e[c].isna().sum(): add('T02.Event_Audit',c,'Missing value',e[c].isna().sum(),'High' if c in('event_id','user_id','event_datetime') else 'Medium','null count','Dropped property','Reject/flag','Required-field check','Engineering')
for c in ['event_datetime']:
    pr=pd.to_datetime(e[c],errors='coerce'); k=int(pr.isna().sum()-e[c].isna().sum())
    if k: add('T02.Event_Audit',c,'Malformed date',k,'High','unparseable non-null','Format drift','Reject','ISO-8601 check','Engineering')
orph=int((~e.user_id.isin(sets['T02.Users'].user_id)).sum())
add('T02.Event_Audit','user_id','Orphan record',orph,'Critical' if orph else 'Low','user_id not in Users','Unknown/deleted user','Quarantine','Referential check','Data')
sess=sets['T02.Sessions']
neg=int((sess.session_duration_seconds<0).sum()); bad_t=int((sess.session_end<sess.session_start).sum())
add('T02.Sessions','session_end','Impossible time order',bad_t,'High' if bad_t else 'Low','session_end < session_start','Clock/timezone issue','Reject','start<=end rule','Engineering')
t=sets['T02.Task_Activity']
imp=int(((t.task_status=='Completed')&t.task_completed_at.isna()).sum())
add('T02.Task_Activity','task_completed_at','Impossible state: Completed without completion time',imp,'High' if imp else 'Low','status=Completed AND completed_at null','State not stamped','Backfill/flag','State machine validation','Engineering')
imp2=int(((t.task_status!='Completed')&t.task_completed_at.notna()).sum())
add('T02.Task_Activity','task_completed_at','Impossible state: completion time on non-completed task',imp2,'High' if imp2 else 'Low','status!=Completed AND completed_at not null','State error','Flag','State machine validation','Engineering')
imp3=int(((t.reward_status=='Credited')&(t.task_status!='Completed')).sum())
add('T02.Task_Activity','reward_status','Reward credited without completed task',imp3,'Critical' if imp3 else 'Low','reward Credited AND task not Completed','Validation gap','Investigate','Reward only after validated completion','Engineering')
oo=int((t.task_started_at<t.task_viewed_at).sum())
add('T02.Task_Activity','task_started_at','Impossible time order (started before viewed)',oo,'High' if oo else 'Low','started<viewed','Clock skew','Flag','Monotonic timestamps','Engineering')
dupact=int(t.activity_id.duplicated().sum())
add('T02.Task_Activity','activity_id','Duplicate ID',dupact,'Critical' if dupact else 'Low','duplicate activity_id','Re-ingestion','Dedupe','Unique key','Engineering')
Q=pd.DataFrame(iss)
# ---- extra stats
extra={}
extra['t02_task_status']=t.task_status.value_counts(dropna=False).to_dict()
extra['t02_reward_status']=t.reward_status.value_counts(dropna=False).to_dict()
extra['t02_failure_reason']=t.failure_reason.value_counts(dropna=False).to_dict()
extra['t02_session_status']=sess.session_status.value_counts(dropna=False).to_dict()
extra['t02_event_status']=ev.event_status.value_counts(dropna=False).to_dict()
extra['t02_account_status']=sets['T02.Users'].account_status.value_counts().to_dict()
if __name__=='__main__':
    pd.set_option('display.width',250,'display.max_columns',30,'display.max_colwidth',60)
    print(P.to_string()); print(R.to_string()); print(Q[['issue_id','dataset','field','issue_type','records_affected','severity']].to_string())
    for k,v in extra.items(): print(k,v)
    print('T02 events dup ids',ev.event_id.duplicated().sum(),'audit extra ids',set(e.event_id)-set(ev.event_id).__len__() if False else len(set(e.event_id)-set(ev.event_id)))
    print('T02 users overlap with T01 users', sets['T02.Users'].user_id.isin(sets['T01.Users_Clean'].user_id).mean())
    a=sets['T02.Users'].merge(sets['T01.Users_Clean'],on='user_id',suffixes=('_2','_1'))
    print('same registration dt',(a.registration_datetime_1==a.registration_datetime_2).mean(),'same name',(a.full_name_1==a.full_name_2).mean())
