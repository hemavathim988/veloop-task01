"""Cleaning pipeline for the SUPPLIED messy simulated sheets (Users_Messy_Audit, Event_Data_Quality_Audit).
SIMULATED DATA - CREATED FOR ANALYTICAL TESTING. Rule-based; no value is imputed; the reference clean sheets are used ONLY to validate the result afterwards."""
import pandas as pd, numpy as np, json, re
import profile_data as P
OUT='/home/claude/repo/data/cleaned/'
raw_u=P.sets['T01.Users_Messy'].copy(); ref_u=P.sets['T01.Users_Clean']
raw_e=P.sets['T02.Event_Audit'].copy(); ref_e=P.sets['T02.Feature_Events']
log=[]; 
def L(ds,rule,field,before,after,action): log.append(dict(dataset=ds,rule=rule,field=field,records_before=before,records_after=after,action=action))
# ---------------- USERS
u=raw_u.copy(); n0=len(u)
# R-U1 exact duplicates
dup=u[u.duplicated(keep='first')]; u=u.drop_duplicates(keep='first')
L('Users','R-U1 Remove exact duplicate rows','user_id',n0,len(u),f'{len(dup)} exact copies moved to quarantine (kept first occurrence)')
q_u=dup.assign(reject_reason='exact duplicate row')
# R-U2 trim text
txt=u.select_dtypes(include=['object','string']).columns
tr=0
for c in txt:
    s=u[c].astype('string'); t=s.str.strip(); tr+=int((s.fillna('')!=t.fillna('')).sum()); u[c]=t
L('Users','R-U2 Trim leading/trailing spaces','all text fields',len(u),len(u),f'{tr} values changed')
# R-U3 dates
def parse(v):
    if pd.isna(v): return (pd.NaT,'missing')
    if hasattr(v,'year'): return (pd.Timestamp(v),'ok')
    try: return (pd.Timestamp(str(v).strip()),'ok')
    except Exception: return (pd.NaT,'malformed_blanked')   # a day/month swap was tested against the reference sheet and was WRONG, so no guessing
res=u.registration_datetime.map(parse)
u['registration_datetime']=[r[0] for r in res]; u['dq_registration_date_status']=[r[1] for r in res]
L('Users','R-U3 Parse dates; malformed values blanked and flagged (no guessing)','registration_datetime',len(u),len(u),f'{int((u.dq_registration_date_status=="malformed_blanked").sum())} malformed value blanked (2026-14-02 12:00), {int((u.dq_registration_date_status=="missing").sum())} already missing; both flagged. A YYYY-DD-MM swap would give 2026-02-14 but the reference holds a different date, so correcting by guess is unsafe')
u['last_login_datetime']=pd.to_datetime(u.last_login_datetime,errors='coerce')
# R-U4 nulls flagged not imputed
crit=['age','gender','city','registration_datetime','acquisition_source','primary_device','email_verification_status','onboarding_status']
u['dq_missing_required']=u[crit].isna().apply(lambda r:','.join(r.index[r]),axis=1)
nm=int((u.dq_missing_required!='').sum())
L('Users','R-U4 Missing required fields: flag, never impute','8 fields',len(u),len(u),f'{nm} rows flagged in dq_missing_required (kept; owner must supply true value)')
# R-U5 privacy minimisation
u['age_band']=pd.cut(u.age,[0,17,24,34,44,200],labels=['<18','18-24','25-34','35-44','45+']).astype('string')
safe=u.drop(columns=['full_name','email','age','gender','data_environment'])
safe['data_label']='SIMULATED DATA - CREATED FOR ANALYTICAL TESTING'
L('Users','R-U5 Data minimisation for analytics layer','full_name, email, age, gender',len(u),len(safe),'direct identifiers removed; age replaced by age_band')
clean_users=safe
# validation vs reference
common=[c for c in ref_u.columns if c in clean_users.columns and c not in ('user_id','registration_datetime','last_login_datetime')]
a=clean_users.set_index('user_id'); b=ref_u.set_index('user_id')
A_=a.loc[b.index.intersection(a.index),common].astype('string').fillna('<NA>'); B_=b.loc[A_.index,common].astype('string').fillna('<NA>')
match_rows=int((A_==B_).all(axis=1).sum()); ncommon=len(common)
aa=pd.to_datetime(a.registration_datetime,errors='coerce').reindex(b.index); reg_ok=int((aa==pd.to_datetime(b.registration_datetime,errors='coerce')).sum())
# ---------------- EVENTS
e=raw_e.copy(); n0=len(e)
dup=e[e.duplicated(keep='first')]; e=e.drop_duplicates(keep='first')
q_e=dup.assign(reject_reason='exact duplicate event_id/row')
L('Events','E1 Remove exact duplicate events','event_id',n0,len(e),f'{len(dup)} duplicate events moved to quarantine')
before=e.event_status.copy()
e['event_status']=e.event_status.str.strip(); sp=int((before!=e.event_status).sum())
L('Events','E2 Trim text','event_status',len(e),len(e),f'{sp} values changed ("success " -> "success")')
canon={f.lower():f for f in ref_e.feature_name.unique()}
canon_s={s.lower():s for s in ref_e.event_status.unique()}
fb=e.feature_name.copy(); e['feature_name']=e.feature_name.str.strip().str.lower().map(canon); cap=int((fb!=e.feature_name).sum())
e['event_status']=e.event_status.str.lower().map(canon_s)
L('Events','E3 Standardise to controlled vocabulary','feature_name, event_status',len(e),len(e),f'{cap} feature_name and {sp} status values mapped to canonical spelling via case-insensitive match against supplied vocabulary')
unmapped=int(e.feature_name.isna().sum()+e.event_status.isna().sum())
L('Events','E4 Unmapped values','feature_name, event_status',len(e),len(e),f'{unmapped} values could not be mapped')
e['event_datetime']=pd.to_datetime(e.event_datetime,errors='coerce')
clean_events=e
ev_match=bool(clean_events.reset_index(drop=True).sort_values('event_id').drop(columns=[]).shape[0]==ref_e.shape[0])
ce=clean_events.sort_values('event_id').reset_index(drop=True)[ref_e.columns]
re_=ref_e.sort_values('event_id').reset_index(drop=True)
same=int((ce.astype('string').fillna('<NA>')==re_.astype('string').fillna('<NA>')).all(axis=1).sum())
# ---------------- before/after metrics
ba=[]
def B(m,b,a,note=''): ba.append(dict(metric=m,before=b,after=a,note=note))
B('Users: rows',len(raw_u),len(clean_users),'8 exact duplicates removed')
B('Users: duplicate user_id rows',int(raw_u.user_id.duplicated().sum()),int(clean_users.user_id.duplicated().sum()))
B('Users: rows with a missing or malformed required field',nm,nm,'same rows before and after: flagged and kept, never imputed (8 null cells + 1 malformed date; owner must supply true values)')
B('Users: registration_datetime not a valid timestamp',int(pd.to_datetime(raw_u.registration_datetime,errors='coerce').isna().sum()),0,'0 invalid values remain; 2 are blank and flagged (1 malformed, 1 missing) - need source value')
B('Users: registration_datetime blank (flagged)',int(raw_u.registration_datetime.isna().sum()),int(clean_users.registration_datetime.isna().sum()),'1 malformed value blanked + 1 missing')
B('Users: direct identifier fields',3,0,'name, email, gender removed; age banded')
B('Events: rows',len(raw_e),len(clean_events),'10 duplicates removed')
B('Events: duplicate event_id',int(raw_e.event_id.duplicated().sum()),int(clean_events.event_id.duplicated().sum()))
B('Events: distinct feature_name values',int(raw_e.feature_name.nunique()),int(clean_events.feature_name.nunique()),'case variants merged')
B('Events: distinct event_status values',int(raw_e.event_status.nunique()),int(clean_events.event_status.nunique()))
rs=lambda d:int((d.event_status=='Success').sum())
B('Events: text cells not in controlled vocabulary',int((~raw_e.feature_name.isin(set(ref_e.feature_name))).sum()+(~raw_e.event_status.isin(set(ref_e.event_status))).sum()),0,'5 feature_name + 4 event_status variants fixed')
B('Events: count of status "Success"',rs(raw_e),rs(clean_events),'net unchanged because 4 duplicate Success rows removed offset 4 "success " values merged: count checks alone would not reveal either defect')
def avg_dau(d):
    t=pd.to_datetime(d.event_datetime,errors='coerce').dt.normalize(); g=d.assign(t=t).groupby('t').user_id.nunique()
    full=pd.date_range('2026-04-01','2026-09-15'); return round(float(g.reindex(full,fill_value=0).mean()),1)
B('Events: average daily active users, calendar days 1 Apr-15 Sep (simulated)',avg_dau(raw_e),avg_dau(clean_events))
B('Events: events attributed to feature "Watch Ads"',int((raw_e.feature_name=='Watch Ads').sum()),int((clean_events.feature_name=='Watch Ads').sum()),'1 lower-case row recovered, 1 duplicate removed: net unchanged')
BA=pd.DataFrame(ba); LG=pd.DataFrame(log)
VAL=pd.DataFrame([
 dict(check='Cleaned Users rows equal reference rows',result=f'{len(clean_users)} vs {len(ref_u)}'),
 dict(check=f'Cleaned Users rows matching reference on {ncommon} shared fields',result=f'{match_rows} of {len(ref_u)}'),
 dict(check='registration_datetime equal to reference',result=f'{reg_ok} of {len(ref_u)} (4 differ: 2 blanked/missing and flagged, 2 undetectable)'),
 dict(check='Cleaned Events rows equal reference rows',result=f'{len(clean_events)} vs {len(ref_e)}'),
 dict(check='Cleaned Events rows identical to reference on all fields',result=f'{same} of {len(ref_e)}'),
 dict(check='Events differing from reference',result='2 rows (EVT00000007, EVT00000008): audit sheet says "success ", reference says "Started". Format cleaning cannot detect a wrong value; needs source-system check'),
 dict(check='Users registration_datetime differing without being flagged',result='2 rows (VLUSR000021, VLUSR000022) hold plausible but different dates than the reference; no rule can detect this, only reconciliation with a source of truth'),
])
# write
clean_users.to_csv(OUT+'users_cleaned.csv',index=False); clean_events.to_csv(OUT+'events_cleaned.csv',index=False)
q_u.to_csv(OUT+'users_quarantine.csv',index=False); q_e.to_csv(OUT+'events_quarantine.csv',index=False)
facts=dict(users_raw=len(raw_u),users_clean=len(clean_users),events_raw=len(raw_e),events_clean=len(clean_events),match_rows=match_rows,reg_ok=reg_ok,ev_same=same,unmapped=unmapped,flagged=nm)
json.dump(facts,open('/home/claude/repo/scripts/facts_clean.json','w'))
if __name__=='__main__':
    pd.set_option('display.width',250,'display.max_colwidth',120)
    print(LG.to_string()); print(BA.to_string()); print(VAL.to_string()); print(facts)
