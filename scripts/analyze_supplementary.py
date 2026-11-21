"""Profiling, relationship tests, quality checks and KPI formula tests on the analyst-generated SIMULATED sets.
SIMULATED DATA - CREATED FOR ANALYTICAL TESTING. Results describe simulated data only."""
import pandas as pd, numpy as np
import generate_supplementary as G
import profile_data as P
S=G.SIM; U=G.users; Tk=G.T
sess=P.sets['T02.Sessions']; ev=P.sets['T02.Feature_Events']
# profile
prof=[];fld=[]
for n,d in S.items():
    dts=[c for c in d.columns if c.endswith('_at')]
    pr=[pd.to_datetime(d[c],errors='coerce') for c in dts]
    prof.append(dict(dataset='SIM.'+n,records=len(d),columns=d.shape[1],date_range=f"{min(p.min() for p in pr)} to {max(p.max() for p in pr)}",
      full_row_duplicates=int(d.duplicated().sum()),total_missing_cells=int(d.isna().sum().sum())))
    for c in d.columns:
        s=d[c]; r=dict(dataset='SIM.'+n,field=c,dtype=str(s.dtype),missing=int(s.isna().sum()),unique=int(s.nunique()))
        if pd.api.types.is_numeric_dtype(s): r.update(min=s.min(),max=s.max(),mean=round(float(s.mean()),2))
        elif s.nunique()<=12: r['categories']='; '.join(f'{k}={v}' for k,v in s.value_counts(dropna=False).items())
        fld.append(r)
PROF=pd.DataFrame(prof); FLD=pd.DataFrame(fld)
# relationships
rel=[]
def rt(ch,ck,pr,pk,cs,ps):
    c=cs[ck].dropna(); p=set(ps[pk].dropna()); o=int((~c.isin(p)).sum())
    rel.append(dict(child=ch,child_key=ck,parent=pr,parent_key=pk,child_rows=len(c),orphan_rows=o,result='PASS' if o==0 else 'FAIL'))
rt('SIM.Rewards','user_id','T02.Users','user_id',S['Rewards'],U)
rt('SIM.Rewards','activity_id','T02.Task_Activity','activity_id',S['Rewards'],Tk)
rt('SIM.Wallet_Transactions','user_id','T02.Users','user_id',S['Wallet_Transactions'],U)
rt('SIM.Wallet_Transactions','related_transaction_id','SIM.Wallet_Transactions','transaction_id',S['Wallet_Transactions'],S['Wallet_Transactions'])
rt('SIM.Withdrawals','user_id','T02.Users','user_id',S['Withdrawals'],U)
rt('SIM.Referrals','referrer_user_id','T02.Users','user_id',S['Referrals'],U)
rt('SIM.Referrals','referred_user_id','T02.Users','user_id',S['Referrals'],U)
REL=pd.DataFrame(rel)
# DQ checks: detected vs planted
R,W,WD,RF=S['Rewards'],S['Wallet_Transactions'],S['Withdrawals'],S['Referrals']
chk=[]
def c(i,ds,fld_,typ,cnt,planted,sev,logic,fix,prev,owner):
    chk.append(dict(issue_id=i,dataset=ds,field=fld_,issue_type=typ,records_affected=int(cnt),planted_in_generator=planted,severity=sev,detection_logic=logic,correction=fix,prevention=prev,owner=owner))
c('SQ001','SIM.Wallet_Transactions','transaction_id','Duplicate transaction ID',W.transaction_id.duplicated().sum(),6,'Critical','transaction_id appears more than once','Keep first, quarantine copy','Unique constraint on ledger','Engineering')
c('SQ002','SIM.Withdrawals','user_id','Orphan record',(~WD.user_id.isin(U.user_id)).sum(),5,'Critical','user_id not in Users','Quarantine','Referential check at ingestion','Data')
c('SQ003','SIM.Withdrawals','final_at','Impossible time order (final before requested)',(WD.final_at<WD.requested_at).sum(),4,'High','final_at < requested_at','Flag for review','Monotonic timestamp rule','Engineering')
c('SQ004','SIM.Referrals','referred_user_id','Self-referral',(RF.referrer_user_id==RF.referred_user_id).sum(),4,'High','referrer = referred','Invalidate referral','Rule: referred != referrer','Engineering')
c('SQ005','SIM.Rewards','reward_amount','Negative amount',(R.reward_amount<0).sum(),3,'High','amount < 0 on non-reversal row','Reject/inspect','amount > 0 validation','Engineering')
wc=W[W.transaction_type=='reward_credit'].drop_duplicates('transaction_id')
cred=R[R.reward_status.isin(['Credited','Reversed','Corrected'])]
c('SQ006','SIM.Rewards vs Wallet','reward_id','Credited reward without wallet credit',(~cred.reward_id.isin(wc.reference_id)).sum(),0,'Critical','credited reward_id not found as wallet reference','Investigate','Reconciliation job','Data/Engineering')
c('SQ007','SIM.Wallet_Transactions','reference_id','Wallet credit without reward',(~wc.reference_id.isin(R.reward_id)).sum(),0,'Critical','wallet reward_credit reference not in Rewards','Investigate','Reconciliation job','Data/Engineering')
ts=WD[(WD.withdrawal_status.isin(['Completed','Rejected','Reversed']))&WD.final_at.isna()]
c('SQ008','SIM.Withdrawals','final_at','Closed status without final timestamp',len(ts),0,'High','status closed AND final_at null','Backfill','State machine validation','Engineering')
bal=W.drop_duplicates('transaction_id').groupby('user_id').amount.sum()
c('SQ009','SIM.Wallet_Transactions','amount','Users with negative net wallet balance',(bal<0).sum(),0,'High','sum(amount) per user < 0','Investigate','Block redemption beyond balance','Engineering')
c('SQ010','SIM.Referrals','acquisition_source','Referred user not marked acquisition_source=Referral',int((~RF.referred_user_id.dropna().isin(U[U.acquisition_source=='Referral'].user_id)).sum()),0,'Medium','referred_user_id not in users with source Referral','Reconcile attribution rules','Single attribution definition','Product/Data')
SQ=pd.DataFrame(chk); SQ['status']=np.where(SQ.records_affected>0,'Open','Check passed - no issue found')
# KPI formula tests (simulated, formula validation only)
kt=[]
def k(i,n,v,note): kt.append(dict(kpi=i,name=n,simulated_test_value=v,note=note))
done=Tk.task_status.eq('Completed'); started=Tk.task_started_at.notna()
k('KPI-E06','Task completion rate (all attempts)',f"{done.sum()/started.sum():.1%}",f"{done.sum()}/{started.sum()}; Pending attempts included")
k('KPI-E06b','Task completion rate (excl. Pending)',f"{done.sum()/(Tk.task_status!='Pending').sum():.1%}",'Pending excluded')
k('KPI-E07','Task abandonment rate',f"{(Tk.task_status=='Abandoned').mean():.1%}",'Abandoned/started')
k('KPI-R01','Reward credits',int((R.reward_status=='Credited').sum()),'status Credited')
k('KPI-R03','Pending rewards',int((R.reward_status=='Pending').sum()),'status Pending')
k('KPI-R04','Reward reversal rate',f"{(R.reward_status=='Reversed').sum()/R.reward_status.isin(['Credited','Reversed','Corrected']).sum():.1%}",'Reversed / all credited-type')
cu=R[R.reward_status=='Credited'].groupby('reward_unit').reward_amount.sum()
k('KPI-R02','Reward credit volume by unit',', '.join(f'{u}={int(v)}' for u,v in cu.items()),'Units never summed together; includes 3 planted negative rows')
k('KPI-R07','Activity-to-credit ratio',f"{R.reward_status.eq('Credited').sum()/done.sum():.1%}",'Credited rewards / completed activities')
Wu=W.drop_duplicates('transaction_id')
k('KPI-W01','Wallet transactions (deduplicated)',len(Wu),f'raw rows {len(W)}')
k('KPI-W04','Wallet reversal rate',f"{(Wu.transaction_type=='reversal').sum()/(Wu.transaction_type=='reward_credit').sum():.1%}",'reversal rows / reward_credit rows')
k('KPI-W03','Redemption entries',int((Wu.transaction_type=='redemption').sum()),'type redemption')
sc=WD.withdrawal_status.value_counts()
k('KPI-D01','Withdrawal requests',len(WD),'')
k('KPI-D02','Completed withdrawals',int(sc.get('Completed',0)),'')
k('KPI-D03','Pending withdrawal queue',int(sc.get('Requested',0)+sc.get('Processing',0)),'Requested + Processing')
k('KPI-D04','Rejected withdrawals',int(sc.get('Rejected',0)),'')
k('KPI-D05','Reversed withdrawals',int(sc.get('Reversed',0)),'')
okp=WD[(WD.withdrawal_status=='Completed')&(WD.final_at>=WD.requested_at)]
k('KPI-D06','Median processing time (hours, Completed)',round(float(((okp.final_at-okp.requested_at).dt.total_seconds()/3600).median()),1),'Excludes open items and 4 planted bad timestamps')
closed=sc.get('Completed',0)+sc.get('Rejected',0)+sc.get('Reversed',0)
k('KPI-D07','Withdrawal completion rate (closed requests)',f"{sc.get('Completed',0)/closed:.1%}",'Completed/(Completed+Rejected+Reversed)')
k('KPI-D08','Method distribution',', '.join(f'{m}={v}' for m,v in WD.method.value_counts().items()),'Placeholder methods')
k('KPI-F01','Referrals created',len(RF),'')
k('KPI-F02','Referral registrations',int(RF.registered_at.notna().sum()),'')
k('KPI-F03','Referral activations',int(RF.activated_at.notna().sum()),'')
k('KPI-F04','Referral conversion rate',f"{(RF.referral_status=='Converted').sum()/len(RF):.1%}",'Converted/created; activation rule To Be Verified')
KT=pd.DataFrame(kt)
if __name__=='__main__':
    pd.set_option('display.width',250,'display.max_colwidth',70,'display.max_columns',20)
    print(PROF.to_string()); print(REL.to_string()); print(SQ[['issue_id','issue_type','records_affected','planted_in_generator']].to_string()); print(KT.to_string())
